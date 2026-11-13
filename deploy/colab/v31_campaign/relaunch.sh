#!/bin/bash
# Relaunch a lost Colab session from its latest downloaded partial.
# 1. stops its local watcher/guard, 2. archives logs + partial into a fresh colab_results/<s>_lostN,
# 3. drops completed problems whose CRLF code would trip the frozen resume check (re-solved),
# 4. starts orchestrate_ls.sh (SEED_RUNS) and a 5-min download guard.
# usage: relaunch.sh <session> "<reason>"
set -u
S=$1; REASON=$2
SCR=/Users/kotori/Documents/TLCN/deploy/colab/v31_campaign
F=/Users/kotori/Documents/TLCN/colab_results/freeze
cd /Users/kotori/Documents/TLCN || exit 1
pkill -f "watch_ls.sh $S " ; pkill -f "guard_dl.sh $S " ; pkill -f "orchestrate_ls.sh $S "
sleep 1
n=1; while [ -e "colab_results/${S}_lost$n" ]; do n=$((n+1)); done
P=colab_results/${S}_lost$n; mkdir -p "$P"
cp colab_results/$S/partial.tar.gz "$P/partial_last.tar.gz" || { echo "no partial for $S"; exit 1; }
for f in orchestrate.log nohup.out guard.out; do [ -f colab_results/$S/$f ] && mv colab_results/$S/$f "$P/"; done
PLANFILE=$SCR/plans/${PLAN_NAME:-$S}.plan
# only runs that the plan will re-enter can trip the resume check; never drop problems of a run
# that is no longer in the plan (it is complete and would not be re-solved)
victims=$(python3 $SCR/check_resume.py "$P/partial_last.tar.gz" | while read v; do r=$(echo "$v" | cut -d/ -f2); grep -q "output-dir /content/runs/$r " "$PLANFILE" && echo "$v"; done)
SEEDTAR="$P/partial_last.tar.gz"
if [ -n "$victims" ]; then
  W=$(mktemp -d /Users/kotori/Documents/TLCN/colab_results/build.XXXX); tar xzf "$P/partial_last.tar.gz" -C "$W" runs
  mkdir -p "$P/crlf_resume_victims"
  for v in $victims; do mv "$W/$v" "$P/crlf_resume_victims/$(echo $v | tr / _)"; done
  (cd "$W" && tar czf "/Users/kotori/Documents/TLCN/$P/seed_fixed.tar.gz" runs)
  SEEDTAR="$P/seed_fixed.tar.gz"
  [ -z "$(python3 $SCR/check_resume.py "$SEEDTAR")" ] || { echo "fixed archive still has victims"; exit 1; }
fi
counts=$(tar tzf "$SEEDTAR" | grep completed.json | awk -F/ '{print $2}' | sort | uniq -c | tr '\n' ' ')
echo "--- $S: $REASON; restarting from $SEEDTAR [$counts] dropped: ${victims:-none}" > colab_results/$S/orchestrate.log
SEED_RUNS="$SEEDTAR" MAX_ALLOC_TRIES=600 nohup deploy/colab/orchestrate_ls.sh $S $SCR/plans/${PLAN_NAME:-$S}.plan $F/tlcn_v3.tar.gz colab_results/$S > colab_results/$S/nohup.out 2>&1 &
INTERVAL=300 nohup deploy/colab/guard_dl.sh $S colab_results/$S > colab_results/$S/guard.out 2>&1 &
echo "$S -> $P; seed $SEEDTAR; $counts; dropped: ${victims:-none}"
