import subprocess
from core.response_model import UnifiedResponse


class WindowsSystemAdapter:
    """
    Production-Level Windows System Control Adapter

    - Supports shutdown, restart, logoff
    - Enforces controlled command mapping
    - Adds safety delay
    """

    SUPPORTED_ACTIONS = {
        "shutdown": "shutdown /s /t 10",
        "restart": "shutdown /r /t 10",
        "logoff": "shutdown /l"
    }

    def handle(self, decision: dict) -> UnifiedResponse:

        target = decision.get("target")

        if not target:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="No system action specified.",
                error_code="NO_SYSTEM_ACTION"
            )

        action = target.lower().strip()

        if action not in self.SUPPORTED_ACTIONS:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="Unsupported system control command.",
                error_code="UNSUPPORTED_SYSTEM_ACTION"
            )

        try:
            command = self.SUPPORTED_ACTIONS[action]

            subprocess.Popen(command, shell=True)

            if action in ["shutdown", "restart"]:
                spoken = f"The system will {action} in 10 seconds."
            else:
                spoken = "Logging off now."

            return UnifiedResponse.success_response(
                category="execution",
                spoken_message=spoken
            )

        except Exception as e:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="System command failed.",
                error_code="SYSTEM_CONTROL_FAILED",
                technical_message=str(e)
            )