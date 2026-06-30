def validate_chunk_identity(
    input_chunk: dict,
    output_row: dict,
) -> None:
    if output_row["path"] != input_chunk["path"]:
        raise ValueError(
            "Ollama changed the path: "
            f"expected {input_chunk['path']!r}, "
            f"received {output_row['path']!r}."
        )

    expected_index = (
        input_chunk["file_chunk_index"]
    )

    actual_index = (
        output_row["file_chunk_index"]
    )

    if actual_index != expected_index:
        raise ValueError(
            "Ollama changed file_chunk_index: "
            f"expected {expected_index}, "
            f"received {actual_index}."
        )