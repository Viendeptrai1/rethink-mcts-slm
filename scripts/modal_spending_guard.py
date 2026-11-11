#!/usr/bin/env python3
"""
Modal Real-time Spending Guard / Circuit Breaker.
Monitors the Modal billing API continuously. If the monthly credit usage
reaches the safety threshold ($26.50 / $30.00), it immediately shuts down
the GPU app and kills running benchmark processes to prevent any credit card charge.
"""

import os
import sys
import time
import toml
import asyncio
import datetime
import subprocess
from pathlib import Path
from modal_proto import api_pb2
import modal.client

PROFILE = os.environ.get("MODAL_PROFILE", "vienphanquoc-123")
MAX_CREDIT_USAGE_DOLLARS = float(os.environ.get("MODAL_MAX_CREDIT", "27.00"))  # Hard safety cap at $27.00
CHECK_INTERVAL_SECONDS = int(os.environ.get("MODAL_GUARD_INTERVAL", "60"))
APP_TO_STOP = os.environ.get("MODAL_APP_NAME", "rethink-vllm")
# Billing data can lag; also stop after this many hours of wall clock since the guard started.
MAX_HOURS = float(os.environ.get("MODAL_MAX_HOURS", "0")) or None

def log(msg: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [SpendingGuard] {msg}", flush=True)

async def get_current_spend(creds: dict):
    c = await modal.client._Client.from_credentials(creds['token_id'], creds['token_secret'])
    dt = datetime.datetime(2026, 11, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    req = api_pb2.WorkspaceBillingSummaryRequest()
    req.start_timestamp.FromDatetime(dt)
    resp = await c.stub.WorkspaceBillingSummary(req)
    
    metered = float(resp.metered_cost)
    billed = float(resp.billed_cost)
    adj = dict(resp.adjustments)
    credit_applied = abs(float(adj.get('Credits', '0')))
    return metered, billed, credit_applied

def emergency_shutdown():
    log("🚨 EMERGENCY SHUTDOWN TRIGGERED! Stopping Modal apps and benchmark processes...")
    # Stop Modal app
    try:
        subprocess.run(["modal", "app", "stop", APP_TO_STOP], 
                       env=dict(os.environ, MODAL_PROFILE=PROFILE),
                       capture_output=True, text=True, timeout=30)
        log(f"✅ Modal app '{APP_TO_STOP}' stopped.")
    except Exception as e:
        log(f"⚠️ Failed to stop modal app: {e}")

    # Kill running benchmark batch processes
    try:
        subprocess.run(["pkill", "-f", "run_benchmark_batch.py"], capture_output=True, timeout=10)
        log("✅ Killed local benchmark runner processes.")
    except Exception as e:
        log(f"⚠️ Failed to kill benchmark process: {e}")

async def main():
    cfg_path = Path.home() / ".modal.toml"
    if not cfg_path.exists():
        log(f"Config file {cfg_path} not found.")
        return

    cfg = toml.load(cfg_path)
    if PROFILE not in cfg:
        log(f"Profile {PROFILE} not found in {cfg_path}.")
        return

    creds = cfg[PROFILE]
    log(f"Starting Spending Guard for profile [{PROFILE}]...")
    log(f"Threshold: Max \${MAX_CREDIT_USAGE_DOLLARS:.2f} / \${30.00:.2f} free credits (Safety buffer: \${30.00 - MAX_CREDIT_USAGE_DOLLARS:.2f}).")

    started = time.time()
    while True:
        if MAX_HOURS and time.time() - started >= MAX_HOURS * 3600:
            log(f"CRITICAL: wall-clock cap of {MAX_HOURS:.1f}h reached.")
            emergency_shutdown()
            break
        try:
            metered, billed, credit_used = await get_current_spend(creds)
            buffer_left = 30.0 - credit_used
            log(f"Check: Metered=\${metered:.2f} | Credit Used=\${credit_used:.2f} | Buffer Left=\${buffer_left:.2f} | Billed=\${billed:.2f}")

            if credit_used >= MAX_CREDIT_USAGE_DOLLARS:
                log(f"CRITICAL: Credit usage (\${credit_used:.2f}) reached or exceeded limit (\${MAX_CREDIT_USAGE_DOLLARS:.2f})!")
                emergency_shutdown()
                break

            if billed > 0.0:
                log(f"CRITICAL: Non-zero billed amount detected (\${billed:.2f})!")
                emergency_shutdown()
                break

        except Exception as e:
            log(f"Error checking billing: {e}")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())

