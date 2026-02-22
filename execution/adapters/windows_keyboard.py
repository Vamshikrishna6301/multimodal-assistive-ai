import time
import pyautogui
from core.response_model import UnifiedResponse


class WindowsKeyboardAdapter:
    """
    Production-Level Keyboard Adapter

    - Adds focus delay
    - Enables fail-safe
    - Handles typing safely
    """

    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.02  # slight delay between actions

    def type_text(self, text: str) -> UnifiedResponse:

        if not text:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="No text was provided to type.",
                error_code="NO_TEXT"
            )

        try:
            # Give user time to focus correct window
            time.sleep(1)

            pyautogui.write(text)

            return UnifiedResponse.success_response(
                category="execution",
                spoken_message="Text typed successfully."
            )

        except pyautogui.FailSafeException:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="Typing stopped due to fail-safe trigger.",
                error_code="FAIL_SAFE_TRIGGERED"
            )

        except Exception as e:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="Typing failed.",
                error_code="TYPE_ERROR",
                technical_message=str(e)
            )