"""Figures H1-H6 for the v3.1 results (report chapters 4-5).

Every number comes from docs/results/v3/analysis_v3_3models.json or from runs/v3_*/problems/*/completed.json;
nothing is typed in by hand. Output: docs/report/figures/v3/<name>.{pdf,png}.

usage: python3 scripts/make_figures_v3.py
"""
import glob
import json
import tarfile
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
INK, INK2, MUTED, GRID, AXIS, SURFACE = '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#000000', '#ffffff'
COLOR = {'direct': '#898781', 'bon16': '#B64342', 'mcts': '#0F4D92'}
MARKER = {'direct': 's', 'bon16': 'o', 'mcts': 'D'}
ROLE_COLOR = dict(zip([r for r, _ in ROLES], ['#42949E', '#3775BA', '#9A4D8E', '#E9A6A1', '#578B55']))

plt.rcParams.update({
    'font.family': 'Arial', 'font.size': 9, 'axes.titlesize': 10, 'axes.labelsize': 9,
    'axes.edgecolor': AXIS, 'axes.linewidth': 1.2, 'axes.labelcolor': INK2, 'axes.titlecolor': INK,
    'xtick.color': INK2, 'ytick.color': INK2, 'xtick.major.size': 0, 'ytick.major.size': 0,
    'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.axisbelow': True,
    'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False,
    'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE, 'savefig.dpi': 300, 'pdf.fonttype': 42,
})


def vn(x, nd=1):
    """Vietnamese decimal comma."""
    return f'{x:.{nd}f}'.replace('.', ',')


def save(fig, name, source, note=None):
    # `source` documents which artifact each figure is built from; it is not printed on the figure
    # (the report keeps sources out of the rendered text). `note` explains how to read the figure.
    if note:
        fig.text(0.01, -0.01, note, fontsize=7, color=MUTED, ha='left', va='top', linespacing=1.5)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'{name}.{ext}', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)
    print('wrote', OUT / name)


def method_legend(ax_or_fig, **kw):
    handles = [Line2D([], [], color=COLOR[m], marker=MARKER[m], linestyle='-', markersize=6, linewidth=1.6, label=l)
               for m, l in METHODS]
    return ax_or_fig.legend(handles=handles, **kw)


def role_tokens(run):
    """Mean recorded tokens per problem and role; use archived request logs when traces are compressed."""
    paths = [Path(f) for f in glob.glob(str(ROOT / 'runs' / run / 'problems/*/requests.json'))]
    archive = ROOT / 'runs' / 'v3_raw_archives' / f'{run}.heavy.tar.gz'
    records = []
    if paths:
        records = (json.loads(path.read_text()) for path in paths)
    elif archive.exists():
        def archived_records():
            with tarfile.open(archive, 'r:gz') as tf:
                for member in tf:
                    if member.name.endswith('/requests.json'):
                        yield json.load(tf.extractfile(member))
        records = archived_records()
    else:
        raise FileNotFoundError(f'No request logs or archive found for {run}')
    acc, count = {}, 0
    for requests in records:
        count += 1
        for q in requests:
            response = q.get('response') or {}
            role = q['request']['role']
            acc[(role, 'input')] = acc.get((role, 'input'), 0) + (response.get('prompt_tokens') or 0)
            acc[(role, 'output')] = acc.get((role, 'output'), 0) + (response.get('completion_tokens') or 0)
    if not count:
        raise ValueError(f'No request records found for {run}')
    return {key: value / count for key, value in acc.items()}


