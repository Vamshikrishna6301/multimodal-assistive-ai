import subprocess
import threading
import queue


class TTS:

    def __init__(self, runtime=None):
        self._runtime = runtime
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._current_process = None
        self._lock = threading.Lock()

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    # =====================================================

    def speak(self, text: str):

        if not text:
            return

        self._queue.put(text)

    # =====================================================

    def is_speaking(self):

        with self._lock:
            return (
                self._current_process is not None
                and self._current_process.poll() is None
            )

    # =====================================================

    def _run_loop(self):

        while not self._stop_event.is_set():

            try:
                text = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if self._runtime:
                self._runtime.start_speaking()

            try:
                safe_text = text.replace('"', '')

                command = (
                    'Add-Type -AssemblyName System.Speech; '
                    '$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                    f'$speak.Speak("{safe_text}")'
                )

                with self._lock:
                    self._current_process = subprocess.Popen(
                        ["powershell", "-Command", command],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )

                self._current_process.wait()

            except Exception as e:
                print("⚠️ TTS Error:", e)

            finally:
                with self._lock:
                    self._current_process = None

                if self._runtime:
                    self._runtime.stop_speaking()

    # =====================================================

    def stop(self):

        with self._lock:
            if self._current_process and self._current_process.poll() is None:
                try:
                    self._current_process.terminate()
                except Exception:
                    pass
                self._current_process = None

        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

        if self._runtime:
            self._runtime.stop_speaking()

    # =====================================================

    def shutdown(self):

        self.stop()
        self._stop_event.set()
        self._thread.join(timeout=2)