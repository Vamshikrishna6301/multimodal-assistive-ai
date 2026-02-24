from core.response_model import UnifiedResponse
from execution.executor import ExecutionEngine
from utility.utility_engine import UtilityEngine
from knowledge.llm_engine import LLMEngine
from knowledge.knowledge_engine import KnowledgeEngine


class DecisionRouter:
    """
    Final Production Decision Router (Hybrid Fast + Smart)

    - Execution → ExecutionEngine
    - Utility → UtilityEngine
    - Simple facts → Wikipedia (fast)
    - Reasoning → TinyLLM (smart)
    """

    EXECUTION_ACTIONS = {
        "OPEN_APP",
        "SEARCH",
        "TYPE_TEXT",
        "FILE_OPERATION",
        "SYSTEM_CONTROL",
        "VISION",  # ✅ Added Vision support
    }

    UTILITY_ACTIONS = {
        "CALCULATE",
        "GET_TIME",
    }

    KNOWLEDGE_ACTIONS = {
        "KNOWLEDGE_QUERY",
    }

    def __init__(self, context_memory):
        # 🔥 Shared ContextMemory injected here
        self.execution_engine = ExecutionEngine(context_memory)
        self.utility_engine = UtilityEngine()
        self.llm_engine = LLMEngine()
        self.wikipedia_engine = KnowledgeEngine()

    # ------------------------------------------------
    # MAIN ROUTE FUNCTION
    # ------------------------------------------------

    def route(self, decision: dict) -> UnifiedResponse:

        if not decision:
            return UnifiedResponse.error_response(
                category="router",
                spoken_message="No decision received.",
                error_code="NO_DECISION"
            )

        status = decision.get("status")
        action = decision.get("action")

        if status != "APPROVED":
            return UnifiedResponse.error_response(
                category="router",
                spoken_message="The action was not approved.",
                error_code="ACTION_NOT_APPROVED"
            )

        # ----------------------------
        # EXECUTION
        # ----------------------------
        if action in self.EXECUTION_ACTIONS:
            return self.execution_engine.execute(decision)

        # ----------------------------
        # UTILITY
        # ----------------------------
        if action in self.UTILITY_ACTIONS:
            return self.utility_engine.handle(decision)

        # ----------------------------
        # KNOWLEDGE (Hybrid)
        # ----------------------------
        if action in self.KNOWLEDGE_ACTIONS:

            query = decision.get("target", "")

            if self._is_simple_fact(query):
                return self.wikipedia_engine.handle(decision)

            return self.llm_engine.handle(decision)

        # ----------------------------
        # UNKNOWN ACTION
        # ----------------------------
        return UnifiedResponse.error_response(
            category="router",
            spoken_message="Unsupported action type.",
            error_code="UNSUPPORTED_ACTION_TYPE"
        )

    # ------------------------------------------------
    # SIMPLE FACT DETECTION
    # ------------------------------------------------

    def _is_simple_fact(self, query: str):

        if not query:
            return False

        query_lower = query.lower().strip()

        simple_prefixes = [
            "who is",
            "who was",
        ]

        if any(query_lower.startswith(prefix) for prefix in simple_prefixes):
            return True

        return False