# ---------------------------------------------------------------------------------------------- H1
def h1_pass_at_1_panel(A, dataset, dataset_label, xlim, filename, *, show_legend):
    """One publication-style forest plot per dataset, with its own meaningful scale."""
    style = {
        'direct': ('Direct', '#767676', 's'),
        'bon16': ('Best-of-16', '#B64342', 'o'),
        'mcts': ('MCTS Dual', '#0F4D92', 'D'),
    }
    offsets = {'direct': 0.24, 'bon16': 0.0, 'mcts': -0.24}
    fig, ax = plt.subplots(figsize=(7.2, 3.15))
    for row, (model_key, _) in enumerate(MODELS):
        y = len(MODELS) - 1 - row
        for method, (method_label, color, marker) in style.items():
            result = A[f'{model_key}/{dataset}']['methods'][method]
            point = 100 * result['rate']
            low, high = (100 * value for value in result['wilson95'])
            y_pos = y + offsets[method]
            ax.errorbar(
                point, y_pos, xerr=[[point - low], [high - point]], fmt=marker,
                color=color, ecolor=color, elinewidth=2.0, capsize=4,
                markersize=8, markeredgecolor=SURFACE, markeredgewidth=1.0, zorder=3,
            )
            label_offset = 8 if method != 'mcts' else -11
            ax.annotate(
                f'{point:.1f}', (point, y_pos), xytext=(0, label_offset), textcoords='offset points',
                fontsize=8.5, color=color, ha='center',
                va='bottom' if label_offset > 0 else 'top',
            )
    n = A[f'{MODELS[0][0]}/{dataset}']['n']
    ax.set_title(f'{dataset_label} (n={n})', loc='left', pad=10, fontsize=13, fontweight='bold')
    ax.set_xlim(*xlim)
    ax.set_xlabel('Pass@1 (%)', fontsize=11)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels([label for _, label in MODELS][::-1], fontsize=10)
    ax.set_ylim(-0.68, len(MODELS) - 0.32)
    ax.grid(axis='y', visible=False)
    if show_legend:
        handles = [
            Line2D([], [], color=color, marker=marker, linewidth=1.8, markersize=7.5,
                   label=label, markeredgecolor=SURFACE, markeredgewidth=1.0)
            for label, color, marker in style.values()
        ]
        fig.legend(handles=handles, loc='upper center', ncol=3, bbox_to_anchor=(0.62, 1.04), fontsize=10)
        fig.tight_layout(rect=(0, 0, 1, 0.88), pad=1.0)
    else:
        fig.tight_layout(pad=1.0)
    save(fig, filename, 'analysis_v3_3models.json (methods.*.rate, wilson95)')


def h1_pass_at_1(A):
    h1_pass_at_1_panel(A, 'apps', 'APPS-300', (8, 78), 'H1_apps_pass_at_1', show_legend=True)
    h1_pass_at_1_panel(A, 'humaneval', 'HumanEval-164', (68, 100), 'H1_humaneval_pass_at_1', show_legend=False)


# ---------------------------------------------------------------------------------------------- H2
def h2_forest(A):
    """Paired bootstrap forest plots, separated vertically for report-scale reading."""
    rows = [(mk, ml, ds, dsl) for ds, dsl in DATASETS for mk, ml in MODELS]
    comparisons = (
        ('mcts_vs_direct', 'MCTS Dual so với Direct', '#0F4D92'),
        ('mcts_vs_bon16', 'MCTS Dual so với Best-of-16', '#0F4D92'),
        ('bon16_vs_direct', 'Best-of-16 so với Direct', '#B64342'),
    )
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 7.5), sharex=True)
    ys = list(reversed(range(len(rows))))
    x_min, x_max = -10, 31
    for ax, (comparison, title, color) in zip(axes, comparisons):
        for y, (mk, ml, ds, dsl) in zip(ys, rows):
            result = A[f'{mk}/{ds}']['comparisons'][comparison]
            point = 100 * result['diff']
            low, high = (100 * value for value in result['boot95'])
            significant = result['p_holm'] < 0.05
            ax.errorbar(
                point, y, xerr=[[point - low], [high - point]], fmt='o',
                color=color, ecolor=color, elinewidth=2.0, capsize=4,
                markersize=8.5, markerfacecolor=color if significant else SURFACE,
                markeredgecolor=color, markeredgewidth=1.7, zorder=3,
            )
            sign = '+' if point > 0 else '−' if point < 0 else ''
            ax.annotate(
                f'{sign}{abs(point):.1f}', (point, y), xytext=(0, 9),
                textcoords='offset points', ha='center', va='bottom',
                fontsize=8.5, color=color, fontweight='bold' if significant else 'normal',
            )
            ax.text(
                1.02, y, f"{result['wins']}/{result['losses']}",
                transform=ax.get_yaxis_transform(), ha='left', va='center',
                fontsize=8.5, color=INK2, clip_on=False,
            )
        ax.axvline(0, color=INK2, linewidth=1.1, zorder=1)
        ax.axhline(2.5, color=GRID, linewidth=0.8, zorder=1)
        ax.set_title(title, loc='left', fontsize=12, fontweight='bold', pad=8, color=color)
        ax.text(1.02, 1.05, 'thắng/thua', transform=ax.transAxes, ha='left', va='bottom',
                fontsize=8, color=MUTED, clip_on=False)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(-0.65, len(rows) - 0.35)
        ax.set_yticks(ys)
        ax.set_yticklabels([f'{ml} · {dsl.split("-")[0]}' for _, ml, _, dsl in rows], fontsize=9)
        ax.grid(axis='y', visible=False)
    axes[-1].set_xlabel('Chênh lệch Pass@1 ghép cặp (điểm %)', fontsize=11)
    handles = [
        Line2D([], [], marker='o', linestyle='', markerfacecolor=INK, markeredgecolor=INK,
               markersize=8, label='Có ý nghĩa sau Holm (p < 0,05)'),
        Line2D([], [], marker='o', linestyle='', markerfacecolor=SURFACE, markeredgecolor=INK,
               markeredgewidth=1.5, markersize=8, label='Không có ý nghĩa sau Holm'),
    ]
    fig.legend(handles=handles, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.015), fontsize=10)
    fig.tight_layout(rect=(0, 0, 0.89, 0.965), h_pad=1.25)
    save(fig, 'H2_paired_forest', 'analysis_v3_3models.json (comparisons)',
         'Thanh ngang: CI bootstrap 95% ghép cặp. Cột số bên phải mỗi khung: số bài thắng/thua (phương pháp thứ nhất/thứ hai). Holm trên 18 so sánh.')


