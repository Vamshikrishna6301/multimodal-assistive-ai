from core.response_model import UnifiedResponse
from execution.vision.screen_capture import ScreenCapture
from execution.vision.ocr_engine import OCREngine
from execution.vision.camera_detector import CameraDetector


class VisionExecutor:

    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.ocr_engine = OCREngine()
        self.camera_detector = CameraDetector()
        self._tts = None  # Will be injected from VoiceLoop

    # =====================================================
    # TTS INJECTION (Clean Architecture)
    # =====================================================

    def set_tts(self, tts):
        self._tts = tts
        self.camera_detector.tts = tts

    # =====================================================

    def handle(self, decision: dict) -> UnifiedResponse:

        try:
            action = decision.get("action")
            target = decision.get("target", "unknown")
            parameters = decision.get("parameters", {})
            task = parameters.get("task", "describe")

            # =====================================================
            # STOP CAMERA
            # =====================================================
            if action == "STOP_CAMERA":

                self.camera_detector.stop()

                return UnifiedResponse.success_response(
                    category="execution",
                    spoken_message="Camera stopped."
                )

            # =====================================================
            # CAMERA LIVE MODE
            # =====================================================
            if target == "camera":

                if task == "detect_objects":

                    self.camera_detector.start()

                    return UnifiedResponse.success_response(
                        category="execution",
                        spoken_message="Camera started."
                    )

                return UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Invalid camera task.",
                    error_code="INVALID_CAMERA_TASK"
                )

            # =====================================================
            # SCREEN LOGIC
            # =====================================================
            if target != "screen":
                return UnifiedResponse.error_response(
                    category="execution",
                    spoken_message="Invalid vision target.",
                    error_code="VISION_INVALID_TARGET"
                )

            frame = self.screen_capture.capture()

            if frame is None:
                raise RuntimeError("Failed to capture screen.")

            # =====================================================
            # OCR TASK
            # =====================================================
            if task == "read_text":

                text = self.ocr_engine.extract_text(frame)

                if not text:
                    return UnifiedResponse.success_response(
                        category="execution",
                        spoken_message="No readable text detected on the screen."
                    )

                return UnifiedResponse.success_response(
                    category="execution",
                    spoken_message=f"I detected the following text: {text}"
                )

            # =====================================================
            # DEFAULT SCREEN RESPONSE
            # =====================================================
            return UnifiedResponse.success_response(
                category="execution",
                spoken_message="Screen captured successfully."
            )

        except Exception as e:
            return UnifiedResponse.error_response(
                category="execution",
                spoken_message="Vision processing failed.",
                error_code="VISION_ERROR",
                technical_message=str(e)
            )