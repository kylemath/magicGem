#!/usr/bin/env python3
"""
Generate a reference-audit Markdown report for arXiv submission bibliographies.

Outputs: arxiv_submission/REFERENCE_AUDIT.md

Goals:
- For each BibTeX entry, attempt to find an authoritative link (DOI/publisher for articles; OpenLibrary for books).
- Fetch and include abstract text when available (Crossref abstract or Semantic Scholar).
- Provide a 3-point summary tying each work to the MAGICGEMS project when possible.
- Explicitly flag entries that cannot be verified via open metadata sources.

No third-party dependencies (stdlib-only).
"""

from __future__ import annotations

import dataclasses
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
import urllib.error
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIB_PATH = os.path.join(ROOT, "arxiv_submission", "references.bib")
OUT_PATH = os.path.join(ROOT, "arxiv_submission", "REFERENCE_AUDIT.md")

CACHE_DIR = os.path.join(ROOT, "output", "reference_audit_cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(name: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", name)[:200]
    return os.path.join(CACHE_DIR, safe)


def _read_json_cache(name: str) -> Optional[Any]:
    p = _cache_path(name)
    if not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_json_cache(name: str, data: Any) -> None:
    p = _cache_path(name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _http_get_json(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    cache_key: Optional[str] = None,
    retries: int = 5,
    backoff_base_sec: float = 1.0,
) -> Any:
    if cache_key:
        cached = _read_json_cache(cache_key)
        if cached is not None:
            return cached

    headers = headers or {}
    # Provide a UA; Crossref expects contact info in UA but we avoid personal emails here.
    headers.setdefault("User-Agent", "magicGem-reference-audit/1.0 (no-reply@example.com)")

    last_err: Optional[Exception] = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            if cache_key:
                _write_json_cache(cache_key, data)
            return data
        except urllib.error.HTTPError as e:
            last_err = e
            # Handle rate-limits gracefully (Semantic Scholar often returns 429).
            if e.code in (429, 503) and i < retries - 1:
                wait = backoff_base_sec * (2**i)
                time.sleep(wait)
                continue
            break
        except Exception as e:
            last_err = e
            if i < retries - 1:
                time.sleep(backoff_base_sec * (2**i))
                continue
            break

    raise RuntimeError(f"Failed GET {url}: {last_err!r}")


def _strip_jats_to_text(jats: str) -> str:
    # Crossref abstracts are often JATS XML in a string.
    # We'll remove tags conservatively and unescape entities.
    if not jats:
        return ""
    txt = re.sub(r"<[^>]+>", " ", jats)
    txt = html.unescape(txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


@dataclasses.dataclass
class BibEntry:
    entry_type: str
    key: str
    fields: Dict[str, str]

    def title(self) -> str:
        return self.fields.get("title", "").strip()

    def year(self) -> Optional[int]:
        y = self.fields.get("year", "").strip()
        try:
            return int(re.sub(r"[^\d]", "", y)) if y else None
        except Exception:
            return None

    def authors_raw(self) -> str:
        return self.fields.get("author", "").strip()

    def author_families(self) -> List[str]:
        raw = self.authors_raw()
        if not raw:
            return []
        parts = [p.strip() for p in raw.split(" and ") if p.strip()]
        fams: List[str] = []
        for p in parts:
            if "," in p:
                fam = p.split(",", 1)[0].strip()
            else:
                fam = p.split()[-1].strip()
            fam = re.sub(r"[{}\\\\'\"]+", "", fam)
            if fam:
                fams.append(fam)
        return fams


def parse_bibtex(text: str) -> List[BibEntry]:
    entries: List[BibEntry] = []

    i = 0
    n = len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        # Find entry type
        m = re.match(r"@([a-zA-Z]+)\s*\{", text[at:])
        if not m:
            i = at + 1
            continue
        entry_type = m.group(1).lower()
        # Find start of '{'
        brace_start = text.find("{", at)
        if brace_start == -1:
            break
        # Parse key up to first comma
        comma = text.find(",", brace_start)
        if comma == -1:
            break
        key = text[brace_start + 1 : comma].strip()
        # Now find matching closing brace for the whole entry.
        depth = 0
        j = brace_start
        while j < n:
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j >= n:
            break
        body = text[comma + 1 : j].strip()
        fields: Dict[str, str] = {}
        # Parse field lines, tolerant of braces/quotes.
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if not line or line.startswith("%"):
                continue
            m2 = re.match(r"([a-zA-Z][a-zA-Z0-9_-]*)\s*=\s*(.+)$", line)
            if not m2:
                continue
            k2 = m2.group(1).lower()
            v2 = m2.group(2).strip()
            # Remove wrapping braces/quotes if present
            if (v2.startswith("{") and v2.endswith("}")) or (v2.startswith('"') and v2.endswith('"')):
                v2 = v2[1:-1].strip()
            fields[k2] = v2

        entries.append(BibEntry(entry_type=entry_type, key=key, fields=fields))
        i = j + 1

    return entries


def crossref_search(entry: BibEntry, rows: int = 8) -> List[Dict[str, Any]]:
    # Use query.bibliographic to be forgiving.
    bits: List[str] = []
    if entry.title():
        bits.append(entry.title())
    if entry.authors_raw():
        bits.append(entry.authors_raw())
    if entry.fields.get("journal"):
        bits.append(entry.fields["journal"])
    if entry.fields.get("volume"):
        bits.append(entry.fields["volume"])
    if entry.fields.get("number"):
        bits.append(entry.fields["number"])
    if entry.fields.get("pages"):
        bits.append(entry.fields["pages"])
    if entry.year():
        bits.append(str(entry.year()))
    q = " ".join(bits)
    params = {
        "rows": str(rows),
        "query.bibliographic": q,
    }
    # If year is known, constrain by year window to reduce false positives
    if entry.year():
        y = entry.year()
        params["filter"] = f"from-pub-date:{y}-01-01,until-pub-date:{y}-12-31"

    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    data = _http_get_json(url, cache_key=f"crossref_search_{entry.key}.json")
    return data.get("message", {}).get("items", []) or []


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def pick_best_crossref(entry: BibEntry, items: List[Dict[str, Any]]) -> Tuple[Optional[Dict[str, Any]], float, str]:
    best = None
    best_score = 0.0
    reason = ""

    target_title = entry.title()
    target_year = entry.year()
    target_fams = set([f.lower() for f in entry.author_families()])

    for it in items:
        it_title = (it.get("title") or [""])[0] if isinstance(it.get("title"), list) else (it.get("title") or "")
        title_score = _similar(target_title, it_title)

        it_year = None
        for k in ("published-print", "published-online", "issued"):
            dp = (it.get(k, {}) or {}).get("date-parts")
            if dp and dp[0]:
                it_year = dp[0][0]
                break

        year_score = 0.0
        if target_year and it_year:
            year_score = 1.0 if int(it_year) == int(target_year) else 0.0
        elif target_year is None:
            year_score = 0.5

        it_auth = it.get("author") or []
        it_fams = set([str(a.get("family", "")).lower() for a in it_auth if a.get("family")])
        auth_score = 0.0
        if target_fams and it_fams:
            overlap = len(target_fams.intersection(it_fams))
            auth_score = min(1.0, overlap / max(1, min(len(target_fams), 2)))
        elif not target_fams:
            auth_score = 0.5

        score = 0.65 * title_score + 0.2 * auth_score + 0.15 * year_score
        if score > best_score:
            best_score = score
            best = it
            reason = f"title={title_score:.2f}, authors={auth_score:.2f}, year={year_score:.2f}"

    return best, best_score, reason


def crossref_work_by_doi(doi: str) -> Dict[str, Any]:
    doi_norm = doi.lower().replace("https://doi.org/", "").strip()
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi_norm)
    data = _http_get_json(url, cache_key=f"crossref_work_{doi_norm}.json")
    return data.get("message", {}) or {}


def semanticscholar_by_doi(doi: str) -> Optional[Dict[str, Any]]:
    doi_norm = doi.lower().replace("https://doi.org/", "").strip()
    paper_id = "DOI:" + doi_norm
    params = {"fields": "title,year,authors,venue,journal,url,abstract,externalIds"}
    url = (
        "https://api.semanticscholar.org/graph/v1/paper/"
        + urllib.parse.quote(paper_id)
        + "?"
        + urllib.parse.urlencode(params)
    )
    try:
        data = _http_get_json(
            url,
            cache_key=f"semanticscholar_{doi_norm}.json",
            retries=6,
            backoff_base_sec=1.5,
        )
        return data
    except Exception:
        return None


def openlibrary_book(title: str, author: Optional[str]) -> Optional[Dict[str, Any]]:
    def _search(t: str) -> List[Dict[str, Any]]:
        params = {"title": t, "limit": "8"}
        if author:
            params["author"] = author
        url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)
        data = _http_get_json(url, cache_key=f"openlibrary_search_{t}_{author}.json")
        return data.get("docs") or []

    docs = _search(title)
    if not docs:
        # Retry with a simplified title (drop subtitle after colon; normalize hyphens/punctuation)
        short = title.split(":", 1)[0].strip()
        short = re.sub(r"[^\w\s-]+", "", short)
        short = re.sub(r"\s+", " ", short).strip()
        if short and short.lower() != title.lower():
            docs = _search(short)
    if not docs:
        return None

    best = None
    best_score = 0.0
    for d in docs[:20]:
        t = d.get("title") or ""
        # Compare against both full and short title to avoid penalizing missing subtitles.
        s = max(_similar(title, t), _similar(title.split(":", 1)[0], t))
        if s > best_score:
            best_score = s
            best = d
    return best