# ---------------------------------------------------------------------------------------------- H3
def h3_budget_panel(A, model_key, model_label, dataset, dataset_label):
    """Readable two-track budget trajectories with one linear token axis per method."""
    styles = {
        'direct': ('Direct', '#898781', 's'),
        'bon16': ('Best-of-$k$', '#B64342', 'o'),
        'mcts': ('MCTS after $k$ rollouts', '#0F4D92', 'D'),
    }
    cell = A[f'{model_key}/{dataset}']
    n = cell['n']
    cost = {
        method: cell['methods'][method]['cost']['input_tokens'] + cell['methods'][method]['cost']['output_tokens']
        for method in ('direct', 'bon16', 'mcts')
    }
    ks = sorted(int(k) for k in cell['best_of_k'])
    bok_x = [cost['bon16'] * k / 16 for k in ks]
    bok_y = [100 * cell['best_of_k'][str(k)] / n for k in ks]
    mcts = cell['mcts_at_k']
    mcts_x = [mcts[str(k)]['mean_tokens'] for k in ks]
    mcts_y = [100 * mcts[str(k)]['passed'] / n for k in ks]
    direct_y = 100 * cell['methods']['direct']['rate']

    fig, axes = plt.subplots(2, 1, figsize=(7.2, 6.4))
    tracks = (
        (axes[0], 'bon16', bok_x, bok_y, 'Direct and Best-of-$k$'),
        (axes[1], 'mcts', mcts_x, mcts_y, 'MCTS after $k$ rollouts'),
    )
    for ax, method, xs, ys, title in tracks:
        label, color, marker = styles[method]
        ax.plot(xs, ys, color=color, linewidth=2.5, solid_capstyle='round', zorder=2)
        ax.scatter(xs, ys, s=52, marker=marker, color=color, edgecolor=SURFACE, linewidth=1.0, zorder=3)
        for index, (k, x, y) in enumerate(zip(ks, xs, ys)):
            first_bok = method == 'bon16' and k == 1
            dx, dy = (-12, 0) if first_bok else (0, 9 if index % 2 == 0 else -14)
            ax.annotate(str(k), (x, y), xytext=(dx, dy), textcoords='offset points',
                        ha='center', va='center' if first_bok else ('bottom' if dy > 0 else 'top'),
                        fontsize=8, color=color, fontweight='bold' if k in (1, 16) else 'normal')
        if method == 'bon16':
            _, direct_color, direct_marker = styles['direct']
            ax.scatter(cost['direct'], direct_y, s=68, marker=direct_marker, color=direct_color,
                       edgecolor=SURFACE, linewidth=1.0, zorder=4)
            ax.annotate('Direct', (cost['direct'], direct_y), xytext=(0, 8), textcoords='offset points',
                        ha='center', va='bottom', fontsize=9, color=direct_color)
            all_y = ys + [direct_y]
        else:
            all_y = ys
        margin = max(3, (max(all_y) - min(all_y)) * 0.22)
        ax.set_ylim(max(0, min(all_y) - margin), min(100, max(all_y) + margin))
        ax.set_xlim(0, max(xs) * 1.08)
        ax.set_title(title, loc='left', fontsize=11, fontweight='bold', color=color, pad=8)
        ax.set_ylabel('Pass@1 (%)', fontsize=11)
        ax.set_xlabel('Tokens / problem (linear scale)', fontsize=10)
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda value, _: f'{value / 1000:g}k' if value >= 1000 else f'{value:g}'))
        ax.grid(False)
        ax.tick_params(labelsize=9)
    handles = [
        Line2D([], [], marker=marker, color=color, linewidth=2.0, markersize=7,
               markeredgecolor=SURFACE, markeredgewidth=0.9, label=label)
        for label, color, marker in styles.values()
    ]
    fig.suptitle(f'{model_label} · {dataset_label}', y=0.99, fontsize=16, fontweight='bold')
    fig.legend(handles=handles, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.955),
               fontsize=10.5, columnspacing=1.7)
    fig.text(0.99, 0.01, 'Number on each colored marker = $k$ (1–16); the two tracks have independent linear token axes.',
             ha='right', va='bottom', fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 0.88), h_pad=1.65)
    save(fig, f'H3_budget_{model_key}_{dataset}', 'analysis_v3_3models.json (best_of_k, mcts_at_k, methods)')


