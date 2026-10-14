import json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from steps import STEPS
import pyruns

LEAN_DIR = os.path.join(here, "..", "..", "lean_upper_bound", "Proofs")
# step id -> (file stem, note); filled from the Lean agent's report
MAP = json.load(open(os.path.join(here, "leanmap.json"))) if os.path.exists(os.path.join(here, "leanmap.json")) else {}

steps = []
for s in STEPS:
    m = MAP.get(s["id"], {})
    stem = m.get("file", s["lean"])
    path = os.path.join(LEAN_DIR, stem + ".lean")
    if os.path.exists(path):
        code = open(path).read().strip()
        status = "gap" if re.search(r"\bsorry\b", re.sub(r"--.*|/-.*?-/", "", code, flags=re.S)) else "ok"
    else:
        code = "-- not formalized yet"
        status = "gap"
    d = dict(s)
    d["tex"] = re.sub(r"\\emph\{([^}]*)\}", r"<em>\1</em>", s["tex"])
    d["py"] = pyruns.RUNS[s["id"]]
    d.update(leanCode=code, leanStatus=status, leanNote=m.get("note", ""))
    steps.append(d)

tpl = open(os.path.join(here, "template.html")).read()
wit = json.load(open(os.path.join(here, "witnesses_sel.json")))
ver = open(os.path.join(here, "..", "..", "lean_upper_bound", "lean-toolchain")).read().strip().split(":")[-1]
mrev = ""
try:
    man = json.load(open(os.path.join(here, "..", "..", "lean_upper_bound", "lake-manifest.json")))
    mrev = [p["rev"][:10] for p in man["packages"] if p["name"] == "mathlib"][0]
except Exception:
    pass
out = (tpl.replace("__STEPS__", json.dumps(steps, ensure_ascii=False).replace("</", "<\\/"))
          .replace("__WITNESSES__", json.dumps(wit))
          .replace("__PRELUDE__", json.dumps(pyruns.PRELUDE.replace("__G14__", str(wit["14"]["gamma"]))).replace("</", "<\\/"))
          .replace("__LEANVERSION__", f"Checked with Lean {ver}, Mathlib {mrev}."))
open(os.path.join(here, "..", "proof_translation.html"), "w").write(out)
print("ok", sum(x["leanStatus"] == "ok" for x in steps), "proved of", len(steps))
