"""Figures H1-H6 for the v3.1 results (report chapters 4-5).

Every number comes from docs/results/v3/analysis_v3_3models.json or from runs/v3_*/problems/*/completed.json;
nothing is typed in by hand. Output: docs/report/figures/v3/<name>.{pdf,png}.

usage: python3 scripts/make_figures_v3.py
"""
import glob
import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / 'docs/results/v3/analysis_v3_3models.json'
OUT = ROOT / 'docs/report/figures/v3'

MODELS = [('qwen25c7b', 'Qwen2.5-Coder-7B'), ('seedcoder8b', 'Seed-Coder-8B'), ('qwen35_9b', 'Qwen3.5-9B')]
DATASETS = [('apps', 'APPS-300'), ('humaneval', 'HumanEval-164')]
METHODS = [('direct', 'Direct'), ('bon16', 'Best-of-16'), ('mcts', 'RethinkMCTS')]
COMPARISONS = [('mcts_vs_direct', 'MCTS so với Direct'), ('mcts_vs_bon16', 'MCTS so với Best-of-16'),
               ('bon16_vs_direct', 'Best-of-16 so với Direct')]
DIFFICULTIES = [('introductory', 'Introductory'), ('interview', 'Interview'), ('competition', 'Competition')]
ROLES = [('expansion', 'Expansion'), ('code', 'Sinh code'), ('rethink', 'Rethink'),
         ('block_analysis', 'Block analysis'), ('critic', 'Critic')]

# Palette (validated with the dataviz skill's validate_palette.js on the light surface).
INK, INK2, MUTED, GRID, AXIS, SURFACE = '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7', '#ffffff'
COLOR = {'direct': '#898781', 'bon16': '#2a78d6', 'mcts': '#eb6834'}
MARKER = {'direct': 's', 'bon16': 'o', 'mcts': 'D'}
ROLE_COLOR = dict(zip([r for r, _ in ROLES], ['#1baf7a', '#eda100', '#6250d6', '#e87ba4', '#008300']))
STAGE_COLOR = ['#ef8c64', '#d4541f', '#94390f']  # ordinal ramp of the MCTS hue

plt.rcParams.update({
    'font.family': 'Arial', 'font.size': 9, 'axes.titlesize': 10, 'axes.labelsize': 9,
    'axes.edgecolor': AXIS, 'axes.linewidth': 0.8, 'axes.labelcolor': INK2, 'axes.titlecolor': INK,
    'xtick.color': INK2, 'ytick.color': INK2, 'xtick.major.size': 0, 'ytick.major.size': 0,
    'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.axisbelow': True,
    'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False,
    'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE, 'savefig.dpi': 200, 'pdf.fonttype': 42,
})


def vn(x, nd=1):
    """Vietnamese decimal comma."""
    return f'{x:.{nd}f}'.replace('.', ',')


def save(fig, name, source, note=None):
    text = (note + '\n' if note else '') + f'Nguồn: {source}'
    fig.text(0.01, -0.01, text, fontsize=7, color=MUTED, ha='left', va='top', linespacing=1.5)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'{name}.{ext}', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)
    print('wrote', OUT / name)


def method_legend(ax_or_fig, **kw):
    handles = [Line2D([], [], color=COLOR[m], marker=MARKER[m], linestyle='-', markersize=6, linewidth=1.6, label=l)
               for m, l in METHODS]
    return ax_or_fig.legend(handles=handles, **kw)


def run_usage(run):
    """Per-problem usage dicts of one run (null token counts are treated as missing, i.e. 0)."""
    return [json.loads(Path(f).read_text())['usage'] for f in glob.glob(str(ROOT / 'runs' / run / 'problems/*/completed.json'))]


def mean_tokens(run):
    us = run_usage(run)
    return sum((u.get('input_tokens') or 0) + (u.get('output_tokens') or 0) for u in us) / len(us)


