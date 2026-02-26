from core.response_model import UnifiedResponse
from execution.dispatcher import Dispatcher
from execution.execution_logger import ExecutionLogger
from execution.uia_service.uia_client import UIAClient


class ExecutionEngine:
    """
    Production Execution Engine
    - External UIA Service (Socket)
    - Named Click
    - Indexed Click
    - Safe fallback handling
    - Robust dispatcher handling
    """

    def __init__(self, context_memory):
        self.dispatcher = Dispatcher()
        self.logger = ExecutionLogger()
        self.context_memory = context_memory
        self.uia_client = UIAClient()

    # =====================================================
    # MAIN EXECUTION ENTRY
    # =====================================================

    def execute(self, decision: dict) -> UnifiedResponse:

        try:
            # -----------------------------
            # Basic validation
            # -----------------------------
            if not isinstance(decision, dict):
                return self._error("Invalid execution request.", "INVALID_DECISION")

            if decision.get("status") != "APPROVED":
                return self._error("Execution blocked.", "NOT_APPROVED")

            if decision.get("blocked_reason"):
                return self._error("Blocked by safety system.", "BLOCKED_BY_SAFETY")

            action = decision.get("action")
            if not action:
                return self._error("No executable action found.", "MISSING_ACTION")

            # -----------------------------
            # Risk validation
            # -----------------------------
            risk_level = decision.get("risk_level", 0)
            requires_confirmation = decision.get("requires_confirmation", False)
            confirmed = decision.get("confirmed", False)

            if (requires_confirmation or risk_level >= 7) and not confirmed:
                return self._error(
                    "Execution requires confirmation.",
                    "CONFIRMATION_REQUIRED"
                )

            # =====================================================
            # 🔥 UIA ACTIONS (Handled FIRST)
            # =====================================================

            if action == "READ_SCREEN":
                return self._handle_read_screen()

            if action == "CLICK_INDEX":
                index = decision.get("parameters", {}).get("index")
                return self._handle_click_index(index)

            if action == "CLICK_NAME":
                name = decision.get("parameters", {}).get("name")
                return self._handle_click_name(name)

            # =====================================================
            # NON-UIA ACTIONS
            # =====================================================

            response = self.dispatcher.dispatch(decision)

            if not response:
                return self._error("Unsupported action type.", "UNSUPPORTED_ACTION")

            if getattr(response, "success", False):
                self._update_context(decision)

            self.logger.log(decision, response)

            return response

        except Exception as e:
            print("🔥 EXECUTION EXCEPTION:", repr(e))
            return self._error(
                "An internal execution error occurred.",
                "EXECUTION_FAILURE",
                technical=str(e)
            )

    # =====================================================
    # UIA HANDLERS
    # =====================================================

    def _handle_read_screen(self) -> UnifiedResponse:

        result = self.uia_client.read_screen()

        if not isinstance(result, dict):
            return self._error("UIA service unavailable.", "UIA_ERROR")

        if result.get("status") != "success":
            return self._error(
                result.get("message", "UIA service error."),
                "UIA_ERROR"
            )

        window = result.get("window", "unknown window")
        elements = result.get("elements", [])

        if not elements:
            return UnifiedResponse.success_response(
                category="execution",
                spoken_message=f"You are in {window}. No interactive elements found."
            )

        lines = []
        for el in elements[:10]:
            lines.append(f"{el['index']}. {el['type']} {el['name']}")

        speech = (
            f"You are in {window}. "
            + ", ".join(lines)
            + ". Say click number or click by name."
        )

        return UnifiedResponse.success_response(
            category="execution",
            spoken_message=speech
        )

    # -----------------------------------------------------

    def _handle_click_index(self, index) -> UnifiedResponse:

        if not isinstance(index, int):
            return self._error("Invalid selection number.", "INVALID_INDEX")

        result = self.uia_client.click_index(index)

        if not isinstance(result, dict):
            return self._error("UIA service unavailable.", "UIA_ERROR")

        if result.get("status") != "success":
            return self._error(
                result.get("message", "Click failed."),
                "CLICK_FAILED"
            )

        return UnifiedResponse.success_response(
            category="execution",
            spoken_message=result.get("message")
        )

    # -----------------------------------------------------

    def _handle_click_name(self, name) -> UnifiedResponse:

        if not name or not isinstance(name, str):
            return self._error("Invalid element name.", "INVALID_NAME")

        name = name.strip()

        result = self.uia_client.click_by_name(name)

        if not isinstance(result, dict):
            return self._error("UIA service unavailable.", "UIA_ERROR")

        if result.get("status") != "success":
            return self._error(
                result.get("message", "Click failed."),
                "CLICK_FAILED"
            )

        return UnifiedResponse.success_response(
            category="execution",
            spoken_message=result.get("message")
        )

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
    # ERROR HELPER
    # =====================================================

    def _error(self, message, code, technical=None):
        return UnifiedResponse.error_response(
            category="execution",
            spoken_message=message,
            error_code=code,
            technical_message=technical
        )

    # =====================================================

    @property
    def camera_detector(self):
        return self.dispatcher.vision_executor.camera_detector