def h3_cost_curve(A):
    for dataset, dataset_label in DATASETS:
        for model_key, model_label in MODELS:
            h3_budget_panel(A, model_key, model_label, dataset, dataset_label)




# ---------------------------------------------------------------------------------------------- H5
def h5_search_stages(A):
    """Offline selection trajectories on the same MCTS Dual candidate trees."""
    stages = (
        ('first_program', 'Ứng viên đầu tiên', '#767676'),
        ('no_critic', 'Sau search', '#0F4D92'),
        ('selected_local', 'Sau critic', '#9A4D8E'),
    )
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 5.2), sharex=True, sharey='row')
    x = [0, 1, 2]
    for row, (ds, dataset_label) in enumerate(DATASETS):
        for column, (model_key, model_label) in enumerate(MODELS):
            ax = axes[row][column]
            result = A[f'{model_key}/{ds}']
            offline, n = result['offline_mcts'], result['n']
            values = [100 * offline[key] / n for key, _, _ in stages]
            ax.plot(x, values, color=INK2, linewidth=1.8, zorder=1)
            for index, ((_, _, color), value) in enumerate(zip(stages, values)):
                ax.scatter(index, value, s=58, color=color, edgecolor=SURFACE, linewidth=1.0, zorder=3)
                ax.annotate(f'{value:.1f}', (index, value), xytext=(0, 7), textcoords='offset points',
                            ha='center', va='bottom', fontsize=8, color=color, fontweight='bold')
            search = offline['search_vs_first_program']
            critic = offline['critic_vs_no_critic']
            ax.text(
                0.5, 0.045, f"S +{search['wins']}/−{search['losses']}   C +{critic['wins']}/−{critic['losses']}",
                transform=ax.transAxes, ha='center', va='bottom', fontsize=7.2, color=INK2,
                bbox=dict(boxstyle='round,pad=0.23', facecolor=SURFACE, edgecolor=GRID, linewidth=0.6),
            )
            ax.set_title(model_label, loc='left', fontsize=10, fontweight='bold', pad=7)
            ax.set_xticks(x)
            ax.set_xticklabels(['Ứng viên\nđầu', 'Sau\nsearch', 'Sau\ncritic'], fontsize=7.5)
            ax.grid(axis='x', visible=False)
            ax.set_xlim(-0.25, 2.25)
            ax.set_ylim((0, 75) if ds == 'apps' else (70, 100))
            ax.set_yticks(range(0, 76, 20) if ds == 'apps' else range(70, 101, 10))
            if column == 0:
                ax.set_ylabel(f'{dataset_label}\nPass@1 (%)', fontsize=9.5)
    handles = [
        Line2D([], [], color=INK2, marker='o', markerfacecolor=color, markeredgecolor=SURFACE,
               markeredgewidth=1.0, linewidth=1.8, markersize=7, label=label.replace('\n', ' '))
        for _, label, color in stages
    ]
    fig.legend(handles=handles, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.025), fontsize=9.5)
    fig.text(0.5, 0.005, 'S/C: số bài thắng/thua ghép cặp của search/critic so với bước liền trước',
             ha='center', va='bottom', fontsize=7.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.045, 1, 0.94), w_pad=1.0, h_pad=1.35)
    save(fig, 'H5_mcts_stages', 'analysis_v3_3models.json (offline_mcts)',
         'Ba bước dùng cùng candidate tree của MCTS Dual và cùng local hidden judge; đây là chọn lại offline, không phải ba run độc lập.')


