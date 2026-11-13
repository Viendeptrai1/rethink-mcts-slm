#!/bin/bash
# Tonight's Qwen3.5-9B run (user: "tối nay chạy lại", 13/11/2026).
# A = qwen35  (BoN16 APPS, Direct APPS, all HumanEval)   B = qwen35b (APPS MCTS only); disjoint runs.
# - waits until START (HH:MM), then starts A from its latest partial
# - starts B only after some runtime has stayed alive >= PROBE_MIN minutes (runtimes stable)
# - on loss: relaunch from the latest partial; a loss before PROBE_MIN counts as "short";
#   MAX_SHORT consecutive short losses -> stop everything (Colab still reclaiming)
# - stops everything if the balance drops below MIN_CU
# Each session downloads results and stops itself when its queue is done (watch_ls.sh).
START=${START:-22:30}; PROBE_MIN=${PROBE_MIN:-30}; MAX_SHORT=${MAX_SHORT:-4}; MIN_CU=${MIN_CU:-15}
SCR=/Users/kotori/Documents/TLCN/deploy/colab/v31_campaign
cd /Users/kotori/Documents/TLCN || exit 1
log(){ echo "$(date '+%F %T') $*"; }
balance(){ colab usage 2>/dev/null | awk '/Current balance/{print int($3)}'; }
stop_all(){
  pkill -f "orchestrate_ls.sh qwen35" ; pkill -f "watch_ls.sh qwen35" ; pkill -f "guard_dl.sh qwen35"
  sleep 2; colab stop -s qwen35 >/dev/null 2>&1; colab stop -s qwen35b >/dev/null 2>&1
  log "STOPPED ALL: $1"; exit 0
}
ready_epoch(){ # epoch of the current session's "session ready" line, empty if none
  local l; l=$(grep "\[$1\] session ready" colab_results/$1/orchestrate.log 2>/dev/null | tail -1 | cut -c1-19)
  [ -n "$l" ] && date -j -f '%Y-%m-%d %H:%M:%S' "$l" +%s
}

now=$(date +%s); target=$(date -j -f '%Y-%m-%d %H:%M' "$(date +%F) $START" +%s)
[ "$target" -gt "$now" ] && { log "waiting until $START"; sleep $((target - now)); }
b=$(balance); log "balance ${b} CU"; [ -n "$b" ] && [ "$b" -lt "$MIN_CU" ] && { log "balance too low, not starting"; exit 1; }

doneA=0; doneB=0; startedB=0; short=0; stable=0
bash $SCR/relaunch.sh qwen35 "tonight run: A (BoN16/Direct APPS + HumanEval)" ; log "A launched"
while true; do
  sleep 60
  b=$(balance); [ -n "$b" ] && [ "$b" -lt "$MIN_CU" ] && stop_all "balance ${b} CU < ${MIN_CU}"
  for s in qwen35 qwen35b; do
    [ "$s" = qwen35 ] && [ $doneA = 1 ] && continue
    [ "$s" = qwen35b ] && { [ $startedB = 0 ] || [ $doneB = 1 ]; } && continue
    f=colab_results/$s/orchestrate.log
    if grep -q "\[$s\] finished:" $f 2>/dev/null; then
      log "$s finished"; [ "$s" = qwen35 ] && doneA=1 || doneB=1; continue
    fi
    if grep -qE "SESSION LOST|GIVING UP|FAILED to start" $f 2>/dev/null; then
      r=$(ready_epoch $s); life=$(( ( $(date +%s) - ${r:-$(date +%s)} ) / 60 ))
      if [ "$life" -lt "$PROBE_MIN" ]; then short=$((short+1)); else short=0; fi
      log "$s lost after ~${life} min (consecutive short losses: $short)"
      [ "$short" -ge "$MAX_SHORT" ] && stop_all "$short consecutive losses before ${PROBE_MIN} min"
      bash $SCR/relaunch.sh $s "tonight: relaunch after loss (~${life} min)"; log "$s relaunched"
      continue
    fi
    r=$(ready_epoch $s)
    if [ -n "$r" ] && [ $(( ($(date +%s) - r) / 60 )) -ge "$PROBE_MIN" ]; then
      [ $stable = 0 ] && log "$s alive >= ${PROBE_MIN} min: runtimes look stable"; stable=1; short=0
    fi
  done
  if [ $stable = 1 ] && [ $startedB = 0 ]; then
    startedB=1; bash $SCR/relaunch.sh qwen35b "tonight run: B (APPS MCTS)"; log "B launched"
  fi
  if [ $doneA = 1 ] && { [ $doneB = 1 ] || { [ $startedB = 0 ] && false; }; }; then log "ALL DONE"; exit 0; fi
  if [ $doneA = 1 ] && [ $startedB = 0 ]; then startedB=1; bash $SCR/relaunch.sh qwen35b "tonight run: B after A finished"; log "B launched (A done)"; fi
done
