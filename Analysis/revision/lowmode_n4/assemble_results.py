#!/usr/bin/env python3
"""Collect raw_outputs/*.jsonl, gaussian_estimates.json and members_analysis.json into results.json."""
import json, os, math, glob, platform, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
def J(p): return json.load(open(os.path.join(HERE, p)))
def JL(p): return [json.loads(l) for l in open(os.path.join(HERE, p)) if l.strip()]

enum = {}
for n in (3, 4):
    for r in JL(f"raw_outputs/enum_n{n}.jsonl"):
        enum.setdefault(str(n), {})[r["mode"]] = {k: v for k, v in r.items() if k not in ("n", "mode")}
gauss = J("gaussian_estimates.json")["per_n"]
mem = J("members_analysis.json")

mc = {}
for p in sorted(glob.glob(os.path.join(HERE, "raw_outputs/mc_n*.jsonl"))):
    rs = JL(os.path.relpath(p, HERE))
    if not rs: continue
    n = rs[0]["n"]; S = sum(r["samples"] for r in rs)
    rec = {"samples": S, "processes": len(rs)}
    for k in ("XY", "DIAG", "L"):
        h = sum(r["hits_" + k] for r in rs); p_ = h / S
        rec[k] = {"hits": h, "prob": p_, "rel_stderr": (1 / math.sqrt(h)) if h else None,
                  "count_estimate": p_ * math.factorial(n * n),
                  "ratio_mc_over_gauss": p_ / gauss[str(n)]["gauss_prob_" + k]}
    mc[str(n)] = rec

exact_L4 = enum["4"]["L"]["count"]
res = {
  "machine": {"cpu": subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip(),
              "cores": os.cpu_count(), "platform": platform.platform(), "python": platform.python_version(),
              "compiler": "Apple clang 17 (cc -O3 -march=native)"},
  "conventions": "cells (i,j) 0-indexed; T1 = sum j s_ij, T2 = sum i s_ij, target (n-1)N(N+1)/4; "
                 "T3 = main diagonal, T4 = anti-diagonal, target M = n(N+1)/2. L_n = {T1=T2=target, T3=T4=M}.",
  "n3": {"L": enum["3"]["L"]["count"], "XY": enum["3"]["XY"]["count"], "DIAG": enum["3"]["DIAG"]["count"],
         "MAGIC": enum["3"]["MAGIC"]["count"], "SEMI": enum["3"]["SEMI"]["count"],
         "brute_force_reference": {"L": 8, "XY": 760, "DIAG": 4224, "MAGIC": 8, "SEMI": 72}},
  "n4": {"L4": exact_L4, "L4_over_16fact": exact_L4 / math.factorial(16),
         "XY": enum["4"]["XY"]["count"], "XY_over_16fact": enum["4"]["XY"]["count"] / math.factorial(16),
         "DIAG": enum["4"]["DIAG"]["count"], "DIAG_independent_combinatorial_check": 49932288000,
         "MAGIC": enum["4"]["MAGIC"]["count"], "SEMI": enum["4"]["SEMI"]["count"], "SEMI_over_8": enum["4"]["SEMI"]["count"] // 8,
         "ROWSL": enum["4"]["ROWSL"]["count"], "COLSL": enum["4"]["COLSL"]["count"],
         "breakdown_rows_cols_equal_34": mem["hist_rows_cols_equal_34"],
         "breakdown_coarse": {"magic": mem["magic"], "rows_all_34_not_cols": mem["rows_all_not_cols"],
                              "cols_all_34_not_rows": mem["cols_all_not_rows"], "neither_all": mem["neither_all"],
                              "no_line_equal_34": mem["no_line_equal_34"]},
         "d4_orbits": mem["d4_orbits"], "paper_example_in_L4": mem["paper_example_in_L4"],
         "E_full_nonmagic": mem["E_full_nonmagic"],
         "distinct_sorted_row_deviation_patterns": mem["distinct_row_deviation_patterns"],
         "runtime_seconds": {m: enum["4"][m]["seconds"] for m in enum["4"]},
         "threads": enum["4"]["L"]["threads"]},
  "gaussian_local_limit": {n: {k: v for k, v in g.items() if k != "cov_T1T2T3T4"} for n, g in gauss.items()},
  "monte_carlo": mc,
  "estimates_L5_L6": {},
  "gallery": mem["gallery"],
}
# conjectural estimates: Gaussian and MC, plus Gaussian x (n=4 correction ratio) for reference
for n in ("5", "6"):
    g = gauss[n]["gauss_count_L"]
    e = {"gaussian_count": g, "gaussian_times_n4_ratio": g * gauss["4"]["ratio_exact_over_gauss_L"]}
    if n in mc: e["mc_count"] = mc[n]["L"]["count_estimate"]; e["mc_rel_stderr"] = mc[n]["L"]["rel_stderr"]
    res["estimates_L5_L6"][n] = e
with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: res[k] for k in ("n3", "n4", "monte_carlo", "estimates_L5_L6")}, indent=1))
