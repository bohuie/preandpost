from src.ollama.chunked_metric_runner import (
    run_chunked_metric,
)
from src.ollama.metric_config import LINES_CONFIG
from src.ollama.prompts import LINES_PROMPT


INPUT_PATH = (
    "/Users/aliyahnurdafika/Library/CloudStorage/"
    "OneDrive-UBC/File Hui, Bowen - repo data/"
    "UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_content/"
    "project-4-direct-geo-referencing.json"
)


if __name__ == "__main__":
    run_chunked_metric(
        config=LINES_CONFIG,
        prompt_template=LINES_PROMPT,
        input_path=INPUT_PATH,
        lines_per_chunk=100,
        chunks_per_call=1,
        max_attempts=1,
    )


# Run:
# python -m src.run_lines
