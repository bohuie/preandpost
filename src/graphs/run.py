from src.graphs.chart import chart


CATEGORIES = {
    "Security": {
        "rating_metric": "security_rating",
        "line_metrics": ["vulnerabilities"],
        "y_label": "Average vulnerabilities per repo",
    },
    "Reliability": {
        "rating_metric": "reliability_rating",
        "line_metrics": ["bugs"],
        "y_label": "Average bugs per repo",
    },
    "Maintainability": {
        "rating_metric": "sqale_rating",
        "line_metrics": ["code_smells", "sqale_index", "sqale_debt_ratio"],
        "y_label": "Average maintainability metrics per repo",
    },
    "Duplications": {
        "line_metrics": ["duplicated_lines_density", "duplicated_lines", "duplicated_blocks", "duplicated_files"],
        "y_label": "Average duplication metrics per repo",
        "y_tick_interval": 250,
    },
    "Size": {
        "line_metrics": ["ncloc", "lines", "statements", "functions", "classes", "files", "comment_lines", "comment_lines_density"],
        "y_label": "Average size metrics per repo",
        "y_tick_interval": 4000,
    },
    "Complexity": {
        "line_metrics": ["complexity", "cognitive_complexity"],
        "y_label": "Average complexity per repo",
    },
}

LABEL_OVERRIDES = {
    "ncloc": "NCLOC",
    "sqale_index": "Technical debt",
    "sqale_debt_ratio": "Technical debt ratio",
}


def label_for(metric):
    return LABEL_OVERRIDES.get(metric, metric.replace("_", " ").capitalize())


def main():
    for title, config in CATEGORIES.items():
        metrics = config["line_metrics"]
        chart(
            title=title,
            line_metrics=metrics,
            line_labels={m: label_for(m) for m in metrics},
            y_label=config["y_label"],
            output_file=f"{title.lower()}.png",
            rating_metric=config.get("rating_metric"),
            y_tick_interval=config.get("y_tick_interval"),
        )


if __name__ == "__main__":
    main()

# Run:
# python -m src.graphs.run
