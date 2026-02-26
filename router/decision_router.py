from core.response_model import UnifiedResponse
from execution.executor import ExecutionEngine
from utility.utility_engine import UtilityEngine
from knowledge.llm_engine import LLMEngine
from knowledge.knowledge_engine import KnowledgeEngine
from execution.vision.vision_query_engine import VisionQueryEngine


class DecisionRouter:

    EXECUTION_ACTIONS = {
        "OPEN_APP",
        "SEARCH",
        "TYPE_TEXT",
        "FILE_OPERATION",
        "SYSTEM_CONTROL",
        "VISION",
        "STOP_CAMERA"
    }

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

        # 🔥 Proper injection (clean architecture)
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

        if isinstance(action, str):
            action = action.upper()

        # --------------------------------------------------
        # VISION QUERY (Highest priority)
        # --------------------------------------------------

        if action == "VISION_QUERY":
            return self.vision_query_engine.handle(decision)

        # --------------------------------------------------
        # EXECUTION
        # --------------------------------------------------

        if action in self.EXECUTION_ACTIONS:
            return self.execution_engine.execute(decision)

        # --------------------------------------------------
        # UTILITY
        # --------------------------------------------------

        if action in self.UTILITY_ACTIONS:
            return self.utility_engine.handle(decision)

        # --------------------------------------------------
        # KNOWLEDGE
        # --------------------------------------------------

        if action in self.KNOWLEDGE_ACTIONS:

            query = decision.get("target", "")

            if query.lower().startswith(("who is", "who was")):
                return self.wikipedia_engine.handle(decision)

            return self.llm_engine.handle(decision)

        # --------------------------------------------------

        return UnifiedResponse.error_response(
            category="router",
            spoken_message="Unsupported action type.",
            error_code="UNSUPPORTED_ACTION_TYPE"
        )