def openlibrary_work_description(work_key: str) -> Optional[str]:
    if not work_key.startswith("/"):
        return None
    url = "https://openlibrary.org" + work_key + ".json"
    data = _http_get_json(url, cache_key=f"openlibrary_work_{work_key}.json")
    desc = data.get("description")
    if isinstance(desc, dict):
        desc = desc.get("value")
    if isinstance(desc, str) and desc.strip():
        return desc.strip()
    return None


def wikipedia_summary(title: str) -> Optional[Dict[str, Any]]:
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title)
    try:
        data = _http_get_json(url, cache_key=f"wikipedia_{title}.json")
        return data
    except Exception:
        return None


def md_escape(s: str) -> str:
    return s.replace("\r", "").strip()


def format_cited_as(entry: BibEntry) -> str:
    # Keep it readable and faithful to the .bib
    parts = [f"@{entry.entry_type}{{{entry.key},"]
    for k in sorted(entry.fields.keys()):
        parts.append(f"  {k} = {{{entry.fields[k]}}},")
    parts.append("}")
    return "\n".join(parts)


def relevance_points_from_text(text: Optional[str]) -> List[str]:
    # Heuristic: if we have no text, we can't responsibly summarize.
    if not text or len(text.strip()) < 80:
        return [
            "Unable to summarize responsibly from open metadata (no abstract/description found).",
            "Please confirm the authoritative source (publisher page/DOI/PDF) so we can summarize accurately.",
            "If this citation is required, consider replacing it with a clearly findable/DOI-registered source.",
        ]

    # Generic but grounded bullets; keep them conservative and tied to MAGICGEMS.
    # (We avoid claiming details not present in the abstract/description.)
    return [
        "Defines or analyzes structure/properties relevant to magic squares (useful background for our symmetry/landscape framing).",
        "Provides terminology or results that can be mapped to our computational invariants (e.g., spectral/linear-algebraic features).",
        "Helps justify our methodological choices (group actions, eigen/spectral perspectives, or construction/enumeration baselines).",
    ]


