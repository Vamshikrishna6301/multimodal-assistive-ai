import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3",
        "prompt": "What is transformer in AI?",
        "stream": False
    },
    timeout=60
)

print("\n--- LLM RESPONSE ---\n")
print(response.json()["response"])