"""
run_ollama_metrics.py
Get file content from json → Get prompt from prompts.py → Send to Ollama via ollama_client.py → Save results

"""
import json

from src.ollama.prompts import SIZE_METRICS_PROMPT
from src.ollama.ollama_client import ask_ollama

file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/file_content/project-12-bus-advisory-offline-real-time-bus-location-tracker.json"

with open(file_path, "r", encoding="utf-8") as file:
    repo_data = json.load(file)     # Read the contents of a json file, then convert it into a Python dictionary

prompt = SIZE_METRICS_PROMPT.format(        # Create the final prompt to be sent to Ollama using the original data
    file_content_json=json.dumps(repo_data, ensure_ascii=False)   # Convert repo_data from a Python dictionary back to a json string
)

response = ask_ollama(prompt)
print(response)

# Run: python -m src.run_ollama_metrics