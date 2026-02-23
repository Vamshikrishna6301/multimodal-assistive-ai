import subprocess
from core.response_model import UnifiedResponse


class WindowsSystemAdapter:
    """
    Windows System Control Adapter
    Handles:
    - Close application
    - Shutdown
    - Restart
    """

    # =====================================================
    # CLOSE APPLICATION
    # =====================================================

    def close_application(self, target: str) -> UnifiedResponse:
        try:
            if not target:
                return UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="No application specified to close.",
                    error_code="NO_TARGET"
                )

            target = target.lower().strip()

            # Strategy 1: Try exact exe name
            result = subprocess.call(
                f'taskkill /IM "{target}.exe" /F',
                shell=True
            )

            if result == 0:
                return UnifiedResponse.success_response(
                    category="execution",
                    spoken_message=f"{target} closed."
                )

            # Strategy 2: Kill by window title (works for UWP apps like Calculator)
            result = subprocess.call(
                f'taskkill /F /FI "WINDOWTITLE eq {target}*"',
                shell=True
            )

            if result == 0:
                return UnifiedResponse.success_response(
                    category="execution",
                    spoken_message=f"{target} closed."
                )

            return UnifiedResponse.error_response(
                category="execution",
                spoken_message=f"Could not close {target}. It may not be running.",
                error_code="PROCESS_NOT_FOUND"
            )

        except Exception as e:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message=f"Failed to close {target}.",
                error_code="CLOSE_FAILED",
                technical_message=str(e)
            )

    # =====================================================
    # MAIN HANDLER
    # =====================================================

    def handle(self, decision: dict) -> UnifiedResponse:

        action = decision.get("action")
        target = decision.get("target", "")
        text = decision.get("text", "").lower()

        # Close Application
        if action == "SYSTEM_CONTROL" and target:
            return self.close_application(target)

        # Shutdown
        if "shutdown" in text:
            subprocess.call("shutdown /s /t 5", shell=True)
            return UnifiedResponse.success_response(
                category="execution",
                spoken_message="System shutting down."
            )

        # Restart
        if "restart" in text:
            subprocess.call("shutdown /r /t 5", shell=True)
            return UnifiedResponse.success_response(
                category="execution",
                spoken_message="System restarting."
            )

        return UnifiedResponse.error_response(
            category="execution",
            spoken_message="Unsupported system control command.",
            error_code="SYSTEM_UNSUPPORTED"
        )