import json

from src.ollama.chunking import (
    make_batches,
    make_content_line_chunks,
)
from src.ollama.metric_config import MetricConfig
from src.ollama.ollama_client import ask_ollama
from src.ollama.response_parser import parse_chunk_response
from src.ollama.result_writer import (
    save_metric_csv,
    save_metric_json,
    save_mismatches_csv,
)
from src.ollama.validation import (
    validate_chunk_identity,
)

def analyze_batch_with_retry(
    batch: list[dict],
    prompt_template: str,
    config: MetricConfig,
    max_attempts: int = 3,
) -> tuple[list[dict], list[dict]]:
    last_error: Exception | None = None
    last_raw: str | None = None
    last_rows: list[dict] | None = None
    last_mismatches: list[dict] = []

    for attempt in range(
        1,
        max_attempts + 1,
    ):
        payload = {
            "chunk_count": len(batch),
            "chunks": batch,
        }

        prompt = prompt_template.format(
            chunk_json=json.dumps(
                payload,
                ensure_ascii=False,
            )
        )

        try:
            last_raw = ask_ollama(prompt)

            rows = parse_chunk_response(
                raw=last_raw,
                metric=config.name,
            )

            if len(rows) != len(batch):
                raise ValueError(
                    "Output count does not match input "
                    f"count: expected {len(batch)}, "
                    f"received {len(rows)}."
                )

            mismatches: list[dict] = []

            for input_chunk, output_row in zip(
                batch,
                rows,
            ):
                validate_chunk_identity(
                    input_chunk,
                    output_row,
                )

                if (
                    config.validate_against_expected
                    and config.expected_value_function
                    is not None
                ):
                    expected = (
                        config.expected_value_function(
                            input_chunk
                        )
                    )

                    actual = output_row[config.name]

                    if actual != expected:
                        mismatches.append(
                            {
                                "path": (
                                    input_chunk["path"]
                                ),
                                "file_chunk_index": (
                                    input_chunk[
                                        "file_chunk_index"
                                    ]
                                ),
                                "expected_value": expected,
                                "ollama_value": actual,
                                "difference": (
                                    actual - expected
                                ),
                                "attempts": attempt,
                            }
                        )

            last_rows = rows
            last_mismatches = mismatches

            if not mismatches:
                return rows, []

            print(
                f"  Attempt {attempt}/"
                f"{max_attempts} returned "
                f"{len(mismatches)} mismatch(es)."
            )

        except Exception as error:
            last_error = error

            print(
                f"  Attempt {attempt}/"
                f"{max_attempts} failed: {error}"
            )

            if last_raw is not None:
                print(
                    "  RAW (first 500 chars): "
                    f"{last_raw[:500]!r}"
                )

    if last_rows is not None:
        for mismatch in last_mismatches:
            mismatch["attempts"] = max_attempts

        print(
            "  WARNING: Using final Ollama result "
            "despite remaining mismatches."
        )

        return last_rows, last_mismatches

    raise RuntimeError(
        f"Ollama produced no usable result after "
        f"{max_attempts} attempts. "
        f"Last error: {last_error}. "
        f"Last raw response: "
        f"{last_raw[:500]!r}"
        if last_raw is not None
        else (
            "Ollama produced no response after "
            f"{max_attempts} attempts. "
            f"Last error: {last_error}."
        )
    )

def aggregate_chunk_results(
    files: list[dict],
    chunk_results: list[dict],
    metric: str,
) -> list[dict]:
    """
    Sum chunk-level values into file-level values.
    """
    totals_by_path: dict[str, int] = {}

    for row in chunk_results:
        path = row["path"]

        totals_by_path[path] = (
            totals_by_path.get(path, 0)
            + int(row[metric])
        )

    return [
        {
            "path": file_item["path"],
            metric: totals_by_path[
                file_item["path"]
            ],
        }
        for file_item in files
        if file_item["path"] in totals_by_path
    ]


def run_chunked_metric(
    config: MetricConfig,
    prompt_template: str,
    input_path: str,
    lines_per_chunk: int = 100,
    chunks_per_call: int = 1,
    top_n: int = 0,
    max_attempts: int = 1,
) -> None:
    with open(
        input_path,
        "r",
        encoding="utf-8",
    ) as file:
        extracted = json.load(file)

    repository = extracted["repository"]
    files = extracted["files"]

    source_chunks = make_content_line_chunks(
        files=files,
        lines_per_chunk=lines_per_chunk,
    )

    request_batches = make_batches(
        items=source_chunks,
        batch_size=chunks_per_call,
    )

    if top_n > 0:
        request_batches = request_batches[:top_n]

    chunk_results: list[dict] = []
    mismatch_results: list[dict] = []

    print(f"Repository       : {repository}")
    print(f"Metric           : {config.name}")
    print(f"Source files     : {len(files)}")
    print(f"Lines per chunk  : {lines_per_chunk}")
    print(f"Content chunks   : {len(source_chunks)}")
    print(f"Chunks per call  : {chunks_per_call}")
    print(f"Ollama calls     : {len(request_batches)}\n")

    for index, batch in enumerate(
        request_batches,
        start=1,
    ):
        print(
            f"[{index}/{len(request_batches)}] "
            f"Analyzing {len(batch)} chunk(s)..."
        )

        try:
            rows, mismatches = (
                analyze_batch_with_retry(
                    batch=batch,
                    prompt_template=prompt_template,
                    config=config,
                    max_attempts=max_attempts,
                )
            )

        except Exception as error:
            print(f"  FAILED: {error}")
            print(
                "  CHUNKS: "
                f"{[(item['path'], item['file_chunk_index']) for item in batch]}"
            )
            continue

        chunk_results.extend(rows)
        mismatch_results.extend(mismatches)

        for row in rows:
            print(
                f"  {row['path']} "
                f"[chunk "
                f"{row['file_chunk_index']}]: "
                f"{row[config.name]}"
            )

    file_rows = aggregate_chunk_results(
        files=files,
        chunk_results=chunk_results,
        metric=config.name,
    )

    json_path = save_metric_json(
        repository=repository,
        metric=config.name,
        rows=file_rows,
    )

    csv_path = save_metric_csv(
        repository=repository,
        metric=config.name,
        rows=file_rows,
    )

    mismatch_path = save_mismatches_csv(
        repository=repository,
        metric=config.name,
        mismatches=mismatch_results,
    )

    total = sum(
        int(row[config.name])
        for row in file_rows
    )

    print("\nSummary")
    print("-------")
    print(f"Files analyzed : {len(file_rows)}")
    print(f"Total {config.name} : {total}")
    print(f"Mismatches     : {len(mismatch_results)}")
    print(f"Saved JSON     : {json_path}")
    print(f"Saved CSV      : {csv_path}")
    print(f"Mismatch CSV   : {mismatch_path}")