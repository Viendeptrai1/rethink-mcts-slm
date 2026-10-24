from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "baselines/direct_generation/configs/qwen25_coder_7b_instruct.json"
DEFAULT_MODEL = "qwen2.5-coder:7b-instruct"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open a private SSH tunnel, pull the Ollama model if needed, then generate code locally"
    )
    parser.add_argument("--ssh-host", required=True)
    parser.add_argument("--ssh-port", type=int, required=True)
    parser.add_argument("--ssh-user", default="root")
    parser.add_argument("--dataset", choices=("apps", "humaneval", "all"), required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--generation-workers", type=int, default=1)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--confirm-full-run", action="store_true")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]*", args.ssh_host):
        parser.error("--ssh-host must be a hostname or IPv4 address")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", args.ssh_user):
        parser.error("--ssh-user contains invalid characters")
    if not 1 <= args.ssh_port <= 65535:
        parser.error("--ssh-port must be between 1 and 65535")
    if args.generation_workers < 1 or args.delay < 0:
        parser.error("workers must be positive and delay cannot be negative")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if not args.plan and args.limit is None and not args.confirm_full_run:
        parser.error("Choose --limit for a smoke run or --confirm-full-run for the full dataset")
    if not args.config.is_file():
        parser.error(f"Config not found: {args.config}")
    return args


def pipeline_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable, "-m", "pipelines", "--stage", "generate",
        "--dataset", args.dataset, "--run-name", args.run_name,
        "--model", args.model, "--config", str(args.config.resolve()),
        "--generation-workers", str(args.generation_workers),
        "--delay", str(args.delay),
    ]
    if args.limit is not None:
        command.extend(("--limit", str(args.limit)))
    if args.plan:
        command.append("--plan")
    if args.confirm_full_run:
        command.append("--confirm-full-run")
    return command


def _free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _models(base_url: str) -> set[str]:
    with urlopen(f"{base_url}/api/tags", timeout=10) as response:
        payload = json.load(response)
    return {
        str(item.get("name") or item.get("model"))
        for item in payload.get("models", [])
        if item.get("name") or item.get("model")
    }


def _wait_for_server(base_url: str, tunnel: subprocess.Popen, *, seconds: float = 120) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if tunnel.poll() is not None:
            raise RuntimeError(f"SSH tunnel stopped before Ollama became ready (exit {tunnel.returncode})")
        try:
            _models(base_url)
            return
        except (OSError, URLError, ValueError):
            time.sleep(1)
    raise TimeoutError("Ollama did not answer through the SSH tunnel within 120 seconds")


def _pull_model(base_url: str, model: str) -> None:
    request = Request(
        f"{base_url}/api/pull",
        data=json.dumps({"model": model, "stream": True}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    print(f"Model {model} is missing on the rented GPU; downloading now...", flush=True)
    last_status = None
    last_percent = -1
    with urlopen(request, timeout=600) as response:
        for line in response:
            if not line.strip():
                continue
            progress = json.loads(line)
            if progress.get("error"):
                raise RuntimeError(f"Ollama pull failed: {progress['error']}")
            status = str(progress.get("status", ""))
            total = progress.get("total") or 0
            percent = int(100 * progress.get("completed", 0) / total) if total else -1
            if status != last_status or (percent >= 0 and percent // 10 != last_percent // 10):
                print(f"Ollama: {status}" + (f" {percent}%" if percent >= 0 else ""), flush=True)
                last_status, last_percent = status, percent
    if model not in _models(base_url):
        raise RuntimeError(f"Ollama pull ended, but {model} is still absent from /api/tags")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    command = pipeline_command(args)
    if args.plan:
        return subprocess.run(command, cwd=ROOT, check=False).returncode

    port = _free_port()
    base_url = f"http://127.0.0.1:{port}"
    ssh_command = [
        "ssh", "-o", "ExitOnForwardFailure=yes", "-o", "ServerAliveInterval=30",
        "-o", "ServerAliveCountMax=3", "-N", "-L",
        f"127.0.0.1:{port}:127.0.0.1:11434", "-p", str(args.ssh_port),
        f"{args.ssh_user}@{args.ssh_host}",
    ]
    print("Opening SSH tunnel; enter the SSH password if prompted.", flush=True)
    tunnel = subprocess.Popen(ssh_command)
    try:
        _wait_for_server(base_url, tunnel)
        if args.model not in _models(base_url):
            _pull_model(base_url, args.model)
        else:
            print(f"Model {args.model} is already present; skipping download.", flush=True)
        env = os.environ.copy()
        env.update({
            "LLM_PROVIDER": "ollama", "LLM_MODEL": args.model,
            "LLM_BASE_URL": f"{base_url}/v1", "LLM_API_KEY": "ollama",
        })
        return subprocess.run(command, cwd=ROOT, env=env, check=False).returncode
    finally:
        tunnel.terminate()
        try:
            tunnel.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tunnel.kill()
            tunnel.wait()


if __name__ == "__main__":
    raise SystemExit(main())
