#!/bin/bash
# Like the archived guard.sh, but never opens `colab ssh`: a packer loop on the VM (started by orchestrate_ls.sh)
# rewrites /content/partial.tar.gz atomically every ~5 min, and this guard only downloads it through
# the contents API. Introduced after three runtimes vanished within ~2 min of a guard.sh ssh save
# (13/11/2026, 01:49, 02:21, 02:47). Later losses (02:57, 03:13, 03:21) happened without ssh, one
# without any download, and the CLI sent no unassign: Colab reclaims runtimes server-side.
# usage: deploy/colab/guard_dl.sh <session-name> <out-dir>
SESSION=$1; OUT=$2; INTERVAL=${INTERVAL:-1200}
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
  if echo "$listing" | grep -qx 'partial.tar.gz'; then
    if colab download -s "$SESSION" /content/partial.tar.gz "$OUT/partial.tar.gz.tmp" >/dev/null 2>&1 \
       && tar tzf "$OUT/partial.tar.gz.tmp" >/dev/null 2>&1; then
      mv "$OUT/partial.tar.gz.tmp" "$OUT/partial.tar.gz"
      log "partial saved ($(du -h "$OUT/partial.tar.gz" | cut -f1), no ssh)"
    else
      log "partial save failed"
    fi
  fi
  sleep "$INTERVAL"
done