# ---------------------------------------------------------------------------------------------- H1
def h1_pass_at_1(A):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    off = {'direct': 0.22, 'bon16': 0.0, 'mcts': -0.22}
    for ax, (ds, dsl) in zip(axes, DATASETS):
        for i, (mk, ml) in enumerate(MODELS):
            y0 = len(MODELS) - 1 - i
            for m, _ in METHODS:
                r = A[f'{mk}/{ds}']['methods'][m]
                lo, hi = (100 * v for v in r['wilson95'])
                ax.plot([lo, hi], [y0 + off[m]] * 2, color=COLOR[m], linewidth=1.6, solid_capstyle='round')
                ax.plot(100 * r['rate'], y0 + off[m], marker=MARKER[m], color=COLOR[m], markersize=6,
                        markeredgecolor=SURFACE, markeredgewidth=1.0, linestyle='')
        ax.set_yticks(range(len(MODELS)))
        ax.set_yticklabels([ml for _, ml in MODELS][::-1] if ax is axes[0] else [])
        ax.set_ylim(-0.6, len(MODELS) - 0.4)
        ax.grid(axis='y', visible=False)
        ax.set_title(dsl, loc='left')
        ax.set_xlabel('Pass@1 trên hidden test (%)')
    axes[0].set_xlim(0, 80)
    axes[1].set_xlim(70, 100)
    method_legend(fig, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.06))
    fig.tight_layout()
    save(fig, 'H1_pass_at_1', 'analysis_v3_3models.json (methods.*.rate, wilson95)',
         'Thanh ngang: khoảng tin cậy Wilson 95%. Trục x của hai khung khác nhau.')


# ---------------------------------------------------------------------------------------------- H2
def h2_forest(A):
    rows = [(mk, ml, ds, dsl) for ds, dsl in DATASETS for mk, ml in MODELS]
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 3.4), sharey=True)
    for ax, (ck, cl) in zip(axes, COMPARISONS):
        for j, (mk, ml, ds, dsl) in enumerate(rows):
            y = len(rows) - 1 - j + (0.5 if ds == 'apps' else 0)
            c = A[f'{mk}/{ds}']['comparisons'][ck]
            lo, hi = (100 * v for v in c['boot95'])
            sig = c['p_holm'] < 0.05
            ax.plot([lo, hi], [y, y], color=INK2, linewidth=1.4, solid_capstyle='round')
            ax.plot(100 * c['diff'], y, marker='o', markersize=6.5, linestyle='',
                    markerfacecolor=INK if sig else SURFACE, markeredgecolor=INK, markeredgewidth=1.2)
            ax.annotate(f"{c['wins']}/{c['losses']}", (1.0, y), xycoords=('axes fraction', 'data'),
                        xytext=(4, 0), textcoords='offset points', fontsize=7, color=INK2, va='center')
        ax.axvline(0, color=INK2, linewidth=0.9)
        ax.set_title(cl, loc='left', fontsize=9)
        ax.set_xlabel('Chênh lệch Pass@1 (điểm %)')
        ax.grid(axis='y', visible=False)
        ax.axhline(len(rows) / 2 - 0.25, color=GRID, linewidth=0.6)
        ax.set_ylim(-0.6, len(rows) + 1.0)
        ax.annotate('thắng/thua', (1.0, len(rows) + 0.35), xycoords=('axes fraction', 'data'), xytext=(4, 0),
                    textcoords='offset points', fontsize=7, color=MUTED, va='center')
    ys = [len(rows) - 1 - j + (0.5 if ds == 'apps' else 0) for j, (_, _, ds, _) in enumerate(rows)]
    axes[0].set_yticks(ys)
    axes[0].set_yticklabels([f'{ml} · {dsl.split("-")[0]}' for _, ml, _, dsl in rows])
    lo = min(min(ax.get_xlim()[0] for ax in axes), -8)
    hi = max(ax.get_xlim()[1] for ax in axes)
    for ax in axes:
        ax.set_xlim(lo, hi)
    handles = [Line2D([], [], marker='o', linestyle='', markerfacecolor=INK, markeredgecolor=INK, label='Có ý nghĩa sau Holm (p < 0,05)'),
               Line2D([], [], marker='o', linestyle='', markerfacecolor=SURFACE, markeredgecolor=INK, label='Không có ý nghĩa sau Holm')]
    fig.legend(handles=handles, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.42)
    save(fig, 'H2_paired_forest', 'analysis_v3_3models.json (comparisons)',
         'Thanh ngang: CI bootstrap 95% ghép cặp. Cột số bên phải mỗi khung: số bài thắng/thua (phương pháp thứ nhất/thứ hai). Holm trên 18 so sánh.')


