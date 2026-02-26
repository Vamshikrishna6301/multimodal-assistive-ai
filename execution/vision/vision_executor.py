from core.response_model import UnifiedResponse
from execution.vision.screen_capture import ScreenCapture
from execution.vision.ocr_engine import OCREngine
from execution.vision.camera_detector import CameraDetector
from execution.vision.scene_graph_engine import SceneGraphEngine
from execution.vision.stabilization_buffer import StabilizationBuffer
from execution.vision.screen_monitoring_engine import ScreenMonitoringEngine
from execution.vision.vision_mode_controller import VisionModeController


class VisionExecutor:

    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.ocr_engine = OCREngine()
        self.camera_detector = CameraDetector()
        self.scene_graph = SceneGraphEngine()
        self.stabilization = StabilizationBuffer()
        self.screen_monitor = ScreenMonitoringEngine()
        self.vision_mode = VisionModeController()
        self._tts = None  # Will be injected from VoiceLoop

    # =====================================================
    # TTS INJECTION (Clean Architecture)
    # =====================================================

    def set_tts(self, tts):
        self._tts = tts
        self.camera_detector.tts = tts

    # =====================================================
    # VISION MODE CONTROL
    # =====================================================

    def set_vision_mode(self, mode: str):
        """Set vision operating mode"""
        try:
            self.vision_mode.set_mode(mode)
            return UnifiedResponse.success_response(
                category="vision",
                spoken_message=f"Vision mode set to {mode}."
            )
        except Exception as e:
            return UnifiedResponse.error_response(
                category="vision",
                spoken_message=f"Failed to set vision mode: {e}",
                error_code="VISION_MODE_ERROR"
            )

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
            # SCREEN MONITORING
            # =====================================================
            if task == "monitor_screen":
                result = self.screen_monitor.monitor(tts=self._tts)
                msg = "Screen monitoring active"
                if result["keywords_detected"]:
                    msg += f": detected {', '.join(result['keywords_detected'])}"
                return UnifiedResponse.success_response(
                    category="execution",
                    spoken_message=msg
                )

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