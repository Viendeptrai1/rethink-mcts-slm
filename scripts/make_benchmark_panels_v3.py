"""Tách Bảng 4.1 thành các biểu đồ nhỏ, không gọi model hoặc chấm lại code.

Chạy: python scripts/make_benchmark_panels_v3.py
Dữ liệu: docs/results/v3/, cohort APPS và artifact của các run v3.
Hình: docs/report/figures/v3/table41/ (PNG 300 dpi và PDF vector).
"""

import json
import math
import tarfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "docs/results/v3"
OUT = ROOT / "docs/report/figures/v3/table41"
MODELS = [
    ("qwen25c7b", "Qwen2.5-Coder-7B"),
    ("seedcoder8b", "Seed-Coder-8B"),
    ("qwen35_9b", "Qwen3.5-9B"),
]
# Palette figures4papers; hatch giúp phân biệt Test-only khi in đen trắng.
METHODS = [
    ("direct", "Direct", "#CFCECE", ""),
    ("bon16", "Best-of-16", "#B64342", ""),
    ("mcts", "MCTS Dual", "#0F4D92", ""),
    ("test_only", "MCTS Test-only", "#8BCF8B", "//"),
]
LEVELS = ["introductory", "interview", "competition"]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def public_passing_candidates(run, pids):
    """Đọc evaluations có sẵn; stream archive nặng thay vì giải nén ra ổ đĩa."""
    passing = {}
    for pid in pids:
        path = run / "problems" / pid / "evaluations.json"
        if path.exists():
            evaluations = load_json(path)
            passing[pid] = {
                e["candidate_id"] for e in evaluations
                if e["suite_visibility"] == "public" and e["execution_summary"]["all_passed"]
            }
    missing = set(pids) - passing.keys()
    if missing:
        archive = ROOT / "runs/v3_raw_archives" / f"{run.name}.heavy.tar.gz"
        with tarfile.open(archive, mode="r|gz") as handle:
            for member in handle:
                path = Path(member.name)
                if path.name != "evaluations.json" or path.parent.name not in missing:
                    continue
                with handle.extractfile(member) as stream:
                    evaluations = json.load(stream)
                passing[path.parent.name] = {
                    e["candidate_id"] for e in evaluations
                    if e["suite_visibility"] == "public" and e["execution_summary"]["all_passed"]
                }
                missing.remove(path.parent.name)
                if not missing:
                    break
    if missing:
        raise ValueError(f"{run.name}: thiếu evaluations của {sorted(missing)}")
    return passing


def build_data():
    analysis = load_json(RESULTS / "analysis_v3_3models.json")
    cache = load_json(RESULTS / "judge_cache_apps.json")
    groups = load_json(ROOT / "data/cohorts/apps_benchmark_300.json")["groups"]
    pids = [pid for level in LEVELS for pid in groups[level]]
    subsets = [groups[level] for level in LEVELS] + [pids]
    data = {}
    for model, _ in MODELS:
        apps = analysis[f"{model}/apps"]
        he = analysis[f"{model}/humaneval"]
        rows = {}
        for method, *_ in METHODS[:3]:
            summary = load_json(ROOT / "runs" / f"v3_apps_{model}_{method}" / "summary.json")
            records = {r["problem_id"]: r for r in summary["results"]}
            if set(records) != set(pids):
                raise ValueError(f"{model}/{method}: cohort không khớp APPS-300")
            rows[method] = {
                "apps_pr": [100 * sum(records[p].get("hidden_pass_rate") or 0 for p in ids) / len(ids)
                            for ids in subsets],
                "apps_pass_at_1": [100 * sum(bool(records[p].get("all_hidden_passed")) for p in ids) / len(ids)
                                   for ids in subsets],
                "humaneval_pass_at_1": 100 * he["methods"][method]["rate"],
            }
            if not math.isclose(rows[method]["apps_pass_at_1"][-1], 100 * apps["methods"][method]["rate"]):
                raise ValueError(f"{model}/{method}: summary khác analysis")

        run = ROOT / "runs" / f"v3_apps_{model}_mcts"
        records = {r["problem_id"]: r for r in load_json(run / "summary.json")["results"]}
        passing = public_passing_candidates(run, pids)
        rates, verdicts = {}, {}
        for pid in pids:
            pdir = run / "problems" / pid
            candidates = {c["candidate_id"]: c for c in load_json(pdir / "candidates.json")}
            selected_path = pdir / "selected.json"
            selected = load_json(selected_path)["candidate_id"] if selected_path.exists() else None
            chosen = min(passing[pid], key=lambda c: candidates[c]["created_sequence"]) if passing[pid] else selected
            if chosen is None:
                rates[pid], verdicts[pid] = 0.0, False
                continue
            result = cache[f"apps/{pid}/{candidates[chosen]['code_hash']}"]
            verdicts[pid] = result["passed"] if isinstance(result, dict) else result
            if chosen == selected:
                rates[pid] = records[pid].get("hidden_pass_rate") or 0.0
            else:
                # Không thể suy ra PR từ một boolean 'không pass hết'.
                rates[pid] = result["rate"]
        rows["test_only"] = {
            "apps_pr": [100 * sum(rates[p] for p in ids) / len(ids) for ids in subsets],
            "apps_pass_at_1": [100 * sum(verdicts[p] for p in ids) / len(ids) for ids in subsets],
            "humaneval_pass_at_1": 100 * he["offline_mcts"]["no_critic"] / he["n"],
        }
        offline = apps["offline_mcts"]
        if not math.isclose(rows["test_only"]["apps_pr"][-1], 100 * offline["pass_rate"]["no_critic"]):
            raise ValueError(f"{model}: PR Test-only khác analysis")
        for index, level in enumerate(LEVELS):
            expected = 100 * offline["by_difficulty"][level]["no_critic"] / len(groups[level])
            if not math.isclose(rows["test_only"]["apps_pass_at_1"][index], expected):
                raise ValueError(f"{model}/{level}: P@1 Test-only khác analysis")
        data[model] = rows
    return data


