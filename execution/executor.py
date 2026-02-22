from core.response_model import UnifiedResponse
from execution.dispatcher import Dispatcher


class ExecutionEngine:
    """
    Production-Ready Execution Engine
    - Validates decision
    - Delegates to Dispatcher
    - Wraps execution errors safely
    """

    def __init__(self):
        self.dispatcher = Dispatcher()

    def execute(self, decision: dict) -> UnifiedResponse:

        try:
            status = decision.get("status")

            if status != "APPROVED":
                return UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Execution blocked. Decision not approved.",
                    error_code="NOT_APPROVED"
                )

            return self.dispatcher.dispatch(decision)

        except Exception as e:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="An internal execution error occurred.",
                error_code="EXECUTION_FAILURE",
                technical_message=str(e)
            )