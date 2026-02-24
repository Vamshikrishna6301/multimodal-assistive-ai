from core.response_model import UnifiedResponse
from execution.adapters.windows_app import WindowsAppAdapter
from execution.adapters.windows_browser import WindowsBrowserAdapter
from execution.adapters.windows_keyboard import WindowsKeyboardAdapter
from execution.adapters.windows_file import WindowsFileAdapter
from execution.adapters.windows_system import WindowsSystemAdapter
from execution.vision.vision_executor import VisionExecutor  # ✅ Added


class Dispatcher:
    """
    Production Dispatcher Layer

    - Routes approved actions
    - Delegates to Windows adapters
    - Keeps logic modular and clean
    """

    def __init__(self):
        self.app_adapter = WindowsAppAdapter()
        self.browser_adapter = WindowsBrowserAdapter()
        self.keyboard_adapter = WindowsKeyboardAdapter()
        self.file_adapter = WindowsFileAdapter()
        self.system_adapter = WindowsSystemAdapter()

        # ✅ Vision Executor
        self.vision_executor = VisionExecutor()

    def dispatch(self, decision: dict) -> UnifiedResponse:

        action = decision.get("action")
        target = decision.get("target")

        # -----------------------------
        # OPEN_APP
        # -----------------------------
        if action == "OPEN_APP":

            if target and target.lower() in ["chrome", "browser", "edge"]:
                return self.browser_adapter.open_browser()

            return self.app_adapter.open_app(target)

        # -----------------------------
        # SEARCH
        # -----------------------------
        elif action == "SEARCH":
            return self.browser_adapter.search(target)

        # -----------------------------
        # TYPE_TEXT
        # -----------------------------
        elif action == "TYPE_TEXT":
            return self.keyboard_adapter.type_text(target)

        # -----------------------------
        # FILE_OPERATION
        # -----------------------------
        elif action == "FILE_OPERATION":
            return self.file_adapter.handle(decision)

        # -----------------------------
        # SYSTEM_CONTROL
        # -----------------------------
        elif action == "SYSTEM_CONTROL":
            return self.system_adapter.handle(decision)

        # -----------------------------
        # VISION  ✅ NEW
        # -----------------------------
        elif action == "VISION":
            return self.vision_executor.handle(decision)

        # -----------------------------
        # Unsupported Action
        # -----------------------------
        return UnifiedResponse.error_response(
            category="execution",
            spoken_message="Unsupported execution action.",
            error_code="UNSUPPORTED_ACTION"
        )