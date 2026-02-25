import cv2
import threading
from ultralytics import YOLO

from execution.vision.tracking_engine import TrackingEngine
from execution.vision.scene_memory import SceneMemory
from execution.vision.event_engine import EventEngine


class CameraDetector:

    def __init__(self, tts=None):

        # YOLO stays on CPU (Whisper uses GPU)
        self.device = "cpu"
        self.model = YOLO("yolov8n.pt")
        self.model.to(self.device)

        self._running = False
        self._thread = None

        self.tts = tts

        # Thread-safe buffers
        self._latest_detections = []
        self._latest_tracked = []
        self._latest_events = []

        self._lock = threading.Lock()

        # Engines
        self.tracker = TrackingEngine()
        self.scene_memory = SceneMemory()
        self.event_engine = EventEngine(
            cooldown=3.5,
            motion_threshold=80
        )

    # =====================================================
    # START CAMERA
    # =====================================================

    def start(self):

        if self._running:
            print("Camera already running.")
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )
        self._thread.start()

    # =====================================================
    # STOP CAMERA
    # =====================================================

    def stop(self):

        if not self._running:
            return

        print("🛑 Stopping camera...")
        self._running = False

        if self._thread:
            self._thread.join(timeout=2)

    # =====================================================
    # PUBLIC GETTERS
    # =====================================================

    def get_latest_detections(self):
        with self._lock:
            return list(self._latest_detections)

    def get_tracked_objects(self):
        with self._lock:
            return list(self._latest_tracked)

    def get_scene_events(self):
        with self._lock:
            return list(self._latest_events)

    # =====================================================
    # MAIN LOOP
    # =====================================================

    def _run_loop(self):

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        '''cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)'''
        if not cap.isOpened():
            print("Unable to access camera.")
            self._running = False
            return

        print("📷 Camera started.")

        frame_skip = 0

        while self._running:

            ret, frame = cap.read()
            if not ret:
                break

            frame_skip += 1

            # Performance frame skip
            if frame_skip % 3 != 0:
                cv2.imshow("Assistant Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                continue

            results = self.model(frame, verbose=False)

            detections = []

            for r in results:
                for box in r.boxes:

                    confidence = float(box.conf[0])
                    if confidence < 0.65:
                        continue

                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    detections.append({
                        "label": class_name,
                        "confidence": confidence,
                        "bbox": (x1, y1, x2, y2)
                    })

                    label = f"{class_name} {confidence:.2f}"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

            # Tracking
            tracked_objects = self.tracker.update(detections)

            # Scene Memory
            events = self.scene_memory.update(tracked_objects)

            # Smart Dynamic Event Processing
            frame_width = frame.shape[1]

            message = self.event_engine.process_events(
                events,
                frame_width=frame_width
            )

            # 🔥 CRITICAL FIX: prevent vision backlog
            if message:
                print(f"[VISION EVENT] {message}")
                # 🔥 Production: No auto TTS for passive events

            # Thread-safe state update
            with self._lock:
                self._latest_detections = detections
                self._latest_tracked = tracked_objects
                self._latest_events = events

            cv2.imshow("Assistant Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        self._running = False
        print("📷 Camera stopped.")