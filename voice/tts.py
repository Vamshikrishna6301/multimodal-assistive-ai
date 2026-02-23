import subprocess
import threading
import queue


class TTS:

    def __init__(self, runtime=None):
        self._runtime = runtime
        self._queue = queue.Queue()
        self._stop_event = threading.Event()

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def speak(self, text: str):

        if not text:
            return

        self._queue.put(text)

    def _run_loop(self):

        while not self._stop_event.is_set():

            try:
                text = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if self._runtime:
                self._runtime.set_speaking(True)

            try:
                # Escape quotes properly
                safe_text = text.replace('"', '')
                command = (
                    'Add-Type –AssemblyName System.Speech; '
                    f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{safe_text}")'
                )

                subprocess.run(
                    ["powershell", "-Command", command],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            except Exception as e:
                print("⚠️ TTS Error:", e)

            if self._runtime:
                self._runtime.set_speaking(False)

    def stop(self):
        if self._runtime:
            self._runtime.set_speaking(False)

    def shutdown(self):
        self._stop_event.set()
        self._thread.join(timeout=2)