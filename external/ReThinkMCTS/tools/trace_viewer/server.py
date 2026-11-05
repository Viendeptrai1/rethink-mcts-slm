from __future__ import annotations

import json
import mimetypes
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs" / "rethinkmcts"
DATA_ROOT = ROOT / "data"
WEB = Path(__file__).resolve().parent / "web"

_JOB_LOCK = threading.Lock()
_ACTIVE_JOB: dict[str, any] = {
    "status": "idle",  # "idle" | "running" | "completed" | "failed" | "stopped"
    "run": None,
    "model": None,
    "dataset": None,
    "problem": None,
    "start_time": 0.0,
    "end_time": 0.0,
    "current_step": "Sẵn sàng",
    "active_node_id": "root",
    "live_tree": None,
    "events": [],
    "logs": [],
    "error": None,
    "process": None,
}

_DATASET_CACHE: dict[str, list[dict]] = {}


def _json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def get_dataset_problem_catalog(dataset_name: str) -> list[dict]:
    """Return all problems defined in the dataset (164 for HumanEval, 300 for APPS)."""
    dataset_key = dataset_name.lower()
    if dataset_key in _DATASET_CACHE:
        return _DATASET_CACHE[dataset_key]

    catalog = []
    if dataset_key == "humaneval":
        arrow_dir = DATA_ROOT / "humaneval" / "arrow"
        if arrow_dir.is_dir():
            try:
                from datasets import load_from_disk
                ds = load_from_disk(str(arrow_dir))["test"]
                for row in ds:
                    task_id = row["task_id"]
                    pid = task_id.replace("/", "_")
                    catalog.append({
                        "id": pid,
                        "task_id": task_id,
                        "entry_point": row.get("entry_point", ""),
                    })
            except Exception as exc:
                print(f"[trace-viewer] Error loading humaneval catalog: {exc}")
    elif dataset_key == "apps":
        apps_raw = DATA_ROOT / "apps" / "raw" / "test"
        if apps_raw.is_dir():
            for p in sorted(apps_raw.iterdir(), key=lambda x: int(x.name) if x.name.isdigit() else x.name):
                if p.is_dir():
                    meta = _json(p / "metadata.json", {})
                    diff = meta.get("difficulty", "").lower()
                    catalog.append({
                        "id": p.name,
                        "task_id": f"apps/{p.name}",
                        "entry_point": diff,
                        "difficulty": diff,
                    })

    _DATASET_CACHE[dataset_key] = catalog
    return catalog


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
            available_datasets = ["humaneval", "apps"]
            existing_dirs = {d.name for d in model_dir.iterdir() if d.is_dir()}
            all_dataset_names = sorted(existing_dirs.union(available_datasets))

            for d_name in all_dataset_names:
                dataset_dir = model_dir / d_name
                solved_set = set()
                if dataset_dir.is_dir():
                    solved_set = {
                        p.name for p in dataset_dir.iterdir()
                        if p.is_dir() and (p / "events.jsonl").is_file() and (p / "search_summary.json").is_file()
                    }
                    if d_name == "apps":
                        for s in list(solved_set):
                            if s.startswith("apps_"):
                                solved_set.add(s.replace("apps_", ""))
                            else:
                                solved_set.add(f"apps_{s}")

                catalog = get_dataset_problem_catalog(d_name)
                problems = []
                if catalog:
                    for item in catalog:
                        pid = item["id"]
                        is_solved = pid in solved_set or pid.replace("apps_", "") in solved_set
                        status_tag = "[Đã giải] " if is_solved else ""
                        label = f"{status_tag}{item['task_id']}"
                        if item.get("entry_point"):
                            label += f" · [{item['entry_point']}]"
                        problems.append({
                            "id": pid,
                            "label": label,
                            "solved": is_solved,
                            "task_id": item["task_id"],
                            "entry_point": item.get("entry_point", ""),
                        })
                    known_ids = {p["id"] for p in problems}
                    for extra in sorted(solved_set - known_ids):
                        problems.append({
                            "id": extra,
                            "label": f"[Đã giải] {extra}",
                            "solved": True,
                            "task_id": extra,
                            "entry_point": "",
                        })
                elif dataset_dir.is_dir():
                    problems = [
                        {
                            "id": p.name,
                            "label": f"[Đã giải] {p.name}",
                            "solved": True,
                            "task_id": p.name,
                            "entry_point": "",
                        }
                        for p in sorted(dataset_dir.iterdir(), key=lambda p: p.name.lower())
                        if p.is_dir() and (p / "events.jsonl").is_file()
                    ]

                if problems:
                    datasets.append({"name": d_name, "problems": problems})

            if datasets:
                models.append({"name": model_dir.name, "datasets": datasets})
        if models:
            models_data = _json(run_dir / "run_config.json", {})
            result.append({"name": run_dir.name, "models": models, "config": models_data})
    return result


