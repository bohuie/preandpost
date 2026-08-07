import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from src.graphs.data import load_chart_data
from src.graphs.style import (
    draw_ai_line, draw_lines, draw_rating_bars, save_chart, max_line_value,
)


def chart(title, line_metrics, line_labels, y_label, output_file,
          rating_metric=None, y_tick_interval=None):
    years, line_values, rating_counts = load_chart_data(line_metrics, rating_metric)
    x = np.arange(len(years))

    fig, ax_main = plt.subplots(figsize=(13, 6.5))
    fig.suptitle(title, fontsize=18, fontweight="bold")
    ax_main.set_xlabel("Year")
    ax_main.set_xticks(x)
    ax_main.set_xticklabels(years)
    ax_main.grid(axis="y", linestyle="--", alpha=0.3)

    if rating_metric:
        draw_rating_bars(ax_main, x, rating_counts)
        ax_main.set_ylabel("Number of teams")
        ax_main.set_ylim(0, ax_main.get_ylim()[1] * 1.2)
        ax_line = ax_main.twinx()
    else:
        ax_line = ax_main

    draw_lines(ax_line, x, line_metrics, line_labels, line_values)
    ax_line.set_ylabel(y_label)
    ax_line.set_ylim(0, max_line_value(line_values) * 1.35)

    if y_tick_interval is not None:
        ax_line.yaxis.set_major_locator(MultipleLocator(y_tick_interval))

    draw_ai_line(ax_main, years)

    if rating_metric:
        h_bar, l_bar = ax_main.get_legend_handles_labels()
        h_line, l_line = ax_line.get_legend_handles_labels()
        fig.legend(h_bar + h_line, l_bar + l_line,
                   loc="lower center", ncol=8, bbox_to_anchor=(0.5, -0.02))
    else:
        ax_line.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4)

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    save_chart(fig, output_file)
