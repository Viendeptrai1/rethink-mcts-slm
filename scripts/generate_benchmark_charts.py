#!/usr/bin/env python3
"""
Generate publication-quality comparative benchmark charts for TLCN / Research Paper.
Compares Qwen2.5-Coder 7B vs 14B across APPS (300 problems) and HumanEval (164 problems).
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Set overall publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

OUTPUT_DIR = "docs/results/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Data definition
categories = ['Introductory\n(100)', 'Interview\n(100)', 'Competition\n(100)', 'Overall\n(300)']

# Pass@1 (%)
p1_7b_direct = [31.00, 7.00, 4.00, 14.00]
p1_7b_dual = [38.00, 14.00, 5.00, 19.00]
p1_7b_test_only = [41.00, 18.00, 9.00, 22.67]
p1_14b_dual = [53.00, 27.00, 28.00, 36.00]

# Hidden Pass Rate (%)
hpr_7b_direct = [45.84, 26.18, 19.52, 30.51]
hpr_7b_dual = [56.70, 42.36, 30.07, 43.04]
hpr_7b_test_only = [61.14, 45.46, 29.42, 45.34]
hpr_14b_dual = [71.26, 50.13, 39.08, 53.49]

# Color Palette (Modern Academic Palette)
c_7b_direct = '#94a3b8'     # Slate gray (Baseline)
c_7b_dual = '#3b82f6'       # Vibrant Blue
c_7b_test_only = '#06b6d4'  # Cyan / Teal
c_14b_dual = '#8b5cf6'      # Deep Purple / Indigo (Hero 14B)

# -------------------------------------------------------------
# FIGURE 1: APPS Pass@1 Comparison (Grouped Bar Chart)
# -------------------------------------------------------------
def plot_figure_1():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(categories))
    width = 0.20
    
    rects1 = ax.bar(x - 1.5*width, p1_7b_direct, width, label='7B Direct (Baseline)', color=c_7b_direct, edgecolor='white', linewidth=1.2)
    rects2 = ax.bar(x - 0.5*width, p1_7b_dual, width, label='7B RethinkMCTS Dual', color=c_7b_dual, edgecolor='white', linewidth=1.2)
    rects3 = ax.bar(x + 0.5*width, p1_7b_test_only, width, label='7B RethinkMCTS Test-only', color=c_7b_test_only, edgecolor='white', linewidth=1.2)
    rects4 = ax.bar(x + 1.5*width, p1_14b_dual, width, label='14B RethinkMCTS Dual (Ours)', color=c_14b_dual, edgecolor='white', linewidth=1.2, zorder=3)
    
    ax.set_ylabel('Pass@1 Accuracy (%)')
    ax.set_title('APPS Benchmark (300 Problems): Pass@1 Accuracy by Difficulty Level', pad=18)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 62)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(100, decimals=0))
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper right', fontsize=10)
    
    # Value annotations on bars
    for rects in [rects1, rects2, rects3, rects4]:
        for bar in rects:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='semibold')
            
    # Key Highlights: Jump annotations
    # 1. Competition Jump (5% -> 28%)
    ax.annotate('+23.0%\n(5.6x)',
                xy=(x[2] + 1.5*width, 28.0), xytext=(x[2] + 0.8*width, 42.0),
                arrowprops=dict(facecolor='#7c3aed', shrink=0.08, width=1.5, headwidth=6),
                ha='center', fontsize=9, fontweight='bold', color='#6d28d9',
                bbox=dict(boxstyle="round,pad=0.3", fc="#f5f3ff", ec="#c4b5fd", lw=1.2))
    
    # 2. Overall Jump (19% -> 36%)
    ax.annotate('+17.0%\n(1.9x)',
                xy=(x[3] + 1.5*width, 36.0), xytext=(x[3] + 0.8*width, 48.0),
                arrowprops=dict(facecolor='#7c3aed', shrink=0.08, width=1.5, headwidth=6),
                ha='center', fontsize=9, fontweight='bold', color='#6d28d9',
                bbox=dict(boxstyle="round,pad=0.3", fc="#f5f3ff", ec="#c4b5fd", lw=1.2))

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "apps_pass_at_1_comparison.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# FIGURE 2: Hidden Test Pass Rate (Macro Mean Pass Rate)
# -------------------------------------------------------------
def plot_figure_2():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(categories))
    width = 0.20
    
    rects1 = ax.bar(x - 1.5*width, hpr_7b_direct, width, label='7B Direct (Baseline)', color=c_7b_direct, edgecolor='white', linewidth=1.2)
    rects2 = ax.bar(x - 0.5*width, hpr_7b_dual, width, label='7B RethinkMCTS Dual', color=c_7b_dual, edgecolor='white', linewidth=1.2)
    rects3 = ax.bar(x + 0.5*width, hpr_7b_test_only, width, label='7B RethinkMCTS Test-only', color=c_7b_test_only, edgecolor='white', linewidth=1.2)
    rects4 = ax.bar(x + 1.5*width, hpr_14b_dual, width, label='14B RethinkMCTS Dual (Ours)', color=c_14b_dual, edgecolor='white', linewidth=1.2, zorder=3)
    
    ax.set_ylabel('Mean Hidden Test Pass Rate (%)')
    ax.set_title('APPS Benchmark: Macro Mean Hidden Test Pass Rate Across Test Suites', pad=18)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 82)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(100, decimals=0))
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper right', fontsize=10)
    
    for rects in [rects1, rects2, rects3, rects4]:
        for bar in rects:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='semibold')
            
    # Highlight 71.26% Intro
    ax.annotate('71.3% Hidden Tests\nResolved on Intro',
                xy=(x[0] + 1.5*width, 71.26), xytext=(x[0] + 1.8*width, 76.0),
                arrowprops=dict(facecolor='#7c3aed', shrink=0.08, width=1.5, headwidth=6),
                ha='left', fontsize=9, fontweight='bold', color='#6d28d9',
                bbox=dict(boxstyle="round,pad=0.3", fc="#f5f3ff", ec="#c4b5fd", lw=1.2))

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "apps_hidden_pass_rate_comparison.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# FIGURE 3: Dual Benchmark Scaling (HumanEval vs APPS Overall)
# -------------------------------------------------------------
def plot_figure_3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    
    # Subplot A: HumanEval (164 problems)
    he_labels = ['7B Direct', '7B Test-only', '7B Dual', '14B Direct', '14B BoN-3', '14B Dual']
    he_scores = [80.49, 89.63, 91.46, 90.24, 91.46, 93.29]
    he_colors = [c_7b_direct, c_7b_test_only, c_7b_dual, '#cbd5e1', '#a78bfa', c_14b_dual]
    
    bars1 = ax1.bar(he_labels, he_scores, color=he_colors, edgecolor='white', linewidth=1.2)
    ax1.set_ylabel('Pass@1 Accuracy (%)')
    ax1.set_title('A. HumanEval Benchmark (164 Problems)\nModel Scaling vs Search Synergy', pad=12)
    ax1.set_ylim(70, 98)
    ax1.set_xticks(range(len(he_labels)))
    ax1.set_xticklabels(he_labels, rotation=30, ha='right')
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(100, decimals=0))
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}%',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='semibold')
        
    # Annotation on Subplot A: 7B Dual > 14B Direct
    ax1.annotate('7B MCTS (91.5%)\n> 14B Direct (90.2%)',
                 xy=(2, 91.46), xytext=(1.5, 94.5),
                 arrowprops=dict(facecolor='#2563eb', shrink=0.08, width=1.5, headwidth=5),
                 ha='center', fontsize=8.5, fontweight='bold', color='#1d4ed8',
                 bbox=dict(boxstyle="round,pad=0.25", fc="#eff6ff", ec="#bfdbfe", lw=1))

    # Subplot B: APPS Overall (300 problems)
    apps_labels = ['7B Direct', '7B Dual', '7B Test-only', '14B Dual']
    apps_p1 = [14.00, 19.00, 22.67, 36.00]
    apps_colors = [c_7b_direct, c_7b_dual, c_7b_test_only, c_14b_dual]
    
    bars2 = ax2.bar(apps_labels, apps_p1, color=apps_colors, edgecolor='white', linewidth=1.2)
    ax2.set_ylabel('Pass@1 Accuracy (%)')
    ax2.set_title('B. APPS Overall Benchmark (300 Problems)\nImpact of Model Capacity in Complex Algorithms', pad=12)
    ax2.set_ylim(0, 45)
    ax2.set_xticks(range(len(apps_labels)))
    ax2.set_xticklabels(apps_labels, rotation=30, ha='right')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(100, decimals=0))
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f'{h:.1f}%',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='semibold')

    ax2.annotate('+17.0% Gain\n(Nearly Double)',
                 xy=(3, 36.0), xytext=(2.4, 40.0),
                 arrowprops=dict(facecolor='#7c3aed', shrink=0.08, width=1.5, headwidth=5),
                 ha='center', fontsize=8.5, fontweight='bold', color='#6d28d9',
                 bbox=dict(boxstyle="round,pad=0.25", fc="#f5f3ff", ec="#c4b5fd", lw=1))

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "cross_benchmark_scaling.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# FIGURE 4: Distribution of Hidden Pass Rates (14B APPS Run)
# -------------------------------------------------------------
def plot_figure_4():
    unified_summary_path = "runs/benchmark_apps_14b_dual_unified/summary.json"
    if not os.path.exists(unified_summary_path):
        print(f"Skipping Figure 4: {unified_summary_path} not found.")
        return
        
    with open(unified_summary_path) as f:
        data = json.load(f)
        
    rates = [r.get('hidden_pass_rate', 0.0) * 100 for r in data.get('results', [])]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    
    # Left: Histogram
    bins = [0, 1e-6, 25, 50, 75, 99.99, 100.1]
    bin_labels = ['0%', '0.1-25%', '25-50%', '50-75%', '75-99%', '100%\n(Full Pass)']
    counts, _ = np.histogram(rates, bins=bins)
    
    bar_colors = ['#f87171', '#fb923c', '#facc15', '#a3e635', '#38bdf8', '#8b5cf6']
    bars = ax1.bar(bin_labels, counts, color=bar_colors, edgecolor='white', linewidth=1.2)
    ax1.set_title('A. 14B APPS: Distribution of Hidden Pass Rate per Problem', pad=12)
    ax1.set_ylabel('Number of Problems')
    ax1.set_xlabel('Hidden Test Pass Rate Range')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f'{h}',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='semibold')
        
    # Right: Cumulative Distribution Function (CDF)
    sorted_rates = np.sort(rates)
    cdf = np.arange(1, len(sorted_rates) + 1) / len(sorted_rates) * 100
    
    ax2.plot(sorted_rates, cdf, color='#8b5cf6', lw=2.5, label='14B RethinkMCTS Dual')
    ax2.axvline(100, color='#10b981', linestyle=':', lw=1.5, label='100% Pass Threshold')
    ax2.axhline(100 - (108/300*100), color='#6366f1', linestyle='--', alpha=0.7, label='Pass@1 Boundary (36.0%)')
    
    ax2.set_title('B. Cumulative Distribution Function (CDF)', pad=12)
    ax2.set_xlabel('Hidden Test Pass Rate (%)')
    ax2.set_ylabel('Cumulative Percent of Cohort (%)')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(100, decimals=0))
    ax2.xaxis.set_major_formatter(mtick.PercentFormatter(100, decimals=0))
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "apps_14b_pass_rate_distribution.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    plot_figure_1()
    plot_figure_2()
    plot_figure_3()
    plot_figure_4()
    print("All benchmark comparison charts successfully created!")
