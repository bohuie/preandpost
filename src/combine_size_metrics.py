"""
Combine saved metric JSON files into per-file and aggregate CSV files.
"""

import csv
import json
from pathlib import Path


REPOSITORY = "project-1-crm-for-non-profits-trellis-crm"
RESULT_DIR = Path("data") / "metric_results" / REPOSITORY
OUTPUT_DIR = Path("data") / "size_metrics"

METRICS = [
    "files",
    "lines",
    "ncloc",
    "comment_lines",
    "comment_density_pct",
    "statements",
    "functions",
    "classes",
]


def load_metric(metric: str) -> dict[str, int | float]:
    path = RESULT_DIR / f"{metric}.json"

    with open(path, "r", encoding="utf-8") as file:
        rows = json.load(file)

    return {
        row["path"]: row.get(metric, 0)
        for row in rows
    }


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    metric_data = {
        metric: load_metric(metric)
        for metric in METRICS
    }

    all_paths = sorted(
        set().union(
            *(data.keys() for data in metric_data.values())
        )
    )

    per_file_rows = []

    for file_path in all_paths:
        row = {"path": file_path}

        for metric in METRICS:
            row[metric] = metric_data[metric].get(file_path, 0)

        per_file_rows.append(row)

    aggregate = {"repository": REPOSITORY}

    for metric in METRICS:
        if metric == "comment_density_pct":
            continue

        aggregate[metric] = sum(
            float(row[metric])
            for row in per_file_rows
        )

    denominator = (
        aggregate["ncloc"]
        + aggregate["comment_lines"]
    )

    aggregate["comment_density_pct"] = (
        round(aggregate["comment_lines"] / denominator * 100, 2)
        if denominator
        else 0.0
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_csv(
        OUTPUT_DIR / f"{REPOSITORY}_per_file.csv",
        per_file_rows,
        ["path", *METRICS],
    )

    write_csv(
        OUTPUT_DIR / f"{REPOSITORY}_aggregate.csv",
        [aggregate],
        ["repository", *METRICS],
    )

    print(f"Per-file CSV : {OUTPUT_DIR / f'{REPOSITORY}_per_file.csv'}")
    print(f"Aggregate CSV: {OUTPUT_DIR / f'{REPOSITORY}_aggregate.csv'}")


if __name__ == "__main__":
    main()
