#!/bin/bash
# Safety net next to a session's watcher: every INTERVAL seconds, pack the runs on the VM over
# `colab ssh` (does not need the kernel) and download them to <out-dir>/partial.tar.gz, so a VM
# that disappears loses at most one interval of work. Logs "SESSION LOST" if the session vanishes.
# Waits for the session's queue to start; exits when the queue is done/failed or the session is lost.
# usage: deploy/colab/guard.sh <session-name> <out-dir>
SESSION=$1; OUT=$2; INTERVAL=${INTERVAL:-1200}
KEY=${COLAB_SSH_KEY:-$HOME/.config/colab-cli/colab_ssh_ed25519}
LOG="$OUT/orchestrate.log"; mkdir -p "$OUT"
log(){ echo "$(date '+%F %T') [$SESSION] guard: $*" >> "$LOG"; }
started=0
while true; do
  listing=$(colab ls -s "$SESSION" /content 2>&1)
  if echo "$listing" | grep -q "not found"; then
    [ "$started" = 1 ] && { log "SESSION LOST (runtime no longer exists); last partial kept in $OUT"; exit 1; }
    sleep 120; continue   # not allocated yet
  fi
  echo "$listing" | grep -q '^queue.log' || { sleep 120; continue; }
  started=1
  echo "$listing" | grep -qE '^QUEUE_(DONE|FAILED)' && { log "queue finished; guard exits"; exit 0; }
  if colab ssh -s "$SESSION" -i "$KEY" -- 'cd /content && tar czf /content/partial.tar.gz.tmp runs *.log 2>/dev/null; mv /content/partial.tar.gz.tmp /content/partial.tar.gz' >/dev/null 2>&1 \
     && colab download -s "$SESSION" /content/partial.tar.gz "$OUT/partial.tar.gz.tmp" >/dev/null 2>&1; then
    mv "$OUT/partial.tar.gz.tmp" "$OUT/partial.tar.gz"
    log "partial saved ($(du -h "$OUT/partial.tar.gz" | cut -f1))"
  else
    log "partial save failed"
  fi
  sleep "$INTERVAL"
done
