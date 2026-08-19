import functools
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/SonarQube"
INPUT_CSV = os.path.join(BASE_DIR, "output", "aggregated.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

plt.rcParams.update({"xtick.labelsize": 15, "ytick.labelsize": 15, "axes.labelsize": 18, "legend.fontsize": 11})

GRADES = ["A", "B", "C", "D", "E"]
RATING_COLORS = {"A": "#00A65A", "B": "#7FBA00", "C": "#FFB300", "D": "#FF7043", "E": "#D32F2F"}
RATING_LABELS = {"A": "A - Excellent", "B": "B - Good", "C": "C - Moderate", "D": "D - Poor", "E": "E - Very Poor"}
LINE_COLORS = ["#1F1F1F", "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756", "#72B7B2", "#FF9DA6"]


def format_number(value, comma=False):
    if value >= 1000:
        return f"{int(value):,}" if comma else f"{value / 1000:.1f}K"
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}"

def max_line_value(line_values):
    return max((v for values in line_values.values() for v in values), default=1)

def draw_ai_line(ax, years):
    if 2023 not in years:
        return
    transition_x = years.index(2023) - 0.5
    ax.axvline(transition_x, color="red", linestyle="--", linewidth=2)
    y_lo, y_hi = ax.get_ylim()
    scale = ax.get_yscale()
    text_y = (y_lo * y_hi) ** 0.5 if scale == "log" else (100 if scale == "function" else y_hi * 0.55)
    ax.text(transition_x - 0.15, text_y, "AI era begins", color="red", fontsize=11,
            fontweight="bold", rotation=90, va="center", ha="right")

def draw_lines(ax, x, line_metrics, line_labels, line_values):
    is_nonlinear = ax.get_yscale() != "linear"
    linear_offset = max_line_value(line_values) * 0.03
    for i, metric in enumerate(line_metrics):
        color = LINE_COLORS[i % len(LINE_COLORS)]
        values = line_values[metric]
        ax.plot(x, values, color=color, linewidth=3, marker="o", markersize=9,
                label=line_labels[metric], markerfacecolor="white", markeredgewidth=2.3)
        for xi, yi in zip(x, values):
            text_y = yi * 1.18 if is_nonlinear and yi > 0 else yi + linear_offset
            ax.text(xi, text_y, format_number(yi), ha="center", fontsize=8, color=color)

def draw_rating_bars(ax, x, rating_counts):
    bar_width = 0.15
    for i, grade in enumerate(GRADES):
        offset = (i - len(GRADES) / 2 + 0.5) * bar_width
        ax.bar(x + offset, rating_counts[grade], bar_width, label=RATING_LABELS[grade],
               color=RATING_COLORS[grade], edgecolor="white", linewidth=0.8)

def piecewise_map(x, xs, ys):
    result = np.interp(x, xs, ys)
    if np.any(x < xs[0]):
        slope = (ys[1] - ys[0]) / (xs[1] - xs[0])
        result = np.where(x < xs[0], ys[0] + slope * (x - xs[0]), result)
    if np.any(x > xs[-1]):
        slope = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
        result = np.where(x > xs[-1], ys[-1] + slope * (x - xs[-1]), result)
    return result

def piecewise_forward(y, log_ticks, display):
    return piecewise_map(np.log10(np.clip(np.asarray(y, dtype=float), 1e-9, None)), log_ticks, display)

def piecewise_inverse(t, log_ticks, display):
    return 10 ** piecewise_map(np.asarray(t, dtype=float), display, log_ticks)

def apply_piecewise_scale(ax, ticks, ylim=None):
    ticks = np.asarray(ticks, dtype=float)
    log_ticks = np.log10(ticks)
    display = np.arange(len(ticks), dtype=float)
    forward = functools.partial(piecewise_forward, log_ticks=log_ticks, display=display)
    inverse = functools.partial(piecewise_inverse, log_ticks=log_ticks, display=display)
    ax.set_yscale("function", functions=(forward, inverse))
    ax.set_yticks(list(ticks))
    ax.set_yticklabels([format_number(t, comma=True) for t in ticks])
    if ylim is not None:
        ax.set_ylim(*ylim)

def save_chart(fig, output_file):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_file)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output_path}")
