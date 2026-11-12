#!/bin/bash
# Like orchestrate.sh, but after starting the queue it hands over to watch_ls.sh, which keeps the
# kernel busy with one long cell and polls only through the contents API (robust to websocket drops).
# usage: deploy/colab/orchestrate_ls.sh <session-name> <plan-file> <code-archive.tar.gz> <out-dir>
SESSION=$1; PLAN=$2; ARCHIVE=$3; OUT=$4
GPU=${COLAB_GPU:-A100}; MAX_ALLOC_TRIES=${MAX_ALLOC_TRIES:-600}
mkdir -p "$OUT"; LOG="$OUT/orchestrate.log"
HERE=$(cd "$(dirname "$0")" && pwd)
log(){ echo "$(date '+%F %T') [$SESSION] $*" | tee -a "$LOG"; }

remote(){
  python3 - "$1" <<'PY' | colab exec -s "$SESSION" --timeout "${2:-120}" 2>&1
import sys, json
print("import subprocess")
print("r = subprocess.run(%s, shell=True, capture_output=True, text=True, executable='/bin/bash')" % json.dumps(sys.argv[1]))
print("print(r.stdout + r.stderr)")
PY
}

for i in $(seq 1 "$MAX_ALLOC_TRIES"); do
  if colab new -s "$SESSION" --gpu "$GPU" >> "$LOG" 2>&1; then log "session ready ($GPU)"; break; fi
  log "allocation attempt $i failed; retrying in 120 s"
  [ "$i" = "$MAX_ALLOC_TRIES" ] && { log "GIVING UP: no $GPU capacity"; exit 1; }
  sleep 120
done

colab upload -s "$SESSION" "$ARCHIVE" /content/tlcn.tar.gz >> "$LOG" 2>&1 || { log "upload failed"; colab stop -s "$SESSION"; exit 1; }
colab upload -s "$SESSION" "$PLAN" /content/plan.txt >> "$LOG" 2>&1 || { log "plan upload failed"; colab stop -s "$SESSION"; exit 1; }
for attempt in 1 2 3; do
  remote 'mkdir -p /content/tlcn /content/runs && tar xzf /content/tlcn.tar.gz -C /content/tlcn && chmod +x /content/tlcn/deploy/colab/*.sh
setsid nohup bash /content/tlcn/deploy/colab/run_plan.sh /content/plan.txt < /dev/null > /content/run_plan.out 2>&1 &
sleep 2; cat /content/tlcn/GIT_COMMIT; nvidia-smi --query-gpu=name --format=csv,noheader' 120 >> "$LOG"
  sleep 20
  if colab ls -s "$SESSION" /content 2>/dev/null | grep -q '^queue.log'; then log "queue started"; break; fi
  log "queue did not start (attempt $attempt)"
  [ "$attempt" = 3 ] && { log "FAILED to start queue; stopping session"; colab stop -s "$SESSION" >> "$LOG" 2>&1; exit 1; }
done
exec bash "$HERE/watch_ls.sh" "$SESSION" "$OUT"
