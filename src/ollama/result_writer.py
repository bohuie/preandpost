import csv
import json

from pathlib import Path


def save_metric_json(
    repository: str,
    metric: str,
    rows: list[dict] | dict,
) -> Path:
    output_dir = (
        Path("data")
        / "metric_results"
        / repository
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / f"{metric}.json"

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            rows,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return output_path


def save_metric_csv(
    repository: str,
    metric: str,
    rows: list[dict],
) -> Path:
    output_dir = (
        Path("output")
        / "metric_results"
        / repository
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / f"{metric}.csv"

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        fieldnames = ["path", metric]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    "path": row.get("path", ""),
                    metric: row.get(metric, ""),
                }
            )

    return output_path


def save_mismatches_csv(
    repository: str,
    metric: str,
    mismatches: list[dict],
) -> Path:
    output_dir = (
        Path("output")
        / "metric_results"
        / repository
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"{metric}_mismatches.csv"
    )

    fieldnames = [
        "path",
        "file_chunk_index",
        "expected_value",
        "ollama_value",
        "difference",
        "attempts",
    ]

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(mismatches)

    return output_path


def save_aggregate_csv(
    repository: str,
    metric: str,
    value: int,
) -> Path:
    output_dir = (
        Path("output")
        / "metric_results"
        / repository
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / f"{metric}.csv"

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[metric],
        )

        writer.writeheader()
        writer.writerow(
            {
                metric: value,
            }
        )

    return output_path