#!/bin/bash
# Reproduce every number, figure and JSON in this directory with one command:
#     bash run_all.sh            (about 3 min without MC; add "mc" to also rerun the Monte Carlo, ~10 min on 16 cores)
# Members of L_4 (234 MB) are written to $WORK/members_n4.bin (default: ./work, git-ignored).
set -e
cd "$(dirname "$0")"
WORK=${WORK:-./work}; mkdir -p "$WORK" raw_outputs
cc -O3 -march=native -o lowmode_enum lowmode_enum.c -lpthread
cc -O3 -march=native -o lowmode_mc lowmode_mc.c
: > raw_outputs/enum_n3.jsonl; : > raw_outputs/enum_n4.jsonl
for m in L XY DIAG MAGIC SEMI ROWSL COLSL; do ./lowmode_enum 3 $m - 16 2>/dev/null >> raw_outputs/enum_n3.jsonl; done
./lowmode_enum 4 L "$WORK/members_n4.bin" 16 2>/dev/null >> raw_outputs/enum_n4.jsonl
for m in XY DIAG MAGIC SEMI ROWSL COLSL; do ./lowmode_enum 4 $m - 16 2>/dev/null >> raw_outputs/enum_n4.jsonl; done
if [ "$1" = "mc" ]; then
  for n in 4 5 6; do
    case $n in 4) ns=125000000;; 5) ns=625000000;; 6) ns=1250000000;; esac
    : > raw_outputs/mc_n$n.jsonl
    for t in $(seq 1 16); do ./lowmode_mc $n $ns $((1000*n+t)) >> raw_outputs/mc_n$n.jsonl & done; wait
  done
fi
python3 gaussian_estimate.py
python3 analyze_members.py "$WORK/members_n4.bin"
python3 assemble_results.py
