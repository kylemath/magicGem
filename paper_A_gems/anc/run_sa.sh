#!/bin/bash
# n total steps T0 T1 -> split over 16 seeds
n=$1; tot=$2; steps=$3; T0=$4; T1=$5
per=$(( (tot+15)/16 ))
for s in $(seq 1 16); do
  ./sa_magic $n $per $((s*1000+n)) $steps $T0 $T1 100 > sa_out/sa_n${n}_$s.txt 2> sa_out/sa_n${n}_$s.log &
done
wait