# ---------------------------------------------------------------------------------------------- H6
def h6_tokens_by_role():
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 5.1), sharey=True, sharex='row')
    role_hatch = dict(zip((role for role, _ in ROLES), ('///', '', '\\\\\\', 'xx', '..')))
    role_data = {
        (ds, mk): role_tokens(f'v3_{ds}_{mk}_mcts')
        for ds, _ in DATASETS for mk, _ in MODELS
    }
    for row, (ds, dataset_label) in enumerate(DATASETS):
        row_max = max(
            sum(role_data[(ds, mk)].get((role, kind), 0) for role, _ in ROLES)
            for mk, _ in MODELS for kind in ('input', 'output')
        ) / 1000
        for col, (model_key, model_label) in enumerate(MODELS):
            ax = axes[row, col]
            tokens = role_data[(ds, model_key)]
            for y, kind in ((1, 'input'), (0, 'output')):
                left = 0
                for role, _ in ROLES:
                    value = tokens.get((role, kind), 0) / 1000
                    if value:
                        ax.barh(y, value, left=left, height=0.56, color=ROLE_COLOR[role],
                                edgecolor=INK, linewidth=0.65, hatch=role_hatch[role])
                    left += value
                ax.annotate(f'{vn(left, 1)}k', (left, y), xytext=(3, 0), textcoords='offset points',
                            fontsize=8.2, color=INK2, va='center', fontweight='bold')
            ax.set_xlim(0, row_max * 1.19)
            ax.set_yticks((1, 0), ('Input', 'Output'))
            ax.set_title(model_label, loc='left', fontsize=10, fontweight='bold', pad=7)
            ax.grid(axis='y', visible=False)
            ax.tick_params(labelsize=8.5)
            if col == 0:
                ax.set_ylabel(dataset_label, fontsize=10, fontweight='bold', color=INK2)
            ax.set_xlabel('Nghìn token / bài', fontsize=9)
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=ROLE_COLOR[role], edgecolor=INK,
                      linewidth=0.65, hatch=role_hatch[role], label=label)
        for role, label in ROLES
    ]
    fig.legend(handles=handles, loc='upper center', ncol=5, bbox_to_anchor=(0.5, 1.005),
               fontsize=9, columnspacing=1.1, handlelength=2, handleheight=1.1)
    fig.text(0.5, 0.012, 'Giá trị cuối mỗi thanh là tổng token trung bình; màu và họa tiết phân biệt vai trò request LLM.',
             ha='center', va='bottom', fontsize=7.7, color=MUTED)
    fig.tight_layout(rect=(0, 0.06, 1, 0.91), w_pad=1.1, h_pad=1.55)
    save(fig, 'H6_mcts_tokens_by_role', 'runs/v3_raw_archives/v3_*_mcts.heavy.tar.gz (requests.json)')


def main():
    A = json.loads(ANALYSIS.read_text())
    h1_pass_at_1(A)
    h2_forest(A)
    h3_cost_curve(A)
    h5_search_stages(A)
    h6_tokens_by_role()


if __name__ == '__main__':
    main()
