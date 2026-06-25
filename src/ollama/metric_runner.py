"""
Shared workflow used by every run_<metric>.py script.
"""

import csv
import json
from pathlib import Path

from src.ollama.ollama_client import ask_ollama


EXTRACTED_PATH = (
    "data/UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_content/project-1-crm-for-non-profits-trellis-crm.json"
)

FILE_LIST_PATH = (
    "data/UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_list/project-1-crm-for-non-profits-trellis-crm.json"
)

AST_PATH = (
    "data/UBCO-COSC499-Winter-2018-Term-1-2/"
    "analysis/project-1-crm-for-non-profits-trellis-crm.json"
)

def make_chunks(files: list[dict], chunk_size: int) -> list[list[dict]]:
    if chunk_size <= 0:
        return [files]
    return [
        files[index:index + chunk_size]
        for index in range(0, len(files), chunk_size)
    ]


def parse_response(raw: str, metric: str) -> list[dict]:
    result = json.loads(raw)

    if "files" not in result:
        raise KeyError("Ollama response does not contain 'files'.")

    rows = []

    for item in result["files"]:
        rows.append(
            {
                "path": item["path"],
                metric: item.get(metric, 0),
            }
        )

    return rows


def save_metric_result(
    repository: str,
    metric: str,
    rows: list[dict],
) -> Path:
    output_dir = Path("data") / "metric_results" / repository
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{metric}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2, ensure_ascii=False)

    return output_path


def save_metric_csv(
    repository: str,
    metric: str,
    data,
) -> Path:
    output_dir = Path("output") / "metric_results" / repository
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{metric}.csv"

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        if isinstance(data, list):
            # Per-file metric: rows of {path, <metric>}
            fieldnames = ["path", metric]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow({k: row.get(k, "") for k in fieldnames})
        elif isinstance(data, dict):
            # Aggregate metric: single row of {<metric>: total}
            fieldnames = list(data.keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)

    return output_path


def run_metric(
    metric: str,
    prompt_template: str,
    chunk_size: int = 3,
    top_n: int = 0,
) -> None:
    with open(EXTRACTED_PATH, "r", encoding="utf-8") as file:
        extracted = json.load(file)

    repository = extracted["repository"]
    chunks = make_chunks(extracted["files"], chunk_size)
    if top_n > 0:
        chunks = chunks[:top_n]
    rows = []

    print(f"Repository   : {repository}")
    print(f"Metric       : {metric}")
    print(f"Total files  : {len(extracted['files'])}")
    print(f"Total chunks : {len(chunks)}\n")

    for index, chunk in enumerate(chunks, start=1):
        payload = {
            "chunk_index": index,
            "file_count": len(chunk),
            "files": chunk,
        }

        prompt = prompt_template.format(
            chunk_json=json.dumps(payload, ensure_ascii=False)
        )

        print(f"[{index}/{len(chunks)}] Analyzing {len(chunk)} file(s)...")

        raw = None
        try:
            raw = ask_ollama(prompt)
            chunk_rows = parse_response(raw, metric)
        except Exception as error:
            print(f"  FAILED: {error}")
            print(f"  FILES IN CHUNK: {[f['path'] for f in chunk]}")
            if raw is not None:
                print(f"  RAW (first 500 chars): {raw[:500]!r}")
            continue

        rows.extend(chunk_rows)

        for row in chunk_rows:
            print(f"  {row['path']}: {row[metric]}")

    result_path = save_metric_result(repository, metric, rows)
    csv_path = save_metric_csv(repository, metric, rows)
    total = sum(float(row[metric]) for row in rows)

    print("\nSummary")
    print("-------")
    print(f"Files analyzed : {len(rows)}")
    print(f"Total {metric} : {total:g}")
    print(f"Saved JSON     : {result_path}")
    print(f"Saved CSV      : {csv_path}")