def _get_problem_info(dataset: str, problem_str: str) -> dict:
    try:
        from DataProcess import load_problem as load_problem_data
        pid = problem_str.replace("HumanEval_", "").replace("HumanEval/", "").replace("apps_", "")
        p = load_problem_data(dataset, pid)
        entry_point = p.entry_point or ""
        if not entry_point and dataset.lower() == "apps":
            try:
                num = int(pid)
                meta_path = DATA_ROOT / "apps" / "raw" / "test" / f"{num:04d}" / "metadata.json"
                if meta_path.is_file():
                    meta = _json(meta_path, {})
                    entry_point = meta.get("difficulty", "")
            except ValueError:
                pass
        return {
            "statement": p.statement or "",
            "entry_point": entry_point,
            "starter_code": p.starter_code or "",
        }
    except Exception:
        return {"statement": "", "entry_point": "", "starter_code": ""}


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
    events_file = directory / "events.jsonl"
    if events_file.is_file():
        try:
            for line in events_file.read_text(encoding="utf-8").splitlines():
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

    info = _get_problem_info(dataset, problem)
    entry_point = summary.get("problem", {}).get("entry_point") or info["entry_point"]
    statement = info["statement"]

    solved = bool(events_file.is_file() and (directory / "search_summary.json").is_file() and events)

    return {
        "run": run,
        "model": model,
        "dataset": dataset,
        "problem": problem,
        "solved": solved,
        "statement": statement,
        "entry_point": entry_point,
        "starter_code": info["starter_code"],
        "summary": summary,
        "tree": tree,
        "events": events,
        "candidates": candidates,
    }


def _format_event_desc(e: dict) -> str:
    ev = e.get("event", "")
    if ev == "select":
        return f"Rollout {e.get('rollout', 0) + 1}: Chọn node {e.get('node_id', 'root')}"
    elif ev == "expand":
        nid = e.get("node_id", "root")
        count = len(e.get("children", []))
        return f"Mở rộng {count} nhánh suy luận từ node {nid}"
    elif ev == "llm_request":
        op = e.get("operation", "LLM call")
        tokens = e.get("usage", {}).get("total_tokens", 0)
        m = e.get("model", "")
        if op == "code_generation":
            return f"LLM: Sinh code giải thuật ({tokens} tokens)"
        elif op == "verbal_feedback":
            return f"LLM: Phân tích phản hồi kiểm thử tự động ({tokens} tokens)"
        elif op == "rethink":
            return f"LLM: Tự sửa lỗi / Rethink giả thuyết ({tokens} tokens)"
        elif op == "expand":
            return f"LLM: Khởi tạo các hướng suy luận ({tokens} tokens)"
        return f"LLM [{op}]: {m} ({tokens} tokens)"
    elif ev == "evaluate":
        rew = e.get("reward")
        rew_str = f"{float(rew):.3f}" if rew is not None else "—"
        pass_rate = e.get("public_pass_rate")
        pr_str = f"{float(pass_rate)*100:.1f}%" if pass_rate is not None else "—"
        cid = e.get("candidate_id", "")
        ph = e.get("phase", "eval")
        return f"Đánh giá ({ph}) {cid}: Pass {pr_str} · Reward {rew_str}"
    elif ev == "rethink":
        nid = e.get("node_id", "")
        rep = e.get("replacement", "")
        short_rep = rep[:55] + "…" if len(rep) > 55 else rep
        return f"Rethink ({nid}): {short_rep}"
    elif ev == "rethink_next":
        nid = e.get("node_id", "")
        return f"Chuyển sang nhánh sâu hơn từ node {nid}"
    elif ev == "complete":
        return f"Hoàn tất: Best Candidate {e.get('best_candidate_id')} (Reward {e.get('best_reward')})"
    return e.get("message") or f"Sự kiện: {ev}"