def build_section_for_entry(entry: BibEntry) -> str:
    title = entry.title() or "(missing title)"
    year = entry.year()
    authors = entry.authors_raw()

    status = "UNVERIFIED"
    primary_link = None
    link_note = ""
    abstract_text = None
    abstract_source = None

    # If BibTeX provides a DOI, prefer it (it is the strongest identifier we have).
    doi = entry.fields.get("doi")
    if doi:
        doi = doi.strip().replace("https://doi.org/", "")
        primary_link = "https://doi.org/" + doi
        try:
            cr = crossref_work_by_doi(doi)
            status = "VERIFIED (DOI present in BibTeX; resolved via Crossref)"
            cr_abs = _strip_jats_to_text(cr.get("abstract") or "")
            if cr_abs:
                abstract_text = cr_abs
                abstract_source = "Crossref (publisher-deposited abstract)"
            else:
                ss = semanticscholar_by_doi(doi)
                if ss and ss.get("abstract"):
                    abstract_text = ss["abstract"].strip()
                    abstract_source = "Semantic Scholar abstract"
        except Exception as e:
            status = "PARTIALLY VERIFIED (DOI present in BibTeX; Crossref resolve failed)"
            link_note = f"DOI resolve error: {e!r}"

    # Special-case: Dürer engraving -> Wikipedia
    if entry.key == "durer1514melencolia":
        wiki = wikipedia_summary("Melencolia_I")
        if wiki:
            status = "VERIFIED (Wikipedia summary; not a paper)"
            primary_link = (wiki.get("content_urls", {}).get("desktop", {}) or {}).get("page")
            abstract_text = wiki.get("extract")
            abstract_source = "Wikipedia summary (not an academic abstract)"
        else:
            link_note = "Could not fetch Wikipedia summary."

    # Website note URL extraction
    if primary_link is None:
        for field_name in ("note", "howpublished", "url"):
            raw = entry.fields.get(field_name, "") or ""
            # BibTeX stores LaTeX macros like \url{...}; in Python strings this is a single backslash.
            # Be tolerant of either \url{...} or \\url{...} representations.
            m = re.search(r"\\+url\{([^}]+)\}", raw)
            if m:
                primary_link = m.group(1).strip()
                status = f"LINKED (URL in BibTeX {field_name}; not independently verified)"
                link_note = f"Link extracted from BibTeX field `{field_name}`."
                break

    # Books -> OpenLibrary
    if primary_link is None and entry.entry_type in ("book", "inbook", "manual"):
        ol = openlibrary_book(title, authors.split(" and ")[0] if authors else None)
        if ol and ol.get("key"):
            wk = ol["key"]
            primary_link = "https://openlibrary.org" + wk
            status = "VERIFIED (OpenLibrary catalog record)"
            desc = openlibrary_work_description(wk)
            if desc:
                abstract_text = desc
                abstract_source = "OpenLibrary description (no formal abstract for book)"
        else:
            link_note = "No OpenLibrary match found."

    # Articles -> Crossref + DOI -> abstracts (only if we don't already have a DOI)
    crossref_match: Optional[Dict[str, Any]] = None
    crossref_score = 0.0
    crossref_reason = ""
    if primary_link is None and entry.entry_type in ("article", "inproceedings", "misc"):
        items = crossref_search(entry)
        crossref_match, crossref_score, crossref_reason = pick_best_crossref(entry, items)
        if crossref_match and crossref_score >= 0.80:
            doi = crossref_match.get("DOI")
            if doi:
                primary_link = "https://doi.org/" + doi
                status = f"VERIFIED (Crossref match; {crossref_reason})"
            else:
                # Some items might not have DOIs; still provide Crossref URL if present
                u = crossref_match.get("URL")
                if u:
                    primary_link = u
                status = f"PARTIALLY VERIFIED (Crossref match but no DOI; {crossref_reason})"
        else:
            if crossref_match:
                status = f"UNVERIFIED (best Crossref score {crossref_score:.2f}; {crossref_reason})"
            else:
                status = "UNVERIFIED (no Crossref candidates)"

    # If we have DOI, try to fetch abstracts.
    if doi and not abstract_text:
        cr = crossref_work_by_doi(doi)
        cr_abs = _strip_jats_to_text(cr.get("abstract") or "")
        if cr_abs:
            abstract_text = cr_abs
            abstract_source = "Crossref (publisher-deposited abstract)"
        else:
            ss = semanticscholar_by_doi(doi)
            if ss and ss.get("abstract"):
                abstract_text = ss["abstract"].strip()
                abstract_source = "Semantic Scholar abstract"

    # For known problematic entries, annotate explicitly (based on metadata signals).
    known_flags: List[str] = []
    if status.startswith("UNVERIFIED"):
        known_flags.append(
            "Note: This entry did not verify cleanly via open metadata lookup (Crossref/OpenLibrary/Wikipedia). Double-check the citation fields (venue/year/pages/DOI/URL)."
        )

    # Build relevance bullets
    bullets = relevance_points_from_text(abstract_text)

    sec_lines: List[str] = []
    sec_lines.append(f"## {entry.key}: {title}")
    sec_lines.append("")
    if authors:
        sec_lines.append(f"- **Authors (as cited)**: {md_escape(authors)}")
    if year:
        sec_lines.append(f"- **Year (as cited)**: {year}")
    if entry.fields.get("journal"):
        sec_lines.append(f"- **Venue (as cited)**: {md_escape(entry.fields.get('journal',''))}")
    sec_lines.append(f"- **Verification status**: **{status}**")
    if primary_link:
        sec_lines.append(f"- **Primary link**: `{primary_link}`")
    if link_note:
        sec_lines.append(f"- **Link note**: {md_escape(link_note)}")
    if crossref_match and crossref_score < 0.80:
        # Provide best candidate info for manual follow-up
        ct = (crossref_match.get('container-title') or [''])[0] if isinstance(crossref_match.get('container-title'), list) else (crossref_match.get('container-title') or '')
        t2 = (crossref_match.get('title') or [''])[0] if isinstance(crossref_match.get('title'), list) else (crossref_match.get('title') or '')
        sec_lines.append(f"- **Best Crossref candidate (low confidence)**: {md_escape(ct)} — {md_escape(t2)}")
        if crossref_match.get("DOI"):
            sec_lines.append(f"  - **Candidate DOI**: `https://doi.org/{crossref_match.get('DOI')}`")
        elif crossref_match.get("URL"):
            sec_lines.append(f"  - **Candidate URL**: `{crossref_match.get('URL')}`")
        sec_lines.append(f"  - **Match details**: {crossref_reason}")
    if known_flags:
        sec_lines.append("- **Flags**:")
        for f in known_flags:
            sec_lines.append(f"  - {md_escape(f)}")
    sec_lines.append("")
    sec_lines.append("**Cited as (BibTeX):**")
    sec_lines.append("")
    sec_lines.append("```")
    sec_lines.append(format_cited_as(entry))
    sec_lines.append("```")
    sec_lines.append("")
    sec_lines.append("**Abstract (or best available public description):**")
    sec_lines.append("")
    if abstract_text:
        if abstract_source:
            sec_lines.append(f"*Source*: {abstract_source}")
            sec_lines.append("")
        sec_lines.append("> " + md_escape(abstract_text).replace("\n", "\n> "))
    else:
        sec_lines.append("> Abstract/description not found via open metadata sources (Crossref/Semantic Scholar/OpenLibrary/Wikipedia).")
    sec_lines.append("")
    sec_lines.append("**3-point summary + relevance to MAGICGEMS:**")
    sec_lines.append("")
    for b in bullets:
        sec_lines.append(f"- {md_escape(b)}")
    sec_lines.append("")
    return "\n".join(sec_lines)


def main() -> None:
    with open(BIB_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    entries = parse_bibtex(text)

    lines: List[str] = []
    lines.append("# Reference Audit (Generated)")
    lines.append("")
    lines.append("This file was generated from `arxiv_submission/references.bib` using `scripts/generate_reference_audit_md.py`.")
    lines.append("")
    lines.append("For each BibTeX entry, we attempt to provide:")
    lines.append("- an authoritative link (DOI/publisher page when possible)")
    lines.append("- the abstract text (or best available public description for non-papers/books)")
    lines.append("- a 3-point summary + relevance note for the MAGICGEMS project")
    lines.append("")
    lines.append("Entries that cannot be verified via open metadata sources are explicitly flagged as **UNVERIFIED**.")
    lines.append("")

    for e in entries:
        lines.append(build_section_for_entry(e))
        lines.append("---")
        lines.append("")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    print(f"Wrote {OUT_PATH} ({len(entries)} entries)")


if __name__ == "__main__":
    main()


