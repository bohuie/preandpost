from src.ollama.metric_runner import run_metric
from src.ollama.prompts import COMMENT_DENSITY_PROMPT


if __name__ == "__main__":
    run_metric("comment_density_pct", COMMENT_DENSITY_PROMPT)
