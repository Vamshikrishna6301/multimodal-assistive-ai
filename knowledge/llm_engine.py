import requests
import json
from core.response_model import UnifiedResponse


class LLMEngine:
    """
    Fast Local LLM Engine (TinyLlama Optimized)
    Used ONLY for reasoning questions.
    """

    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "tinyllama"
    TIMEOUT = 40

    def handle(self, decision: dict) -> UnifiedResponse:

        query = decision.get("target")

        if not query:
            return UnifiedResponse.error_response(
                category="knowledge",
                spoken_message="I did not receive a question.",
                error_code="NO_QUERY"
            )

        try:
            response = requests.post(
                self.OLLAMA_URL,
                json={
                    "model": self.MODEL_NAME,
                    "prompt": self._build_prompt(query),
                    "stream": False,
                    "options": {
                        "num_predict": 60,
                        "temperature": 0.2,
                        "num_ctx": 512,
                        "num_thread": 8
                    }
                },
                timeout=self.TIMEOUT
            )

            if response.status_code != 200:
                return UnifiedResponse.error_response(
                    category="knowledge",
                    spoken_message="Local AI model is not responding.",
                    error_code="LLM_CONNECTION_ERROR"
                )

            data = response.json()
            answer = data.get("response", "").strip()

            return UnifiedResponse.success_response(
                category="knowledge",
                spoken_message=self._shorten(answer)
            )

        except Exception:
            return UnifiedResponse.error_response(
                category="knowledge",
                spoken_message="Local AI model encountered an error.",
                error_code="LLM_EXCEPTION"
            )

    def _build_prompt(self, query: str):
        return f"""
Answer briefly in 2 short sentences maximum.
No paragraphs.
Question:
{query}
"""

    def _shorten(self, text: str):
        sentences = text.split(". ")
        if len(sentences) > 2:
            return ". ".join(sentences[:2])
        return text