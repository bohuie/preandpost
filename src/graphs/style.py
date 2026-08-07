import os
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


BASE_DIR = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/SonarQube"
INPUT_CSV = os.path.join(BASE_DIR, "output", "aggregated.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

plt.rcParams.update({
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "axes.labelsize": 14,
    "legend.fontsize": 11,
})

GRADES = ["A", "B", "C", "D", "E"]

RATING_COLORS = {
    "A": "#00A65A",
    "B": "#7FBA00",
    "C": "#FFB300",
    "D": "#FF7043",
    "E": "#D32F2F",
}

RATING_LABELS = {
    "A": "A - Excellent",
    "B": "B - Good",
    "C": "C - Moderate",
    "D": "D - Poor",
    "E": "E - Critical",
}

LINE_COLORS = [
    "#1F1F1F", "#4C78A8", "#F58518", "#54A24B",
    "#B279A2", "#E45756", "#72B7B2", "#FF9DA6",
]


def format_number(value):
    if value >= 1000:
        return f"{value / 1000:.1f}K"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.2f}"


def max_line_value(line_values):
    all_values = [v for values in line_values.values() for v in values]
    return max(all_values) if all_values else 1


def draw_ai_line(ax, years):
    if 2023 not in years:
        return
    transition_x = years.index(2023) - 0.5
    ax.axvline(transition_x, color="red", linestyle="--", linewidth=2)
    ax.text(transition_x - 0.15, ax.get_ylim()[1] * 0.55, "AI era begins",
            color="red", fontsize=11, fontweight="bold",
            rotation=90, va="center", ha="right")


def draw_lines(ax, x, line_metrics, line_labels, line_values):
    offset = max_line_value(line_values) * 0.03
    for i, metric in enumerate(line_metrics):
        color = LINE_COLORS[i % len(LINE_COLORS)]
        values = line_values[metric]
        ax.plot(x, values, color=color, linewidth=3,
                marker="o", markersize=9, label=line_labels[metric],
                markerfacecolor="white", markeredgewidth=2.3)
        for xi, yi in zip(x, values):
            ax.text(xi, yi + offset, format_number(yi), ha="center", fontsize=8, color=color)


def draw_rating_bars(ax, x, rating_counts):
    bar_width = 0.15
    for i, grade in enumerate(GRADES):
        offset = (i - len(GRADES) / 2 + 0.5) * bar_width
        ax.bar(x + offset, rating_counts[grade], bar_width,
               label=RATING_LABELS[grade], color=RATING_COLORS[grade],
               edgecolor="white", linewidth=0.8)


def save_chart(fig, output_file):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_file)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output_path}")
