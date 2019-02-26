#!/bin/bash
numMatches=0
numTests=100
for i in `seq 1 $numTests`;
  do
    python3 othello.py random1 student | grep "student (white) wins" &> /dev/null
    if [ $? -eq 0 ]; then
      numMatches=$((numMatches + 1))
      echo "Test $i passed"
    else
      echo "Test $i failed"
    fi
  done
echo "$numMatches tests passed total"
awk -v m="$numMatches" -v n="$numTests" 'BEGIN{printf "%.0f%% of tests passed\n", m/n * 100}'
