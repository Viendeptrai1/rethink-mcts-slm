#!/bin/bash
# Re-attach to a running session when the kernel websocket is unreliable.
# 1. Submits ONE long cell that keeps the kernel busy (Colab reclaims idle kernels) until the queue
#    finishes or MAX_HOURS pass, writing /content/heartbeat every minute. The kernel keeps running
#    the cell even if this client's connection drops.
# 2. Polls only through the contents API (`colab ls`), which does not need the kernel.
# 3. When the queue is done/failed (run_plan.sh has already packed results.tar.gz) or the time cap
#    passes, downloads results and logs and stops the session.
# usage: deploy/colab/watch_ls.sh <session-name> <out-dir>
SESSION=$1; OUT=$2; MAX_HOURS=${MAX_HOURS:-14}
mkdir -p "$OUT"; LOG="$OUT/orchestrate.log"
log(){ echo "$(date '+%F %T') [$SESSION] $*" | tee -a "$LOG"; }

finish(){
  log "collecting results"
  colab download -s "$SESSION" /content/results.tar.gz "$OUT/results.tar.gz" >> "$LOG" 2>&1 || log "download of results.tar.gz failed"
  for f in queue.log setup.log; do colab download -s "$SESSION" /content/$f "$OUT/$f" >> "$LOG" 2>&1; done
  log "stopping session"
  colab stop -s "$SESSION" >> "$LOG" 2>&1 || log "colab stop failed: STOP IT BY HAND"
  log "finished: $1"
  exit 0
}

log "watch_ls attached; submitting keep-busy cell (MAX_HOURS=$MAX_HOURS)"
python3 - "$MAX_HOURS" <<'PY' | colab exec -s "$SESSION" --timeout 60 >> "$LOG" 2>&1
import sys
h = float(sys.argv[1])
print(f'''import os, time
t0 = time.time()
while time.time() - t0 < {h} * 3600:
    if os.path.exists("/content/QUEUE_DONE") or os.path.exists("/content/QUEUE_FAILED"):
        break
    open("/content/heartbeat", "w").write(str(int(time.time())))
    time.sleep(60)
if not (os.path.exists("/content/QUEUE_DONE") or os.path.exists("/content/QUEUE_FAILED")):
    import subprocess
    subprocess.run("cd /content && tar czf /content/results.tar.gz runs *.log; touch /content/WATCH_TIMEOUT", shell=True)
print("keep-busy cell finished")''')
PY
started=$(date +%s); unreachable=0
while true; do
  listing=$(colab ls -s "$SESSION" /content 2>/dev/null)
  if [ -z "$listing" ]; then
    unreachable=$((unreachable+1)); log "contents API unreachable ($unreachable)"
    [ "$unreachable" -ge 6 ] && finish "session unreachable"
  else
    unreachable=0
    echo "$listing" | grep -q '^QUEUE_DONE' && finish "queue done"
    echo "$listing" | grep -q '^QUEUE_FAILED' && finish "queue failed"
    echo "$listing" | grep -q '^WATCH_TIMEOUT' && finish "MAX_HOURS=$MAX_HOURS reached (results packed on the VM)"
  fi
  [ $(( $(date +%s) - started )) -gt $(( MAX_HOURS * 3600 + 1800 )) ] && finish "MAX_HOURS exceeded locally"
  sleep 120
done
