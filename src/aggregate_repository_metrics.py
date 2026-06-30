import csv
import json

from pathlib import Path


PER_FILE_METRICS = [
    "lines",
    "comment_lines",
    "blank_lines",
    "ncloc",
    "statements",
    "functions",
    "classes",
]

AGGREGATE_METRICS = [
    "files",
]


def read_per_file_metric(
    repository: str,
    metric: str,
) -> int:
    """
    Read a per-file metric CSV and sum all values.
    """
    csv_path = (
        Path("output")
        / "metric_results"
        / repository
        / f"{metric}.csv"
    )

    if not csv_path.exists():
        print(
            f"WARNING: Missing metric file: {csv_path}"
        )
        return 0

    total = 0

    with open(
        csv_path,
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            value = row.get(metric, "")

            if value == "":
                continue

            total += int(float(value))

    return total


def read_aggregate_metric(
    repository: str,
    metric: str,
) -> int:
    """
    Read a metric that already contains one repository-level value.
    """
    csv_path = (
        Path("output")
        / "metric_results"
        / repository
        / f"{metric}.csv"
    )

    if not csv_path.exists():
        print(
            f"WARNING: Missing metric file: {csv_path}"
        )
        return 0

    with open(
        csv_path,
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        row = next(reader, None)

    if row is None:
        return 0

    value = row.get(metric, "")

    if value == "":
        return 0

    return int(float(value))


def build_repository_summary(
    repository: str,
) -> dict:
    summary = {
        "repository": repository,
    }

    for metric in AGGREGATE_METRICS:
        summary[metric] = read_aggregate_metric(
            repository=repository,
            metric=metric,
        )

    for metric in PER_FILE_METRICS:
        summary[metric] = read_per_file_metric(
            repository=repository,
            metric=metric,
        )

    return summary



def save_repository_summary_csv(
    repository: str,
    summary: dict,
) -> Path:
    output_dir = (
        Path("output")
        / "repository_results"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"{repository}.csv"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(summary.keys()),
        )

        writer.writeheader()
        writer.writerow(summary)

    return output_path


def save_repository_summary_json(
    repository: str,
    summary: dict,
) -> Path:
    output_dir = (
        Path("data")
        / "repository_results"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"{repository}.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return output_path