def load_ast_files(ast_path: str) -> tuple[str, list[dict]]:
    with open(ast_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    by_path: dict[str, list[dict]] = {}
    for chunk in data["chunks"]:
        path = chunk["path"]
        chunk_meta = chunk["chunk"]
        if path not in by_path:
            by_path[path] = []
        by_path[path].append(
            {
                "start_line": chunk_meta["start_line"],
                "end_line": chunk_meta["end_line"],
            }
        )

    files = [
        {"path": path, "chunks": chunks}
        for path, chunks in by_path.items()
    ]
    return data["repository"], files


def run_metric_from_ast(
    metric: str,
    prompt_template: str,
    chunk_size: int = 3,
    top_n: int = 0,
) -> None:
    repository, files = load_ast_files(AST_PATH)
    batches = make_chunks(files, chunk_size)
    if top_n > 0:
        batches = batches[:top_n]
    rows = []

    print(f"Repository    : {repository}")
    print(f"Metric        : {metric}")
    print(f"Source        : AST output ({AST_PATH})")
    print(f"Total files   : {len(files)}")
    print(f"Batch size    : {chunk_size} file(s) per Ollama call")
    print(f"Total batches : {len(batches)}\n")

    for index, batch in enumerate(batches, start=1):
        payload = {
            "chunk_index": index,
            "file_count": len(batch),
            "files": batch,
        }

        prompt = prompt_template.format(
            chunk_json=json.dumps(payload, ensure_ascii=False)
        )

        print(f"[{index}/{len(batches)}] Analyzing {len(batch)} file(s)...")

        raw = None
        try:
            raw = ask_ollama(prompt)
            batch_rows = parse_response(raw, metric)
        except Exception as error:
            print(f"  FAILED: {error}")
            print(f"  FILES IN BATCH: {[f['path'] for f in batch]}")
            if raw is not None:
                print(f"  RAW (first 500 chars): {raw[:500]!r}")
            continue

        rows.extend(batch_rows)

        for row in batch_rows:
            print(f"  {row['path']}: {row[metric]}")

    result_path = save_metric_result(repository, metric, rows)
    csv_path = save_metric_csv(repository, metric, rows)
    total = sum(float(row[metric]) for row in rows)

    print("\nSummary")
    print("-------")
    print(f"Files analyzed : {len(rows)}")
    print(f"Total {metric} : {total:g}")
    print(f"Saved JSON     : {result_path}")
    print(f"Saved CSV      : {csv_path}")


def run_aggregate_metric(
    metric: str,
    prompt_template: str,
    chunk_size: int = 0,
    top_n: int = 0,
) -> None:
    with open(FILE_LIST_PATH, "r", encoding="utf-8") as file:
        extracted = json.load(file)

    repository = extracted["repository"]
    chunks = make_chunks(extracted["filenames"], chunk_size)
    if top_n > 0:
        chunks = chunks[:top_n]

    print(f"Repository      : {repository}")
    print(f"Metric          : {metric}")
    print(f"Total filenames : {len(extracted['filenames'])}")
    print(f"Total chunks    : {len(chunks)}\n")

    total = 0

    for index, chunk in enumerate(chunks, start=1):
        payload = {
            "chunk_index": index,
            "filename_count": len(chunk),
            "filenames": chunk,
        }

        prompt = prompt_template.format(
            chunk_json=json.dumps(payload, ensure_ascii=False)
        )

        print(f"[{index}/{len(chunks)}] Counting {len(chunk)} filename(s)...")

        try:
            raw = ask_ollama(prompt)
            value = int(json.loads(raw)[metric])
        except Exception as error:
            print(f"  FAILED: {error}")
            continue

        total += value
        print(f"  chunk {index}: {value}")

    result_path = save_metric_result(repository, metric, {metric: total})
    csv_path = save_metric_csv(repository, metric, {metric: total})

    print("\nSummary")
    print("-------")
    print(f"Total {metric} : {total}")
    print(f"Saved JSON     : {result_path}")
    print(f"Saved CSV      : {csv_path}")