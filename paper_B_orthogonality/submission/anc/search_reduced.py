#!/usr/bin/env python3
"""Reduced-scale rerun of the local-search experiment (Table 'search'): 2e4 steepest-descent runs and
64 annealing runs per order instead of 2e5 and 400.  Writes search_reduced.json.
Full-scale data: algo_results.json (produced by `python3 algorithms.py`, ~1 h on 16 cores)."""
import json, os
import algorithms as A
A.RUNS_GREEDY = 20000
A.RUNS_SA = 64
if __name__ == '__main__':
    r = A.run_all()
    json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'search_reduced.json'), 'w'), indent=1)
