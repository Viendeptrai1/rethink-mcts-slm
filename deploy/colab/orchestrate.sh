#!/bin/bash
# Local driver for one Colab session (runs on the user's machine, needs the `colab` CLI logged in).
# usage: deploy/colab/orchestrate.sh <session-name> <plan-file> <code-archive.tar.gz> <out-dir>
#
# 1. Allocates an A100 session (retries while Colab has no capacity).
# 2. Uploads the code archive and the plan, starts deploy/colab/run_plan.sh detached on the VM.
# 3. Keeps the kernel busy (Colab reclaims runtimes whose kernel is idle) and polls the queue.
# 4. When the queue is done or failed (or the session is lost), downloads results.tar.gz and
#    the logs into <out-dir>, then stops the session so it stops consuming compute units.
SESSION=$1; PLAN=$2; ARCHIVE=$3; OUT=$4
GPU=${COLAB_GPU:-A100}; MAX_ALLOC_TRIES=${MAX_ALLOC_TRIES:-60}
mkdir -p "$OUT"; LOG="$OUT/orchestrate.log"
log(){ echo "$(date '+%F %T') [$SESSION] $*" | tee -a "$LOG"; }

remote(){ # run a shell command on the VM through the kernel; $2 = exec timeout seconds
  python3 - "$1" <<'PY' | colab exec -s "$SESSION" --timeout "${2:-120}" 2>&1
import sys, json
print("import subprocess")
print("r = subprocess.run(%s, shell=True, capture_output=True, text=True, executable='/bin/bash')" % json.dumps(sys.argv[1]))
print("print(r.stdout + r.stderr)")
PY
}

finish(){
  log "collecting results"
  colab download -s "$SESSION" /content/results.tar.gz "$OUT/results.tar.gz" >> "$LOG" 2>&1 || log "download of results.tar.gz failed"
  for f in queue.log setup.log; do colab download -s "$SESSION" /content/$f "$OUT/$f" >> "$LOG" 2>&1; done
  log "stopping session"
  colab stop -s "$SESSION" >> "$LOG" 2>&1 || log "colab stop failed: STOP IT BY HAND"
  log "finished: $1"
  exit 0
}

# 1. allocate
for i in $(seq 1 "$MAX_ALLOC_TRIES"); do
  if colab new -s "$SESSION" --gpu "$GPU" >> "$LOG" 2>&1; then log "session ready ($GPU)"; break; fi
  log "allocation attempt $i failed; retrying in 120 s"
  [ "$i" = "$MAX_ALLOC_TRIES" ] && { log "GIVING UP: no $GPU capacity"; exit 1; }
  sleep 120
done

# 2. upload and start
colab upload -s "$SESSION" "$ARCHIVE" /content/tlcn.tar.gz >> "$LOG" 2>&1 || finish "upload failed"
colab upload -s "$SESSION" "$PLAN" /content/plan.txt >> "$LOG" 2>&1 || finish "plan upload failed"
remote 'mkdir -p /content/tlcn /content/runs && tar xzf /content/tlcn.tar.gz -C /content/tlcn && chmod +x /content/tlcn/deploy/colab/*.sh
setsid nohup bash /content/tlcn/deploy/colab/run_plan.sh /content/plan.txt < /dev/null > /content/run_plan.out 2>&1 &
sleep 2; cat /content/tlcn/GIT_COMMIT; nvidia-smi --query-gpu=name --format=csv,noheader' 120 >> "$LOG"
log "queue started"

# 3. keep the kernel busy and poll
errors=0
while true; do
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
    echo "$out" | grep -q "STATE DONE" && finish "queue done"
    echo "$out" | grep -q "STATE FAILED" && finish "queue failed: $(echo "$out" | tail -1)"
  else
    errors=$((errors+1)); log "poll error $errors: $(echo "$out" | tail -1)"
    [ "$errors" -ge 6 ] && finish "session unreachable (lost or reclaimed?)"
    sleep 60
  fi
done
