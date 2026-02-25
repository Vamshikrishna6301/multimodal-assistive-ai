from core.response_model import UnifiedResponse
from execution.dispatcher import Dispatcher
from execution.execution_logger import ExecutionLogger


class ExecutionEngine:
    """
    Production Hardened Execution Layer

    Guarantees:
    - No execution without APPROVED status
    - No execution if blocked by safety
    - Dangerous execution allowed ONLY if confirmed=True
    - Safe against malformed decision input
    """

    def __init__(self, context_memory):
        self.dispatcher = Dispatcher()
        self.logger = ExecutionLogger()
        self.context_memory = context_memory

    # =====================================================
    # MAIN EXECUTION ENTRY
    # =====================================================

    def execute(self, decision: dict) -> UnifiedResponse:

        try:
            # 1️⃣ Handle malformed input safely
            if not isinstance(decision, dict):
                response = UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Invalid execution request.",
                    error_code="INVALID_DECISION"
                )
                self.logger.log({}, response)
                return response

            # 2️⃣ Must be APPROVED
            if decision.get("status") != "APPROVED":
                response = UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Execution blocked. Decision not approved.",
                    error_code="NOT_APPROVED"
                )
                self.logger.log(decision, response)
                return response

            # 3️⃣ Block if safety flagged
            if decision.get("blocked_reason"):
                response = UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Execution blocked by safety system.",
                    error_code="BLOCKED_BY_SAFETY"
                )
                self.logger.log(decision, response)
                return response

            # 4️⃣ Validate action
            action = decision.get("action")
            if not action:
                response = UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="No executable action found.",
                    error_code="MISSING_ACTION"
                )
                self.logger.log(decision, response)
                return response

            # 5️⃣ Risk & Confirmation Revalidation
            risk_level = decision.get("risk_level", 0)
            requires_confirmation = decision.get("requires_confirmation", False)
            confirmed = decision.get("confirmed", False)

            if (requires_confirmation or risk_level >= 7) and not confirmed:
                response = UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Execution requires confirmation.",
                    error_code="CONFIRMATION_REQUIRED"
                )
                self.logger.log(decision, response)
                return response

            # 6️⃣ SAFE TO EXECUTE
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

            self.logger.log(decision if isinstance(decision, dict) else {}, response)
            return response

    # =====================================================
    # CONTEXT UPDATE
    # =====================================================

    def _update_context(self, decision: dict):

        action = decision.get("action")
        target = decision.get("target")

        if action == "OPEN_APP" and target:
            self.context_memory.last_app = target

        elif action == "SYSTEM_CONTROL" and target:
            if self.context_memory.last_app == target:
                self.context_memory.last_app = None

        elif action == "FILE_OPERATION" and target:
            self.context_memory.last_file = target

    # =====================================================
    # SAFE CAMERA ACCESS FOR ROUTER
    # =====================================================

    @property
    def camera_detector(self):
        """
        Exposes CameraDetector safely to DecisionRouter
        without leaking internal architecture.
        """
        return self.dispatcher.vision_executor.camera_detector