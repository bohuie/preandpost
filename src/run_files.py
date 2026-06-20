from src.ollama.metric_runner import run_metric
from src.ollama.prompts import FILES_PROMPT


if __name__ == "__main__":
    run_metric("files", FILES_PROMPT)
