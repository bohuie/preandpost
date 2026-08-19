import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from src.graphs.data import load_chart_data
from src.graphs.style import (
    apply_piecewise_scale, draw_ai_line, draw_lines,
    draw_rating_bars, save_chart, max_line_value,
)


def chart(title, line_metrics, line_labels, y_label, output_file,
          rating_metric=None, y_tick_interval=None,
          custom_ticks=None, linear=False):
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
        ax_main.set_ylabel("Percentage of teams (%)")
        ax_main.set_ylim(0, 100)
        ax_line = ax_main.twinx()
    else:
        ax_line = ax_main
        if custom_ticks is not None:
            positives = [v for values in line_values.values() for v in values if v > 0]
            ylim = (min(positives) * 0.7, custom_ticks[-1] * 1.05) if positives else None
            apply_piecewise_scale(ax_line, custom_ticks, ylim=ylim)
        elif not linear:
            ax_line.set_yscale("log")

    draw_lines(ax_line, x, line_metrics, line_labels, line_values)
    ax_line.set_ylabel(y_label)

    if rating_metric:
        ax_line.set_ylim(0, max_line_value(line_values) * 1.35)
        if y_tick_interval is not None:
            ax_line.yaxis.set_major_locator(MultipleLocator(y_tick_interval))
    elif custom_ticks is not None:
        pass
    elif linear:
        ax_line.set_ylim(0, max_line_value(line_values) * 1.35)
    else:
        positive_values = [v for values in line_values.values() for v in values if v > 0]
        if positive_values:
            ax_line.set_ylim(min(positive_values) * 0.3, max(positive_values) * 4)

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
