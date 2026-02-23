import requests
import urllib.parse
import re
from core.response_model import UnifiedResponse


class KnowledgeEngine:
    """
    Production Wikipedia Knowledge Engine
    - Clean factual output
    - No conversational filler
    - Disambiguation resistant
    - Deterministic behavior
    """

    WIKI_OPENSEARCH_URL = "https://en.wikipedia.org/w/api.php"
    WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

    HEADERS = {
        "User-Agent": "AssistiveAI/1.0 (Educational Project)"
    }

    # ------------------------------------------------
    # PUBLIC ENTRY
    # ------------------------------------------------

    def handle(self, decision: dict) -> UnifiedResponse:

        query = decision.get("target")

        if not query or not self._is_valid_query(query):
            return UnifiedResponse.error_response(
                category="knowledge",
                spoken_message="That does not appear to be a valid question.",
                error_code="INVALID_QUERY"
            )

        try:
            summary = self._get_best_summary(query)

            if not summary:
                return UnifiedResponse.error_response(
                    category="knowledge",
                    spoken_message="I could not find a clear answer.",
                    error_code="NO_RESULT"
                )

            return UnifiedResponse.success_response(
                category="knowledge",
                spoken_message=self._shorten(summary)
            )

        except Exception:
            return UnifiedResponse.error_response(
                category="knowledge",
                spoken_message="I am unable to answer that right now.",
                error_code="KNOWLEDGE_ERROR"
            )

    # ------------------------------------------------
    # QUERY VALIDATION
    # ------------------------------------------------

    def _is_valid_query(self, query: str):

        stripped = query.strip()

        if len(stripped) < 3:
            return False

        if stripped.isdigit():
            return False

        if not any(char.isalnum() for char in stripped):
            return False

        return True

    # ------------------------------------------------
    # NORMALIZE QUERY
    # ------------------------------------------------

    def _normalize_query(self, query):

        query = query.lower().strip()

        prefixes = [
            "who is",
            "who was",
            "what is",
            "what was",
            "explain",
            "tell me about",
            "define",
        ]

        for prefix in prefixes:
            if query.startswith(prefix):
                query = query[len(prefix):].strip()
                break

        query = query.replace("?", "").strip()

        return query

    # ------------------------------------------------
    # GET BEST SUMMARY
    # ------------------------------------------------

    def _get_best_summary(self, query):

        normalized_query = self._normalize_query(query)

        params = {
            "action": "opensearch",
            "search": normalized_query,
            "limit": 5,
            "namespace": 0,
            "format": "json"
        }

        response = requests.get(
            self.WIKI_OPENSEARCH_URL,
            params=params,
            headers=self.HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if len(data) < 2 or not data[1]:
            return None

        titles = data[1]

        for title in titles:

            # Prefer exact match if available
            if title.lower() == normalized_query.lower():
                chosen_title = title
                break
        else:
            chosen_title = titles[0]

        encoded_title = urllib.parse.quote(chosen_title)

        summary_response = requests.get(
            self.WIKI_SUMMARY_URL + encoded_title,
            headers=self.HEADERS,
            timeout=10
        )

        if summary_response.status_code != 200:
            return None

        summary_data = summary_response.json()
        extract = summary_data.get("extract")

        if not extract:
            return None

        lower_extract = extract.lower()

        if "may refer to" in lower_extract:
            return None

        return extract

    # ------------------------------------------------
    # SHORTEN FOR VOICE
    # ------------------------------------------------

    def _shorten(self, text):

        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        if len(sentences) > 2:
            text = " ".join(sentences[:2])
        else:
            text = sentences[0]

        text = text.strip()

        if not text.endswith("."):
            text += "."

        return text