from src.ollama.metric_runner import run_metric_from_ast
from src.ollama.prompts import LINES_PROMPT


if __name__ == "__main__":
    run_metric_from_ast("lines", LINES_PROMPT, chunk_size=3)

# Run: python -m src.run_lines