# ---------------------------------------------------------------------------------------------- H3
def h3_cost_curve(A):
    fig, axes = plt.subplots(2, 3, figsize=(7.6, 4.9))
    for r, (ds, dsl) in enumerate(DATASETS):
        for c, (mk, ml) in enumerate(MODELS):
            ax = axes[r][c]
            cell = A[f'{mk}/{ds}']
            n = cell['n']
            t = {m: mean_tokens(f'v3_{ds}_{mk}_{m}') for m, _ in METHODS}
            ks = sorted(int(k) for k in cell['best_of_k'])
            # Samples are i.i.d., so the expected cost of the first k samples is k/16 of the Best-of-16 cost.
            xs = [t['bon16'] * k / 16 for k in ks]
            ys = [100 * cell['best_of_k'][str(k)] / n for k in ks]
            ax.plot(xs, ys, color=COLOR['bon16'], linewidth=1.8)
            mk_idx = [k - 1 for k in (1, 2, 4, 8, 16)]
            ax.plot([xs[i] for i in mk_idx], [ys[i] for i in mk_idx], color=COLOR['bon16'], marker='o', markersize=4,
                    markeredgecolor=SURFACE, markeredgewidth=0.8, linestyle='')
            for k in (1, 16):
                ax.annotate(f'k={k}', (xs[k - 1], ys[k - 1]), xytext=(6, -10) if k == 1 else (0, 6),
                            textcoords='offset points', fontsize=7, color=INK2, ha='left' if k == 1 else 'center')
            for m in ('direct', 'mcts'):
                ax.plot(t[m], 100 * cell['methods'][m]['rate'], marker=MARKER[m], color=COLOR[m], markersize=7,
                        markeredgecolor=SURFACE, markeredgewidth=1.0, linestyle='')
            ratio = t['mcts'] / t['bon16']
            ax.annotate(f'×{vn(ratio)} token\nso với BoN16', (t['mcts'], 100 * cell['methods']['mcts']['rate']),
                        xytext=(0, -24), textcoords='offset points', fontsize=7, color=INK2, ha='center')
            ax.set_xscale('log')
            ax.set_title(f'{ml} · {dsl.split("-")[0]}', loc='left', fontsize=9)
            if c == 0:
                ax.set_ylabel('Pass@1 (%)')
            if r == 1:
                ax.set_xlabel('Token trung bình mỗi bài (thang log)')
            ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
                lambda v, _: f'{int(v / 1000)}k' if v >= 1000 else f'{int(v)}'))
            ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
            ax.set_xlim(t['direct'] / 1.8, t['mcts'] * 1.8)
    for r in range(2):
        lo = min(axes[r][c].get_ylim()[0] for c in range(3))
        hi = max(axes[r][c].get_ylim()[1] for c in range(3))
        for c in range(3):
            axes[r][c].set_ylim(lo - 5, hi + 3)
    handles = [Line2D([], [], color=COLOR['direct'], marker=MARKER['direct'], linestyle='', markersize=6, label='Direct'),
               Line2D([], [], color=COLOR['bon16'], marker='o', markersize=3.5, linewidth=1.8, label='Best-of-k (k = 1…16)'),
               Line2D([], [], color=COLOR['mcts'], marker=MARKER['mcts'], linestyle='', markersize=6, label='RethinkMCTS')]
    fig.legend(handles=handles, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout()
    save(fig, 'H3_cost_vs_pass', 'analysis_v3_3models.json (best_of_k, methods); runs/v3_*/problems/*/completed.json (usage)',
         'Best-of-k: chọn theo public test trong k mẫu đầu, chấm lại hidden trên máy local; token = k/16 token của Best-of-16. '
         'Token = input + output trung bình mỗi bài.')


# ---------------------------------------------------------------------------------------------- H4
def h4_difficulty(A):
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9), sharey=True)
    x = range(len(DIFFICULTIES))
    for ax, (mk, ml) in zip(axes, MODELS):
        bd = A[f'{mk}/apps']['by_difficulty']
        for m, _ in METHODS:
            ys = [100 * bd[d][m] / bd[d]['n'] for d, _ in DIFFICULTIES]
            ax.plot(x, ys, color=COLOR[m], marker=MARKER[m], markersize=6, linewidth=1.8,
                    markeredgecolor=SURFACE, markeredgewidth=1.0)
        ax.set_xticks(list(x))
        ax.set_xticklabels([l for _, l in DIFFICULTIES])
        ax.set_xlim(-0.3, len(DIFFICULTIES) - 0.7)
        ax.set_title(ml, loc='left')
        ax.grid(axis='x', visible=False)
    axes[0].set_ylabel('Pass@1 (%), 100 bài mỗi mức')
    axes[0].set_ylim(0, 90)
    fig.tight_layout()
    method_legend(fig, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.08))
    save(fig, 'H4_apps_by_difficulty', 'analysis_v3_3models.json (by_difficulty)')


