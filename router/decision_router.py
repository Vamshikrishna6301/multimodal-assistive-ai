from core.response_model import UnifiedResponse
from execution.executor import ExecutionEngine
from utility.utility_engine import UtilityEngine
from knowledge.llm_engine import LLMEngine
from knowledge.knowledge_engine import KnowledgeEngine
from execution.vision.vision_query_engine import VisionQueryEngine


class DecisionRouter:
    """
    Central Routing Engine
    Routes approved decisions to:
    - Execution Engine
    - Utility Engine
    - Knowledge Engine
    - Vision Query Engine
    """

    UTILITY_ACTIONS = {
        "CALCULATE",
        "GET_TIME",
    }

    KNOWLEDGE_ACTIONS = {
        "KNOWLEDGE_QUERY",
    }

    def __init__(self, context_memory):

        self.execution_engine = ExecutionEngine(context_memory)
        self.utility_engine = UtilityEngine()
        self.llm_engine = LLMEngine()
        self.wikipedia_engine = KnowledgeEngine()

        self.vision_query_engine = VisionQueryEngine(
            self.execution_engine.camera_detector
        )

    # =====================================================
    # MAIN ROUTE FUNCTION
    # =====================================================

    def route(self, decision: dict) -> UnifiedResponse:

        if not decision:
            return UnifiedResponse.error_response(
                category="router",
                spoken_message="No decision received.",
                error_code="NO_DECISION"
            )

        if decision.get("status") != "APPROVED":
            return UnifiedResponse.error_response(
                category="router",
                spoken_message="The action was not approved.",
                error_code="ACTION_NOT_APPROVED"
            )

        action = decision.get("action")

        print("DEBUG ROUTER ACTION VALUE:", action, "| TYPE:", type(action))

        # --------------------------------------------------
        # VISION QUERY (separate from UIA screen reading)
        # --------------------------------------------------

        if action == "VISION_QUERY":
            return self.vision_query_engine.handle(decision)

        # --------------------------------------------------
        # UTILITY ACTIONS
        # --------------------------------------------------

        if action in self.UTILITY_ACTIONS:
            return self.utility_engine.handle(decision)

        # --------------------------------------------------
        # KNOWLEDGE ACTIONS
        # --------------------------------------------------

        if action in self.KNOWLEDGE_ACTIONS:

            query = decision.get("target", "")

            if isinstance(query, str) and query.lower().startswith(("who is", "who was")):
                return self.wikipedia_engine.handle(decision)

            return self.llm_engine.handle(decision)

        # --------------------------------------------------
        # EVERYTHING ELSE → EXECUTION ENGINE
        # --------------------------------------------------
        # 🔥 This removes the need to maintain EXECUTION_ACTIONS list
        # and prevents future "Unsupported action type" bugs.

        return self.execution_engine.execute(decision)