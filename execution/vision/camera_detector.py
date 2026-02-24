import cv2
import time
import threading
from collections import Counter

from ultralytics import YOLO


class CameraDetector:

    def __init__(self, tts=None):

        # 🔥 Force YOLO to CPU (Whisper keeps GPU)
        self.device = "cpu"
        self.model = YOLO("yolov8n.pt")
        self.model.to(self.device)

        self._running = False
        self._thread = None

        self._last_spoken = None
        self._last_summary_time = 0

        self.tts = tts

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
    # MAIN LOOP
    # =====================================================

    def _run_loop(self):

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

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

            # 🔥 Frame skipping (balance performance)
            if frame_skip % 3 != 0:
                cv2.imshow("Assistant Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                continue

            results = self.model(frame, verbose=False)

            detected = []

            for r in results:
                for box in r.boxes:

                    confidence = float(box.conf[0])

                    # 🔥 Balanced confidence threshold
                    if confidence < 0.5:
                        continue

                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]

                    detected.append(class_name)

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = f"{class_name} {confidence:.2f}"

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

            # -------------------------------------------------
            # STABLE SPEECH SUMMARY (Every 2 seconds)
            # -------------------------------------------------

            if detected and time.time() - self._last_summary_time > 2:

                counts = Counter(detected)

                summary = ", ".join(
                    f"{v} {k}{'s' if v > 1 else ''}"
                    for k, v in counts.items()
                )

                message = f"I see {summary}."

                # Speak only if changed
                if message != self._last_spoken:

                    print(f"Detected: {summary}")

                    if self.tts:
                        self.tts.speak(message)

                    self._last_spoken = message

                self._last_summary_time = time.time()

            cv2.imshow("Assistant Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        self._running = False
        print("📷 Camera stopped.")