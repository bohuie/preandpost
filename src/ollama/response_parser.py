import json


def clean_json_response(raw: str) -> str:
    """
    Remove optional markdown JSON fences from an Ollama response.
    """
    cleaned = raw.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    return cleaned


def parse_chunk_response(
    raw: str,
    metric: str,
) -> list[dict]:
    """
    Parse a generic chunk-level Ollama response.

    Expected output:
    {
        "chunks": [
            {
                "path": "...",
                "file_chunk_index": 1,
                "<metric>": 10
            }
        ]
    }
    """
    cleaned = clean_json_response(raw)
    result = json.loads(cleaned)

    if "chunks" not in result:
        raise KeyError(
            "Ollama response does not contain 'chunks'."
        )

    rows: list[dict] = []

    for item in result["chunks"]:
        if metric not in item:
            raise KeyError(
                f"Ollama response does not contain "
                f"metric {metric!r}."
            )

        rows.append(
            {
                "path": item["path"],
                "file_chunk_index": int(
                    item["file_chunk_index"]
                ),
                metric: int(item[metric]),
            }
        )

    return rows

def parse_aggregate_response(
    raw: str,
    metric: str,
) -> int:
    cleaned = clean_json_response(raw)
    result = json.loads(cleaned)

    if metric not in result:
        raise KeyError(
            f"Ollama response does not contain {metric!r}."
        )

    value = int(result[metric])

    if value < 0:
        raise ValueError(
            f"{metric!r} must be non-negative."
        )

    return value