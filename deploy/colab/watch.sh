#!/bin/bash
# Re-attach to a Colab session whose queue (run_plan.sh) is already running: keep the kernel busy,
# poll, and when the queue is done/failed (or MAX_HOURS passes) download results and stop it.
# Use when an orchestrate.sh process died or lost its connection; it never restarts the queue.
# usage: deploy/colab/watch.sh <session-name> <out-dir>
SESSION=$1; OUT=$2
MAX_HOURS=${MAX_HOURS:-14}; MAX_ERRORS=${MAX_ERRORS:-30}
mkdir -p "$OUT"; LOG="$OUT/orchestrate.log"
log(){ echo "$(date '+%F %T') [$SESSION] $*" | tee -a "$LOG"; }

remote(){
  python3 - "$1" <<'PY' | colab exec -s "$SESSION" --timeout "${2:-120}" 2>&1
import sys, json
print("import subprocess")
print("r = subprocess.run(%s, shell=True, capture_output=True, text=True, executable='/bin/bash')" % json.dumps(sys.argv[1]))
print("print(r.stdout + r.stderr)")
PY
}

finish(){
  log "collecting results"
  remote 'cd /content && tar czf /content/results.tar.gz runs *.log 2>/dev/null; ls -l /content/results.tar.gz' 600 >> "$LOG"
  colab download -s "$SESSION" /content/results.tar.gz "$OUT/results.tar.gz" >> "$LOG" 2>&1 || log "download of results.tar.gz failed"
  for f in queue.log setup.log; do colab download -s "$SESSION" /content/$f "$OUT/$f" >> "$LOG" 2>&1; done
  log "stopping session"
  colab stop -s "$SESSION" >> "$LOG" 2>&1 || log "colab stop failed: STOP IT BY HAND"
  log "finished: $1"
  exit 0
}

queue_state(){ # via the contents API (does not need the kernel)
  if colab ls -s "$SESSION" /content 2>/dev/null | grep -q '^QUEUE_DONE'; then echo DONE
  elif colab ls -s "$SESSION" /content 2>/dev/null | grep -q '^QUEUE_FAILED'; then echo FAILED
  elif colab ls -s "$SESSION" /content >/dev/null 2>&1; then echo RUNNING
  else echo UNREACHABLE; fi
}

log "watch attached"
errors=0; started=$(date +%s)
while true; do
  [ $(( $(date +%s) - started )) -gt $(( MAX_HOURS * 3600 )) ] && finish "MAX_HOURS=$MAX_HOURS reached"
  out=$(python3 - <<'PY' | colab exec -s "$SESSION" --timeout 900 2>&1
print('''import os, time, subprocess
for _ in range(10):
    if os.path.exists("/content/QUEUE_DONE") or os.path.exists("/content/QUEUE_FAILED"):
        break
    time.sleep(60)
tail = subprocess.run("tail -2 /content/queue.log", shell=True, capture_output=True, text=True).stdout
state = "DONE" if os.path.exists("/content/QUEUE_DONE") else ("FAILED" if os.path.exists("/content/QUEUE_FAILED") else "RUNNING")
print("STATE", state); print(tail)''')
PY
)
  if echo "$out" | grep -q "^STATE"; then
    errors=0
    echo "$out" | sed "s/^/$(date '+%T') /" >> "$LOG"
  else
    # The kernel websocket can drop while the VM is fine: ask the contents API before giving up.
    state=$(queue_state)
    errors=$((errors+1)); log "poll error $errors ($state): $(echo "$out" | tail -1)"
    [ "$state" = "UNREACHABLE" ] && [ "$errors" -ge 6 ] && finish "session unreachable"
    [ "$errors" -ge "$MAX_ERRORS" ] && finish "too many poll errors"
    sleep 60
  fi
  echo "$out" | grep -q "STATE DONE" && finish "queue done"
  echo "$out" | grep -q "STATE FAILED" && finish "queue failed: $(echo "$out" | tail -1)"
  case "${state:-}" in DONE) finish "queue done";; FAILED) finish "queue failed";; esac
  state=""
done
