from typing import Any


def make_batches(
    items: list[Any],
    batch_size: int,
) -> list[list[Any]]:
    """
    Divide a list into batches.

    If batch_size <= 0, return all items in one batch.
    """
    if batch_size <= 0:
        return [items]

    return [
        items[index:index + batch_size]
        for index in range(0, len(items), batch_size)
    ]


def make_content_line_chunks(
    files: list[dict],
    lines_per_chunk: int = 100,
) -> list[dict]:
    """
    Divide source files into chunks based on physical lines.

    Every physical line receives a sequential number local
    to its chunk.
    """
    if lines_per_chunk <= 0:
        raise ValueError(
            "lines_per_chunk must be greater than zero."
        )

    chunks: list[dict] = []

    for file_item in files:
        path = file_item["path"]
        extension = file_item.get("extension", "")
        content = file_item.get("content", "")

        if content == "":
            chunks.append(
                {
                    "path": path,
                    "extension": extension,
                    "file_chunk_index": 1,
                    "is_empty_file": True,
                    "physical_lines": [],
                }
            )
            continue

        physical_lines = content.splitlines()

        for start in range(
            0,
            len(physical_lines),
            lines_per_chunk,
        ):
            selected_lines = physical_lines[
                start:start + lines_per_chunk
            ]

            formatted_lines = [
                {
                    "line_number": offset + 1,
                    "text": line,
                }
                for offset, line in enumerate(selected_lines)
            ]

            chunks.append(
                {
                    "path": path,
                    "extension": extension,
                    "file_chunk_index": (
                        start // lines_per_chunk
                    ) + 1,
                    "is_empty_file": False,
                    "physical_lines": formatted_lines,
                }
            )

    return chunks