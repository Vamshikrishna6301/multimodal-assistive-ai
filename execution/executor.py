from core.response_model import UnifiedResponse
from execution.dispatcher import Dispatcher
from execution.execution_logger import ExecutionLogger


class ExecutionEngine:

    def __init__(self, context_memory):
        self.dispatcher = Dispatcher()
        self.logger = ExecutionLogger()
        self.context_memory = context_memory

    def execute(self, decision: dict) -> UnifiedResponse:

        try:
            if decision.get("status") != "APPROVED":
                response = UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Execution blocked. Decision not approved.",
                    error_code="NOT_APPROVED"
                )
                self.logger.log(decision, response)
                return response

            response = self.dispatcher.dispatch(decision)

            if response.success:
                self._update_context(decision)

            self.logger.log(decision, response)
            return response

        except Exception as e:
            response = UnifiedResponse.error_response(
                category="execution",
                spoken_message="An internal execution error occurred.",
                error_code="EXECUTION_FAILURE",
                technical_message=str(e)
            )
            self.logger.log(decision, response)
            return response

    def _update_context(self, decision: dict):

        action = decision.get("action")
        target = decision.get("target")

        if action == "OPEN_APP" and target:
            self.context_memory.last_app = target

        if action == "SYSTEM_CONTROL" and target:
            if self.context_memory.last_app == target:
                self.context_memory.last_app = None

        if action == "FILE_OPERATION" and target:
            self.context_memory.last_file = target