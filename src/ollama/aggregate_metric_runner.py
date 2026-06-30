import json

from src.ollama.chunking import make_batches
from src.ollama.ollama_client import ask_ollama
from src.ollama.response_parser import (
    parse_aggregate_response,
)
from src.ollama.result_writer import (
    save_aggregate_csv,
    save_metric_json,
)

def analyze_aggregate_batch(
    batch: list[str],
    chunk_index: int,
    metric: str,
    prompt_template: str,
    max_attempts: int = 1,
) -> tuple[int, dict | None]:
    """
    Send one filename/path batch to Ollama.

    The final Ollama result is retained even when it differs
    from the deterministic batch length.
    """
    expected = len(batch)

    payload = {
        "chunk_index": chunk_index,
        "path_count": expected,
        "paths": batch,
    }

    prompt = prompt_template.format(
        chunk_json=json.dumps(
            payload,
            ensure_ascii=False,
        )
    )

    last_error: Exception | None = None
    last_raw: str | None = None
    last_value: int | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            last_raw = ask_ollama(prompt)

            value = parse_aggregate_response(
                raw=last_raw,
                metric=metric,
            )

            last_value = value

            if value == expected:
                return value, None

            mismatch = {
                "chunk_index": chunk_index,
                "expected_value": expected,
                "ollama_value": value,
                "difference": value - expected,
                "attempts": attempt,
            }

            print(
                f"  Attempt {attempt}/{max_attempts} "
                f"returned a mismatch: "
                f"expected {expected}, received {value}."
            )

        except Exception as error:
            last_error = error

            print(
                f"  Attempt {attempt}/{max_attempts} "
                f"failed: {error}"
            )

            if last_raw is not None:
                print(
                    "  RAW (first 500 chars): "
                    f"{last_raw[:500]!r}"
                )

    if last_value is not None:
        return (
            last_value,
            {
                "chunk_index": chunk_index,
                "expected_value": expected,
                "ollama_value": last_value,
                "difference": last_value - expected,
                "attempts": max_attempts,
            },
        )

    raise RuntimeError(
        f"Ollama produced no usable result for "
        f"chunk {chunk_index}. "
        f"Last error: {last_error}."
    )




def run_aggregate_metric(
    metric: str,
    prompt_template: str,
    input_path: str,
    paths_per_chunk: int = 100,
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

    # Prefer complete paths.
    paths = extracted.get("paths")

    if paths is None:
        # Fallback for older file_list JSON files.
        paths = extracted.get("filenames", [])

    batches = make_batches(
        items=paths,
        batch_size=paths_per_chunk,
    )

    if top_n > 0:
        batches = batches[:top_n]

    total = 0
    mismatches: list[dict] = []
    failed_chunks: list[int] = []

    print(f"Repository       : {repository}")
    print(f"Metric           : {metric}")
    print(f"Total paths      : {len(paths)}")
    print(f"Paths per chunk  : {paths_per_chunk}")
    print(f"Ollama calls     : {len(batches)}\n")

    for index, batch in enumerate(
        batches,
        start=1,
    ):
        expected = len(batch)

        print(
            f"[{index}/{len(batches)}] "
            f"Counting {expected} path(s)..."
        )

        try:
            value, mismatch = analyze_aggregate_batch(
                batch=batch,
                chunk_index=index,
                metric=metric,
                prompt_template=prompt_template,
                max_attempts=max_attempts,
            )

        except Exception as error:
            print(f"  FAILED: {error}")
            failed_chunks.append(index)
            continue

        total += value

        print(
            f"  Expected: {expected}"
        )
        print(
            f"  Ollama  : {value}"
        )

        if mismatch is not None:
            mismatches.append(mismatch)

    json_path = save_metric_json(
        repository=repository,
        metric=metric,
        rows={
            metric: total,
        },
    )

    csv_path = save_aggregate_csv(
        repository=repository,
        metric=metric,
        value=total,
    )

    print("\nSummary")
    print("-------")
    print(f"Expected files : {sum(len(batch) for batch in batches)}")
    print(f"Ollama files   : {total}")
    print(f"Mismatches     : {len(mismatches)}")
    print(f"Failed chunks  : {len(failed_chunks)}")
    print(f"Saved JSON     : {json_path}")
    print(f"Saved CSV      : {csv_path}")