"""
Shared workflow used by every run_<metric>.py script.
"""

import json
from pathlib import Path

from src.ollama.ollama_client import ask_ollama


EXTRACTED_PATH = (
    "data/UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_content/project-1-crm-for-non-profits-trellis-crm.json"
)

CHUNK_SIZE = 1


def make_chunks(files: list[dict]) -> list[list[dict]]:
    return [
        files[index:index + CHUNK_SIZE]
        for index in range(0, len(files), CHUNK_SIZE)
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


def run_metric(metric: str, prompt_template: str) -> None:
    with open(EXTRACTED_PATH, "r", encoding="utf-8") as file:
        extracted = json.load(file)

    repository = extracted["repository"]
    chunks = make_chunks(extracted["files"])
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

        try:
            raw = ask_ollama(prompt)
            chunk_rows = parse_response(raw, metric)
        except Exception as error:
            print(f"  FAILED: {error}")
            continue

        rows.extend(chunk_rows)

        for row in chunk_rows:
            print(f"  {row['path']}: {row[metric]}")

    result_path = save_metric_result(repository, metric, rows)
    total = sum(float(row[metric]) for row in rows)

    print("\nSummary")
    print("-------")
    print(f"Files analyzed : {len(rows)}")
    print(f"Total {metric} : {total:g}")
    print(f"Saved result   : {result_path}")
