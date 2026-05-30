import json
import urllib.error
import urllib.request


class OllamaClient:
    def __init__(self, model_name="mistral:latest"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def ask(self, document_text, question):
        prompt = self._build_prompt(document_text, question)

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }

        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data.get("response", "").strip()
        except urllib.error.URLError:
            raise ConnectionError(
                "Could not connect to Ollama. Make sure Ollama is running."
            )

    def _build_prompt(self, document_text, question):
        return f"""
Use the document below to answer the question.

If the answer is not in the document, say that you cannot find the answer in the document.

Document:
{document_text}

Question:
{question}

Answer:
""".strip()
