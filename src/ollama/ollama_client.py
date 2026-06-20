"""

Given a prompt → send it to Ollama → return the results

"""
# ollama list

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"


def ask_ollama(prompt: str) -> str:     # The program sends a prompt to the local Ollama
    response = requests.post(           # Sending HTTP requests
        OLLAMA_URL,
        json={                          # Data sent to Ollama in json format
            "model": MODEL_NAME,
            "prompt": prompt,
            "options": {
                "temperature": 0        # To make the Ollama ​​response consistent on every run
            },
            "stream": False,            # Ollama returns the answer all at once
        },
        timeout=300,                    # The program will wait for a response from Ollama for a maximum of 300 seconds, if not a timeout error will occur
    )

    # Checks whether the request was successful. If successful, the program continues; if not, the program stops
    response.raise_for_status()

    result = response.json()    # Converting the response from Ollama to a Python dictionary

    return result["response"]   # Takes the contents of the answer from Ollama, then returns it as output