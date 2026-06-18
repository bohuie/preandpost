import csv
import json
from pathlib import Path

import requests

from src.ollama.prompts import SIZE_METRIC_CHUNK_PROMPT


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:latest"
CHUNK_SIZE = 3
NUM_CTX = 16_384

EXTRACTED_PATH = (
    "data/UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_content/project-1-crm-for-non-profits-trellis-crm.json"
)


def make_chunks(files: list[dict], chunk_size: int) -> list[list[dict]]:
    return [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]


def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "num_ctx": NUM_CTX,
                "temperature": 0,
                "seed": 42,
            },
        },
        timeout=600,
    )
    response.raise_for_status()
    return response.json()["response"]


def aggregate(rows: list[dict]) -> dict:
    fields = ["lines", "ncloc", "comment_lines",
              "statements", "functions", "classes"]
    totals = {f: sum(int(r.get(f, 0)) for r in rows) for f in fields}
    totals["files"] = len(rows)
    denom = totals["ncloc"] + totals["comment_lines"]
    totals["comment_density_pct"] = (
        round(totals["comment_lines"] / denom * 100, 2) if denom else 0.0
    )
    return totals


def save_csv(rows: list[dict], path: Path, fields: list[str],
             append: bool = False) -> None:
    write_header = not (append and path.exists())
    mode = "a" if append else "w"
    with open(path, mode, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if write_header:
            writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def main():
    with open(EXTRACTED_PATH, "r", encoding="utf-8") as f:
        extracted = json.load(f)    # Load json file content

    all_files = extracted["files"]  # Load all files
    skipped = [f["path"] for f in all_files if len(f["content"]) > 40_000]
    all_files = [f for f in all_files if len(f["content"]) <= 40_000]
    if skipped:
        print(f"Skipped {len(skipped)} file(s) > 40K chars (~10K token):")
        for p in skipped:
            print(f"  - {p}")
    extension_by_path = {f["path"]: f["extension"] for f in all_files}
    chunks = make_chunks(all_files, CHUNK_SIZE)

    print(f"Total file  : {len(all_files)}")
    print(f"Total chunk : {len(chunks)}")

    per_file_rows = []

    for index, chunk_files in enumerate(chunks, start=1):
        chunk_payload = {
            "chunk_index": index,
            "file_count": len(chunk_files),
            "files": chunk_files,
        }
        prompt = SIZE_METRIC_CHUNK_PROMPT.format(
            chunk_json=json.dumps(chunk_payload, ensure_ascii=False)
        )

        print(f"[{index}/{len(chunks)}] {len(chunk_files)} file ...", flush=True)
        raw = call_ollama(prompt)

        try:
            parsed = json.loads(raw)["files"]
        except (json.JSONDecodeError, KeyError):
            print(f"  PARSE FAIL. Raw response:\n{raw!r}\n")
            continue

        for entry in parsed:
            entry["repository"] = extracted["repository"]
            entry["extension"] = extension_by_path.get(entry.get("path"), "")
            per_file_rows.append(entry)

    # Create folder for the organization
    org_dir = Path("data") / extracted["owner"]
    org_dir.mkdir(parents=True, exist_ok=True)
    per_file_path = org_dir / "size_file.csv"
    # Create file for the aggregate data
    aggregate_path = Path("data") / "size_aggregate.csv"

    per_file_fields = ["repository", "path", "extension", "lines", "ncloc",
                       "comment_lines", "statements", "functions", "classes"]
    save_csv(per_file_rows, per_file_path, per_file_fields, append=True)

    totals = aggregate(per_file_rows)
    meta = {
        "owner": extracted["owner"],
        "repository": extracted["repository"],
        "default_branch": extracted["default_branch"],
    }
    aggregate_fields = ["owner", "repository", "default_branch", "files", "lines",
                        "ncloc", "comment_lines", "comment_density_pct",
                        "statements", "functions", "classes"]
    save_csv([{**meta, **totals}], aggregate_path, aggregate_fields, append=True)

    print(f"DONE - {len(per_file_rows)} row appended to {per_file_path}")
    print(f"       1 row appended to {aggregate_path}")


if __name__ == "__main__":
    main()


# Run: python -m src.run_size_metrics