# ---------------------------------------------------------------------------------------------- H5
def h5_search_stages(A):
    stages = [('first_program', 'Chương trình đầu tiên'), ('no_critic', 'Sau search, chọn theo test'),
              ('selected_local', 'Sau search, chọn theo test + critic')]
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={'width_ratios': [1, 1]})
    w = 0.26
    for ax, (ds, dsl) in zip(axes, DATASETS):
        for i, (mk, ml) in enumerate(MODELS):
            cell = A[f'{mk}/{ds}']
            om, n = cell['offline_mcts'], cell['n']
            for s, (sk, _) in enumerate(stages):
                ax.bar(i + (s - 1) * (w + 0.02), 100 * om[sk] / n, width=w, color=STAGE_COLOR[s], linewidth=0)
            sv = om['search_vs_first_program']
            cv = om['critic_vs_no_critic']
            top = max(100 * om[sk] / n for sk, _ in stages)
            ax.annotate(f"search: +{sv['wins']}/−{sv['losses']}\ncritic: +{cv['wins']}/−{cv['losses']}", (i, top),
                        xytext=(0, 4), textcoords='offset points', fontsize=7, color=INK2, ha='center', va='bottom')
        ax.set_xticks(range(len(MODELS)))
        ax.set_xticklabels([ml for _, ml in MODELS], fontsize=8)
        ax.set_title(dsl, loc='left')
        ax.grid(axis='x', visible=False)
        ax.set_ylim(0, 114 if ds == 'humaneval' else 85)
        ax.set_yticks(range(0, 101 if ds == 'humaneval' else 81, 20))
    axes[0].set_ylabel('Pass@1 (%)')
    handles = [plt.Rectangle((0, 0), 1, 1, color=STAGE_COLOR[s], label=l) for s, (_, l) in enumerate(stages)]
    fig.legend(handles=handles, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.07), fontsize=8)
    fig.tight_layout()
    save(fig, 'H5_mcts_stages', 'analysis_v3_3models.json (offline_mcts)',
         'Chọn lại offline trên cây MCTS, chấm hidden trên máy local. Chú thích trên cột: số bài thắng/thua của bước so với bước trước.')


# ---------------------------------------------------------------------------------------------- H6
def h6_tokens_by_role():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.9), sharey=True)
    labels = []
    for ax, (ds, dsl) in zip(axes, DATASETS):
        for i, (mk, ml) in enumerate(MODELS):
            us = run_usage(f'v3_{ds}_{mk}_mcts')
            for j, kind in enumerate(('input', 'output')):
                y = (len(MODELS) - 1 - i) * 2.6 + (0.55 if kind == 'input' else -0.55)
                left = 0
                for role, _ in ROLES:
                    v = sum((((u.get('tokens_by_role') or {}).get(role) or {}).get(kind) or 0) for u in us) / len(us) / 1000
                    if v > 0:
                        ax.barh(y, v, left=left, height=0.9, color=ROLE_COLOR[role], edgecolor=SURFACE, linewidth=1.0)
                    left += v
                ax.annotate(f'{vn(left, 0)}k', (left, y), xytext=(3, 0), textcoords='offset points',
                            fontsize=7, color=INK2, va='center')
                if ax is axes[0]:
                    labels.append((y, f'{ml} · {"input" if kind == "input" else "output"}'))
        ax.set_title(f'{dsl}: RethinkMCTS', loc='left')
        ax.set_xlabel('Nghìn token trung bình mỗi bài')
        ax.grid(axis='y', visible=False)
        ax.set_xlim(0, ax.get_xlim()[1] * 1.12)
    axes[0].set_yticks([y for y, _ in labels])
    axes[0].set_yticklabels([l for _, l in labels], fontsize=8)
    handles = [plt.Rectangle((0, 0), 1, 1, color=ROLE_COLOR[r], label=l) for r, l in ROLES]
    fig.legend(handles=handles, loc='upper center', ncol=5, bbox_to_anchor=(0.5, 1.07), fontsize=8)
    fig.tight_layout()
    save(fig, 'H6_mcts_tokens_by_role', 'runs/v3_*_mcts/problems/*/completed.json (usage.tokens_by_role); số liệu dạng bảng ở ledger mục 5.1')


def main():
    A = json.loads(ANALYSIS.read_text())
    h1_pass_at_1(A)
    h2_forest(A)
    h3_cost_curve(A)
    h4_difficulty(A)
    h5_search_stages(A)
    h6_tokens_by_role()


if __name__ == '__main__':
    main()
