import os
from pathlib import Path
from core.response_model import UnifiedResponse


class WindowsFileAdapter:
    """
    Production-Level File Adapter

    - Restricts file operations to safe user folders
    - Prevents system directory access
    - Handles file validation
    """

    SAFE_DIRECTORIES = [
        Path.home() / "Desktop",
        Path.home() / "Documents",
        Path.home() / "Downloads"
    ]

    def handle(self, decision: dict) -> UnifiedResponse:

        target = decision.get("target")

        if not target:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="No file name was provided.",
                error_code="NO_FILE_NAME"
            )

        try:
            file_path = self._find_file_in_safe_dirs(target)

            if not file_path:
                return UnifiedResponse.error_response(
                    category="execution",
                    spoken_message=f"I could not find a file named {target} in safe folders.",
                    error_code="FILE_NOT_FOUND"
                )

            os.remove(file_path)

            return UnifiedResponse.success_response(
                category="execution",
                spoken_message=f"The file {target} has been deleted."
            )

        except PermissionError:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="Permission denied while trying to delete the file.",
                error_code="PERMISSION_DENIED"
            )

        except Exception as e:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="File operation failed.",
                error_code="FILE_OPERATION_FAILED",
                technical_message=str(e)
            )

    def _find_file_in_safe_dirs(self, filename: str):

        for directory in self.SAFE_DIRECTORIES:
            potential_path = directory / filename
            if potential_path.exists() and potential_path.is_file():
                return potential_path

        return None