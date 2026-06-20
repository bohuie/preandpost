from src.ollama.metric_runner import run_metric
from src.ollama.prompts import CLASSES_PROMPT


if __name__ == "__main__":
    run_metric("classes", CLASSES_PROMPT)
