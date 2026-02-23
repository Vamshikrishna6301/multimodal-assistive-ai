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

    def close_application(self, target: str) -> UnifiedResponse:

        try:
            # Try killing process by name
            subprocess.call(f"taskkill /IM {target}.exe /F", shell=True)

            return UnifiedResponse.success_response(
                category="execution",
                spoken_message=f"{target} closed."
            )

        except Exception:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message=f"Failed to close {target}.",
                error_code="CLOSE_FAILED"
            )

    # ----------------------------------------

    def handle(self, decision: dict) -> UnifiedResponse:

        text = decision.get("text", "").lower()

        if "shutdown" in text:
            subprocess.call("shutdown /s /t 5", shell=True)
            return UnifiedResponse.success_response(
                category="execution",
                spoken_message="System shutting down."
            )

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