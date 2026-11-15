"""Small-multiple token charts derived from Bảng 4.2 in the thesis source.

The LaTeX table is the single source of truth: edit its numeric cells, then run
``python scripts/make_token_table_panels.py`` to regenerate both figures.
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "thesis/chuong/chuong4.tex"
OUT = ROOT / "docs/report/figures/v3"

MODELS = ("Qwen2.5-Coder-7B", "Seed-Coder-8B", "Qwen3.5-9B")
METHODS = ("Direct", "Best-of-16", "MCTS Dual", "MCTS Test-only")
METRICS = ("Input", "Output", "Total")
DATASETS = (("APPS-300", 0, "H7_tokens_apps_breakdown"),
            ("HumanEval-164", 3, "H7_tokens_humaneval_breakdown"))
COLORS = {"Direct": "#898781", "Best-of-16": "#B64342", "MCTS Dual": "#0F4D92", "MCTS Test-only": "#7ABD85"}
HATCHES = {"Direct": "", "Best-of-16": "", "MCTS Dual": "", "MCTS Test-only": "//"}
SURFACE, GRID, INK, MUTED = "#ffffff", "#e1e0d9", "#0b0b0b", "#52514e"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10,
    "axes.edgecolor": "#000000", "axes.linewidth": 1.2, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.7, "axes.axisbelow": True, "axes.spines.top": False,
    "axes.spines.right": False, "legend.frameon": False, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "savefig.dpi": 300, "pdf.fonttype": 42,
})


def clean_latex(value: str) -> str:
    value = value.replace(r"\\", " ")
    value = re.sub(r"\\[A-Za-z]+(?:\[[^]]+\])?", "", value)
    value = value.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", value).strip().replace("- ", "-")


def token(cell: str) -> int:
    value = re.sub(r"\\textcolor\{red\}\{([^{}]+)\}", r"\1", cell.strip()).replace(".", "")
    if not value.isdigit():
        raise ValueError(f"Bảng 4.2 có ô token không hợp lệ: {cell!r}")
    return int(value)


def read_token_table() -> dict[str, dict[str, list[int]]]:
    source = TABLE.read_text(encoding="utf-8")
    start = source.index(r"\label{tab:token-trungbinh}")
    end = source.index(r"\end{tabular*}", start)
    rows = source[start:end].splitlines()
    table: dict[str, dict[str, list[int]]] = {}
    model: str | None = None
    for raw in rows:
        if r"\multirow{4}" in raw:
            match = re.search(r"\\shortstack\[l\]\{([^}]*)\}", raw)
            if match is None:
                raise ValueError(f"Không đọc được model từ Bảng 4.2: {raw}")
            model = clean_latex(match.group(1))
            table[model] = {}
            continue
        if model is None or " & " not in raw or not raw.lstrip().startswith("&"):
            continue
        cells = [cell.strip() for cell in raw.strip().removesuffix(r"\\").split("&")]
        if len(cells) != 8:
            continue
        method = clean_latex(cells[1])
        if method not in METHODS:
            continue
        table[model][method] = [token(value) for value in cells[2:]]
    missing = [(model, method) for model in MODELS for method in METHODS if method not in table.get(model, {})]
    if missing:
        raise ValueError(f"Bảng 4.2 thiếu dữ liệu: {missing}")
    return table


def compact_tokens(value: int) -> str:
    if value < 1_000:
        return str(value)
    return f"{value / 1_000:.1f}k" if value < 10_000 else f"{value / 1_000:.0f}k"


def ytick(value: float, _position: int) -> str:
    if value >= 1_000:
        return f"{value / 1_000:g}k"
    return f"{value:g}"


def draw_dataset(table: dict[str, dict[str, list[int]]], dataset: str, offset: int, output: str) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 9.0), sharex=True, sharey=True)
    x = list(range(len(METRICS)))
    width = 0.18
    offsets = (-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width)
    for axis, model in zip(axes, MODELS):
        for method, bar_offset in zip(METHODS, offsets):
            values = table[model][method][offset:offset + 3]
            positions = [value + bar_offset for value in x]
            axis.bar(
                positions, [value - 1 for value in values], width=width, bottom=1, color=COLORS[method],
                edgecolor="#4e4e4e", linewidth=0.7, hatch=HATCHES[method], label=method,
            )
            for position, value in zip(positions, values):
                axis.annotate(
                    compact_tokens(value), (position, value), xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", rotation=90, fontsize=8, color=INK,
                )
        axis.set_title(model, loc="left", pad=7, fontweight="bold")
        axis.set_yscale("log")
        axis.set_ylim(50, 2_000_000)
        axis.set_yticks((100, 1_000, 10_000, 100_000))
        axis.yaxis.set_major_formatter(FuncFormatter(ytick))
        axis.grid(axis="x", visible=False)
        axis.grid(axis="y", which="major")
        axis.set_ylabel("Tokens / problem\n(log scale)")
    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels(METRICS, fontsize=10)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.955),
               fontsize=10, columnspacing=2.0)
    fig.suptitle(dataset, x=0.13, y=0.99, ha="left", fontsize=14, fontweight="bold", color=INK)
    fig.subplots_adjust(left=0.13, right=0.98, bottom=0.07, top=0.86, hspace=0.48)
    OUT.mkdir(parents=True, exist_ok=True)
    for extension in ("pdf", "png"):
        fig.savefig(OUT / f"{output}.{extension}", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def main() -> None:
    table = read_token_table()
    for dataset, offset, output in DATASETS:
        draw_dataset(table, dataset, offset, output)


if __name__ == "__main__":
    main()
