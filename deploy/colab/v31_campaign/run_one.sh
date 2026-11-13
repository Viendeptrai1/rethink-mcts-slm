#!/bin/bash
# Keep one Colab session's queue going: relaunch from the latest partial after every runtime loss.
# Stops when the queue finishes, after MAX_SHORT consecutive losses shorter than PROBE_MIN minutes
# (Colab still reclaiming quickly), or when the balance drops below MIN_CU.
# usage: run_one.sh <session>       (plan: plans/<session>.plan; partial: colab_results/<session>/)
S=$1; PROBE_MIN=${PROBE_MIN:-30}; MAX_SHORT=${MAX_SHORT:-4}; MIN_CU=${MIN_CU:-10}
SCR=/Users/kotori/Documents/TLCN/deploy/colab/v31_campaign
cd /Users/kotori/Documents/TLCN || exit 1
log(){ echo "$(date '+%F %T') $*"; }
balance(){ colab usage 2>/dev/null | awk '/Current balance/{print int($3)}'; }
stop(){ pkill -f "orchestrate_ls.sh $S " ; pkill -f "watch_ls.sh $S " ; pkill -f "guard_dl.sh $S "; sleep 2
        colab stop -s $S >/dev/null 2>&1; log "STOPPED: $1"; exit 0; }
ready_epoch(){ local l; l=$(grep "\[$S\] session ready" colab_results/$S/orchestrate.log 2>/dev/null | tail -1 | cut -c1-19)
               [ -n "$l" ] && date -j -f '%Y-%m-%d %H:%M:%S' "$l" +%s; }
short=0
bash $SCR/relaunch.sh $S "run_one: start"; log "$S launched"
while true; do
  sleep 60
  b=$(balance); [ -n "$b" ] && [ "$b" -lt "$MIN_CU" ] && stop "balance ${b} CU < ${MIN_CU}"
  f=colab_results/$S/orchestrate.log
  grep -q "\[$S\] finished:" $f 2>/dev/null && { log "$S FINISHED"; exit 0; }
  if grep -qE "SESSION LOST|GIVING UP|FAILED to start" $f 2>/dev/null; then
    r=$(ready_epoch); life=$(( ( $(date +%s) - ${r:-$(date +%s)} ) / 60 ))
    if [ "$life" -lt "$PROBE_MIN" ]; then short=$((short+1)); else short=0; fi
    log "$S lost after ~${life} min (consecutive short losses: $short)"
    [ "$short" -ge "$MAX_SHORT" ] && stop "$short consecutive losses before ${PROBE_MIN} min"
    bash $SCR/relaunch.sh $S "run_one: relaunch after loss (~${life} min)"; log "$S relaunched"
  fi
done