def build_tree_from_events(events: list[dict]) -> tuple[dict, str, dict]:
    root = {
        "node_id": "root",
        "action": "Root problem",
        "prior": 1.0,
        "q_value": 0.0,
        "visit_count": 0,
        "children": [],
        "rethink_count": 0,
        "status": "root",
        "public_pass_rate": None,
        "reward": None,
        "candidate_id": None,
    }
    nodes_map = {"root": root}
    active_node = "root"

    total_tokens = 0
    llm_calls_count = 0
    current_rollout = 0
    best_reward = 0.0
    latest_op = "Khởi tạo"
    candidate_count = 0

    for e in events:
        ev = e.get("event")
        if ev == "llm_request":
            llm_calls_count += 1
            usage = e.get("usage") or {}
            total_tokens += int(usage.get("total_tokens") or 0)
            op = e.get("operation") or ""
            if op == "code_generation":
                latest_op = "Sinh code"
            elif op == "verbal_feedback":
                latest_op = "Phân tích phản hồi test"
            elif op == "rethink":
                latest_op = "Tự sửa lỗi (Rethink)"
            elif op == "expand":
                latest_op = "Mở rộng nhánh"
            else:
                latest_op = op
        elif ev == "select":
            nid = e.get("node_id", "root")
            active_node = nid
            current_rollout = int(e.get("rollout", 0)) + 1
            if nid in nodes_map:
                nodes_map[nid]["visit_count"] = nodes_map[nid].get("visit_count", 0) + 1
                nodes_map[nid]["status"] = "selected"
        elif ev == "expand":
            parent_id = e.get("node_id", "root")
            parent = nodes_map.get(parent_id)
            if parent:
                for c in e.get("children", []):
                    cid = c.get("node_id")
                    if cid and cid not in nodes_map:
                        child_node = {
                            "node_id": cid,
                            "action": c.get("thought", ""),
                            "prior": float(c.get("prior") or 0.0),
                            "q_value": 0.0,
                            "visit_count": 0,
                            "children": [],
                            "rethink_count": 0,
                            "parent_id": parent_id,
                            "status": "unvisited",
                            "public_pass_rate": None,
                            "reward": None,
                            "candidate_id": None,
                        }
                        parent["children"].append(child_node)
                        nodes_map[cid] = child_node
        elif ev == "evaluate":
            candidate_count += 1
            nid = e.get("node_id", "root")
            rew = float(e.get("reward") or 0.0)
            pass_rate = float(e.get("public_pass_rate") or 0.0)
            cid = e.get("candidate_id")
            if rew > best_reward:
                best_reward = rew
            if nid in nodes_map:
                n = nodes_map[nid]
                n["candidate_id"] = cid
                n["public_pass_rate"] = pass_rate
                n["reward"] = rew
                n["status"] = "evaluated"
                curr_id = nid
                while curr_id:
                    curr_node = nodes_map[curr_id]
                    curr_node["q_value"] = max(curr_node.get("q_value", 0.0), rew)
                    curr_id = curr_node.get("parent_id")
        elif ev == "rethink":
            nid = e.get("node_id")
            if nid in nodes_map:
                if e.get("replacement"):
                    nodes_map[nid]["action"] = e.get("replacement")
                nodes_map[nid]["rethink_count"] = nodes_map[nid].get("rethink_count", 0) + 1
                nodes_map[nid]["status"] = "rethinking"
        elif ev == "complete":
            if e.get("best_reward") is not None:
                best_reward = float(e.get("best_reward"))

    def get_depth(n, d=0):
        if not n.get("children"):
            return d
        return max(get_depth(c, d + 1) for c in n["children"])

    stats = {
        "total_nodes": len(nodes_map),
        "max_depth": get_depth(root),
        "llm_requests": llm_calls_count,
        "total_tokens": total_tokens,
        "current_rollout": max(1, current_rollout),
        "best_reward": round(best_reward, 3),
        "candidate_count": candidate_count,
        "latest_op": latest_op,
    }

    return root, active_node, stats


