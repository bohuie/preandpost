from src.ollama.aggregate_metric_runner import (
    run_aggregate_metric,
)
from src.ollama.prompts import FILES_PROMPT


INPUT_PATH = (
    "/Users/aliyahnurdafika/Library/CloudStorage/"
    "OneDrive-UBC/File Hui, Bowen - repo data/"
    "UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_list/"
    "project-4-direct-geo-referencing.json"
)


if __name__ == "__main__":
    run_aggregate_metric(
        metric="files",
        prompt_template=FILES_PROMPT,
        input_path=INPUT_PATH,
        paths_per_chunk=20,
        max_attempts=1,
    )
# Run:
# python -m src.run_files
