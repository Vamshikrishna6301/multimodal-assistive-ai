import subprocess
import shutil
from core.response_model import UnifiedResponse


class WindowsAppAdapter:
    """
    Strict Production-Level Windows App Launcher

    - Only launches apps that exist in PATH
    - Allows known safe system apps
    - Does NOT blindly call 'start'
    """

    COMMON_APPS = {
        "notepad": "notepad.exe",
        "calc": "calc.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "explorer": "explorer.exe"
    }

    def open_app(self, app_name: str) -> UnifiedResponse:

        if not app_name:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="No application name was provided.",
                error_code="NO_APP_NAME"
            )

        app_name = app_name.lower().strip()

        # Resolve known aliases
        resolved = self.COMMON_APPS.get(app_name, app_name)

        # Try resolving in PATH
        executable = shutil.which(resolved)

        if not executable:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message=f"I could not find an application named {app_name}.",
                error_code="APP_NOT_FOUND"
            )

        try:
            subprocess.Popen(executable)

            return UnifiedResponse.success_response(
                category="execution",
                spoken_message=f"Opening {app_name}."
            )

        except Exception as e:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="Failed to open the application.",
                error_code="APP_OPEN_FAILED",
                technical_message=str(e)
            )