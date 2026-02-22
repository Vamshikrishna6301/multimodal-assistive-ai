import requests
import urllib.parse
import re
from core.response_model import UnifiedResponse


class KnowledgeEngine:
    """
    Final Optimized Free Knowledge Engine
    - Wikipedia based
    - Context aware
    - Garbage resistant
    - AI-term boosted
    - Disambiguation filtered
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
                spoken_message=f"{self._shorten(summary)} Would you like more details?"
            )

        except Exception as e:
            print("DEBUG ERROR:", str(e))
            return UnifiedResponse.error_response(
                category="knowledge",
                spoken_message="I am unable to answer that right now.",
                error_code="KNOWLEDGE_ERROR",
                technical_message=str(e)
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
    # CONTEXT BOOSTING
    # ------------------------------------------------

    def _boost_context(self, query):

        ai_keywords = [
            "ai",
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "neural network",
        ]

        if any(keyword in query for keyword in ai_keywords):
            query += " artificial intelligence machine learning neural network"

        return query

    # ------------------------------------------------
    # GET BEST SUMMARY
    # ------------------------------------------------

    def _get_best_summary(self, query):

        normalized_query = self._normalize_query(query)
        boosted_query = self._boost_context(normalized_query)

        params = {
            "action": "opensearch",
            "search": boosted_query,
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

        # Try up to 5 candidates
        for title in titles:

            encoded_title = urllib.parse.quote(title)

            summary_response = requests.get(
                self.WIKI_SUMMARY_URL + encoded_title,
                headers=self.HEADERS,
                timeout=10
            )

            if summary_response.status_code != 200:
                continue

            summary_data = summary_response.json()
            extract = summary_data.get("extract")

            if not extract:
                continue

            lower_extract = extract.lower()

            # Avoid disambiguation pages
            if "may refer to" in lower_extract:
                continue

            # Avoid film bias when AI context exists
            if "ai" in normalized_query and (
                "film" in lower_extract or
                "movie" in lower_extract
            ):
                continue

            # Prefer proper definition sentences
            if " is " in extract or " was " in extract:
                return extract

        return None

    # ------------------------------------------------
    # SHORTEN FOR VOICE
    # ------------------------------------------------

    def _shorten(self, text):

        sentences = re.split(r'(?<=\.)\s+', text)

        if len(sentences) > 2:
            trimmed = " ".join(sentences[:2])
        else:
            trimmed = text

        if not trimmed.endswith("."):
            trimmed += "."

        return trimmed