def plot_panels(data, metric, title, ylabel, filename, *, portrait):
    if portrait:
        fig, axes = plt.subplots(3, 1, figsize=(7.2, 10), sharey=True)
        fig.subplots_adjust(left=0.12, right=0.98, bottom=0.06, top=0.84, hspace=0.45)
    else:
        fig, axes = plt.subplots(1, 3, figsize=(16, 5.8), sharey=True)
        fig.subplots_adjust(left=0.065, right=0.99, bottom=0.12, top=0.75, wspace=0.10)
    fig.suptitle(title, y=0.98, fontsize=20, fontweight="bold")
    handles = [Patch(facecolor=color, edgecolor="#333333", hatch=hatch, label=label)
               for _, label, color, hatch in METHODS]
    fig.legend(handles=handles, loc="upper center",
               bbox_to_anchor=(0.53, 0.94 if portrait else 0.91),
               ncol=2 if portrait else 4, frameon=False,
               fontsize=11 if portrait else 13, handlelength=1.6)
    is_he = metric == "humaneval_pass_at_1"
    for ax, (model, label) in zip(axes, MODELS):
        for index, (method, _, color, hatch) in enumerate(METHODS):
            if is_he:
                positions = np.array([index])
                values = [data[model][method][metric]]
                width = 0.65
            else:
                positions = np.arange(4) + (index - 1.5) * 0.20
                values = data[model][method][metric]
                width = 0.18
            bars = ax.bar(positions, values, width=width, color=color, edgecolor="#333333",
                          linewidth=0.7, hatch=hatch, zorder=3)
            ax.bar_label(bars, labels=[f"{v:.2f}" for v in values], padding=3,
                         fontsize=11 if is_he else 9, rotation=0 if is_he else 90)
        ax.set_title(label, fontsize=15, pad=12)
        # Cột bắt đầu từ 0; cùng thang đo cho cả ba model, không phóng đại chênh lệch.
        ax.set_ylim(0, 115)
        ax.set_yticks(np.arange(0, 101, 20))
        ax.grid(axis="y", color="#D6D6D6", linewidth=0.6, zorder=0)
        ax.tick_params(axis="both", length=0, labelsize=12, pad=7)
        if is_he:
            ax.set_xticks(range(4), ["Direct", "Best-of-16", "MCTS\nDual", "MCTS\nTest-only"])
        else:
            ax.set_xticks(range(4), ["Intro", "Inter", "Comp", "Average" if metric == "apps_pr" else "Overall"])
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_linewidth(1.2)
    for ax in axes if portrait else axes[:1]:
        ax.set_ylabel(ylabel, fontsize=14)
    for ext in ("png", "pdf"):
        path = OUT / f"{filename}{'_portrait' if portrait else ''}.{ext}"
        fig.savefig(path, dpi=300, facecolor="white")
        print(f"Wrote {path.relative_to(ROOT)}")
    plt.close(fig)


def main():
    plt.rcParams.update({
        "font.family": ["Arial", "DejaVu Sans", "sans-serif"],
        "font.size": 14, "legend.frameon": False, "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    data = build_data()
    OUT.mkdir(parents=True, exist_ok=True)
    sidecar = {
        "protocol": "v3.1",
        "unit": "percent",
        "sources": ["docs/results/v3/analysis_v3_3models.json", "docs/results/v3/judge_cache_apps.json",
                    "data/cohorts/apps_benchmark_300.json", "runs/v3_apps_<model>_<method>/summary.json",
                    "runs/v3_apps_<model>_mcts/problems/", "runs/v3_raw_archives/v3_apps_<model>_mcts.heavy.tar.gz"],
        "apps_columns": LEVELS + ["overall"],
        "notes": ["Test-only là chọn lại offline từ run Dual, không phải run độc lập.",
                  "PR Test-only dùng verdict gốc nếu trùng candidate ID, nếu khác dùng cache local.",
                  "P@1 của các run chính dùng verdict gốc; Test-only dùng verdict local.",
                  "Qwen3.5-9B có output bị cắt trên APPS; MCTS APPS chạy Colab, baseline chạy Modal.",
                  "Không có candidate tính 0; mẫu số đầy đủ 300 bài APPS và 164 bài HumanEval."],
        "models": data,
    }
    (RESULTS / "benchmark_panels_v3.json").write_text(json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for metric, title, ylabel, filename in [
        ("apps_pr", "APPS-300 Pass Rate", "Pass Rate (%)", "apps_pass_rate"),
        ("apps_pass_at_1", "APPS-300 Pass@1", "Pass@1 (%)", "apps_pass_at_1"),
        ("humaneval_pass_at_1", "HumanEval-164 Pass@1", "Pass@1 (%)", "humaneval_pass_at_1"),
    ]:
        for portrait in (False, True):
            plot_panels(data, metric, title, ylabel, filename, portrait=portrait)


if __name__ == "__main__":
    main()
