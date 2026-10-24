from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs" / "rethinkmcts"
WEB = Path(__file__).resolve().parent / "web"


def _json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def list_runs() -> list[dict]:
    result = []
    if not OUTPUTS.exists():
        return result
    for run_dir in sorted(OUTPUTS.iterdir(), key=lambda p: p.name.lower()):
        if not run_dir.is_dir():
            continue
        models = []
        for model_dir in sorted(run_dir.iterdir(), key=lambda p: p.name.lower()):
            if not model_dir.is_dir():
                continue
            datasets = []
            for dataset_dir in sorted(model_dir.iterdir(), key=lambda p: p.name.lower()):
                if not dataset_dir.is_dir():
                    continue
                problems = [
                    p.name for p in sorted(dataset_dir.iterdir(), key=lambda p: p.name.lower())
                    if p.is_dir() and (p / "events.jsonl").is_file()
                ]
                if problems:
                    datasets.append({"name": dataset_dir.name, "problems": problems})
            if datasets:
                models.append({"name": model_dir.name, "datasets": datasets})
        if models:
            models_data = _json(run_dir / "run_config.json", {})
            result.append({"name": run_dir.name, "models": models, "config": models_data})
    return result


def load_problem(run: str, model: str, dataset: str, problem: str) -> dict:
    parts = (run, model, dataset, problem)
    if any(not isinstance(value, str) or not value or value in {".", ".."}
           or "/" in value or "\\" in value for value in parts):
        raise ValueError("Invalid artifact path")
    directory = (OUTPUTS / run / model / dataset / problem).resolve()
    if not directory.is_relative_to(OUTPUTS.resolve()):
        raise ValueError("Artifact path is outside the RethinkMCTS output directory")
    summary = _json(directory / "search_summary.json", {})
    tree = _json(directory / "tree.json", {})
    events = []
    try:
        for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    events.append({"event": "invalid_event", "raw": line})
    except OSError:
        pass
    candidates = []
    candidate_dir = directory / "candidates"
    if candidate_dir.is_dir():
        for path in sorted(candidate_dir.iterdir(), key=lambda p: p.name):
            if path.is_dir():
                metadata = _json(path / "metadata.json", {})
                candidates.append({
                    "id": path.name,
                    "metadata": metadata,
                    "solution": _read_text(path / "solution.py"),
                    "response": _read_text(path / "response.txt"),
                    "execution": _json(path / "execution.json", {}),
                    "feedback": _json(path / "feedback.json", {}),
                })
    return {"run": run, "model": model, "dataset": dataset, "problem": problem,
            "summary": summary, "tree": tree, "events": events, "candidates": candidates}


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        url = urlparse(self.path)
        if url.path == "/api/runs":
            self._send(json.dumps(list_runs()).encode(), "application/json; charset=utf-8")
            return
        if url.path == "/api/problem":
            query = parse_qs(url.query)
            try:
                payload = load_problem(*(query.get(key, [""])[0] for key in
                                         ("run", "model", "dataset", "problem")))
            except (ValueError, OSError) as exc:
                self._send(json.dumps({"error": str(exc)}).encode(), "application/json", 400)
                return
            self._send(json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8")
            return
        relative = "index.html" if url.path in {"/", "/index.html"} else url.path.lstrip("/")
        target = (WEB / relative).resolve()
        if not target.is_relative_to(WEB.resolve()) or not target.is_file():
            self._send(b"Not found", "text/plain", 404)
            return
        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self._send(target.read_bytes(), f"{mime}; charset=utf-8")

    def log_message(self, fmt: str, *args) -> None:
        print("[trace-viewer] " + fmt % args)


def main() -> None:
    if not OUTPUTS.exists():
        raise SystemExit(f"RethinkMCTS artifacts not found: {OUTPUTS}")
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("RethinkMCTS trace viewer: http://127.0.0.1:8765")
    print(f"Reading artifacts from: {OUTPUTS}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping trace viewer.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