def _run_mcts_job(dataset: str, pid: str, run: str, model_arg: str, rollouts: int, problem_raw: str) -> None:
    safe_model = model_arg.replace(":", "_")
    target_problem_dir = f"{int(pid):04d}" if dataset == "apps" else f"HumanEval_{pid}"
    target_dir = OUTPUTS / run / safe_model / dataset / target_problem_dir
    events_file = target_dir / "events.jsonl"

    # Pre-clean prior artifacts so a fresh job starts clean
    if target_dir.is_dir():
        for fname in ["events.jsonl", "search_summary.json", "final_solution.py", "tree.json"]:
            p = target_dir / fname
            if p.is_file():
                try:
                    p.unlink()
                except OSError:
                    pass
    
    cmd = [
        sys.executable,
        "-u",
        "-m", "rethinkmcts",
        "--dataset", dataset,
        "--problem-id", pid,
        "--run-name", run,
        "--model", model_arg,
        "--rollouts", str(rollouts),
    ]
    print(f"[trace-viewer] Starting MCTS job: {' '.join(cmd)}")

    max_duration = 1200.0  # 20 minutes timeout for local inference
    start_t = time.time()

    # Initialize tree with root
    with _JOB_LOCK:
        _ACTIVE_JOB["live_tree"] = {
            "node_id": "root",
            "action": "Root problem",
            "prior": 1.0,
            "q_value": 0.0,
            "visit_count": 0,
            "children": [],
            "rethink_count": 0,
        }
        _ACTIVE_JOB["active_node_id"] = "root"
        _ACTIVE_JOB["current_step"] = "Đang khởi tạo root node và môi trường MCTS..."
        _ACTIVE_JOB["stats"] = {
            "total_nodes": 1,
            "max_depth": 0,
            "llm_requests": 0,
            "total_tokens": 0,
            "current_rollout": 1,
            "best_reward": 0.0,
            "candidate_count": 0,
            "latest_op": "Khởi tạo",
        }

    try:
        proc = subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        with _JOB_LOCK:
            _ACTIVE_JOB["process"] = proc

        # Background daemon thread to read stdout asynchronously without blocking
        def _stream_stdout():
            if not proc.stdout:
                return
            for raw_line in iter(proc.stdout.readline, ""):
                line_str = raw_line.strip()
                if line_str:
                    with _JOB_LOCK:
                        _ACTIVE_JOB["logs"].append(line_str)
                        if len(_ACTIVE_JOB["logs"]) > 50:
                            _ACTIVE_JOB["logs"].pop(0)
            try:
                proc.stdout.close()
            except Exception:
                pass

        t_reader = threading.Thread(target=_stream_stdout, daemon=True)
        t_reader.start()

        while True:
            ret = proc.poll()

            # Read dynamic events from events.jsonl and rebuild live tree
            if events_file.is_file():
                try:
                    all_lines = events_file.read_text(encoding="utf-8").splitlines()
                    raw_events = []
                    for l in all_lines:
                        l = l.strip()
                        if l:
                            try:
                                raw_events.append(json.loads(l))
                            except Exception:
                                pass

                    if raw_events:
                        live_tree, active_nid, stats = build_tree_from_events(raw_events)
                        formatted_events = [
                            {
                                "time": time.strftime("%H:%M:%S"),
                                "event": ev.get("event", "event"),
                                "node_id": ev.get("node_id"),
                                "desc": _format_event_desc(ev),
                                "phase": ev.get("phase"),
                                "candidate_id": ev.get("candidate_id"),
                            }
                            for ev in raw_events
                        ]
                        with _JOB_LOCK:
                            _ACTIVE_JOB["live_tree"] = live_tree
                            _ACTIVE_JOB["active_node_id"] = active_nid
                            _ACTIVE_JOB["events"] = formatted_events
                            _ACTIVE_JOB["stats"] = stats
                            if formatted_events:
                                _ACTIVE_JOB["current_step"] = formatted_events[-1]["desc"]
                except Exception:
                    pass

            if ret is not None:
                if ret == 0:
                    with _JOB_LOCK:
                        _ACTIVE_JOB["status"] = "completed"
                        _ACTIVE_JOB["end_time"] = time.time()
                        _ACTIVE_JOB["current_step"] = "Hoàn tất giải thuật MCTS thành công."
                else:
                    err_snippet = "\n".join(_ACTIVE_JOB["logs"][-8:])
                    with _JOB_LOCK:
                        _ACTIVE_JOB["status"] = "failed"
                        _ACTIVE_JOB["end_time"] = time.time()
                        _ACTIVE_JOB["error"] = f"Tiến trình kết thúc với mã lỗi {ret}.\n{err_snippet}"
                break

            if time.time() - start_t > max_duration:
                proc.kill()
                with _JOB_LOCK:
                    _ACTIVE_JOB["status"] = "failed"
                    _ACTIVE_JOB["end_time"] = time.time()
                    _ACTIVE_JOB["error"] = f"Tiến trình vượt quá thời gian tối đa ({int(max_duration)}s). Đã dừng an toàn."
                break

            time.sleep(0.4)

    except Exception as exc:
        with _JOB_LOCK:
            _ACTIVE_JOB["status"] = "failed"
            _ACTIVE_JOB["end_time"] = time.time()
            _ACTIVE_JOB["error"] = f"Lỗi hệ thống: {exc}"
    finally:
        with _JOB_LOCK:
            _ACTIVE_JOB["process"] = None


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
            self._send(json.dumps(list_runs(), ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
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
        if url.path == "/api/solve/status":
            with _JOB_LOCK:
                st = _ACTIVE_JOB["status"]
                start = _ACTIVE_JOB["start_time"]
                end = _ACTIVE_JOB["end_time"] or time.time()
                elapsed = round(end - start, 1) if start > 0 else 0.0
                resp = {
                    "status": st,
                    "run": _ACTIVE_JOB["run"],
                    "model": _ACTIVE_JOB["model"],
                    "dataset": _ACTIVE_JOB["dataset"],
                    "problem": _ACTIVE_JOB["problem"],
                    "elapsed_seconds": elapsed,
                    "current_step": _ACTIVE_JOB["current_step"],
                    "active_node_id": _ACTIVE_JOB.get("active_node_id", "root"),
                    "live_tree": _ACTIVE_JOB.get("live_tree"),
                    "stats": _ACTIVE_JOB.get("stats", {}),
                    "events": _ACTIVE_JOB["events"],
                    "logs": _ACTIVE_JOB["logs"][-15:],
                    "error": _ACTIVE_JOB["error"],
                }
            self._send(json.dumps(resp, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", 200)
            return

        relative = "index.html" if url.path in {"/", "/index.html"} else url.path.lstrip("/")
        target = (WEB / relative).resolve()
        if not target.is_relative_to(WEB.resolve()) or not target.is_file():
            self._send(b"Not found", "text/plain", 404)
            return
        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self._send(target.read_bytes(), f"{mime}; charset=utf-8")

    def do_POST(self) -> None:
        url = urlparse(self.path)
        if url.path == "/api/solve":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
            except Exception:
                self._send(json.dumps({"error": "Invalid JSON body"}).encode(), "application/json", 400)
                return

            dataset = data.get("dataset", "humaneval")
            problem = data.get("problem", "")
            run = data.get("run", "demo_ollama")
            model = data.get("model", "")
            rollouts = int(data.get("rollouts", 3))

            if not problem or ".." in problem or "/" in problem:
                self._send(json.dumps({"error": "Tên bài toán không hợp lệ"}).encode(), "application/json", 400)
                return

            pid = problem.replace("HumanEval_", "").replace("HumanEval/", "").replace("apps_", "")

            with _JOB_LOCK:
                if _ACTIVE_JOB["status"] == "running":
                    self._send(
                        json.dumps({"error": "Một tiến trình MCTS đang chạy. Vui lòng đợi hoặc bấm Dừng tiến trình."}).encode("utf-8"),
                        "application/json; charset=utf-8",
                        409,
                    )
                    return

                model_arg = model.replace("_", ":") if model and model != "configured-model" else "qwen2.5-coder:7b"
                _ACTIVE_JOB["status"] = "running"
                _ACTIVE_JOB["run"] = run
                _ACTIVE_JOB["model"] = model_arg
                _ACTIVE_JOB["dataset"] = dataset
                _ACTIVE_JOB["problem"] = problem
                _ACTIVE_JOB["start_time"] = time.time()
                _ACTIVE_JOB["end_time"] = 0.0
                _ACTIVE_JOB["current_step"] = f"Khởi động tiến trình MCTS cho {dataset}/{pid}..."
                _ACTIVE_JOB["active_node_id"] = "root"
                _ACTIVE_JOB["live_tree"] = {
                    "node_id": "root",
                    "action": "Root problem",
                    "prior": 1.0,
                    "q_value": 0.0,
                    "visit_count": 0,
                    "children": [],
                    "rethink_count": 0,
                }
                _ACTIVE_JOB["events"] = []
                _ACTIVE_JOB["logs"] = []
                _ACTIVE_JOB["error"] = None
                _ACTIVE_JOB["process"] = None

            thread = threading.Thread(
                target=_run_mcts_job,
                args=(dataset, pid, run, model_arg, rollouts, problem),
                daemon=True,
            )
            thread.start()

            self._send(
                json.dumps({
                    "success": True,
                    "message": f"Đã bắt đầu tiến trình giải {problem}",
                    "job": {
                        "dataset": dataset,
                        "problem": problem,
                        "run": run,
                        "model": model_arg,
                    }
                }).encode("utf-8"),
                "application/json; charset=utf-8",
                200,
            )
            return

        if url.path == "/api/solve/stop":
            with _JOB_LOCK:
                proc = _ACTIVE_JOB.get("process")
                if proc and _ACTIVE_JOB["status"] == "running":
                    proc.kill()
                    _ACTIVE_JOB["status"] = "stopped"
                    _ACTIVE_JOB["end_time"] = time.time()
                    _ACTIVE_JOB["current_step"] = "Người dùng đã dừng tiến trình."
                    _ACTIVE_JOB["error"] = "Tiến trình đã được dừng theo yêu cầu."
                    self._send(json.dumps({"success": True, "message": "Đã dừng tiến trình"}).encode("utf-8"), "application/json; charset=utf-8", 200)
                    return
                else:
                    self._send(json.dumps({"error": "Không có tiến trình nào đang chạy"}).encode("utf-8"), "application/json; charset=utf-8", 400)
                    return

        self._send(b"Not found", "text/plain", 404)

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
