import pyttsx3
import threading


class TTS:

    def __init__(self, runtime=None):
        self._lock = threading.Lock()
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", 180)
        self._engine.setProperty("volume", 1.0)
        self._runtime = runtime
        self._speaking = False

    def speak(self, text: str):

        if not text:
            return

        threading.Thread(
            target=self._speak,
            args=(text,),
            daemon=True
        ).start()

    def _speak(self, text: str):

        with self._lock:
            self._speaking = True

            if self._runtime:
                self._runtime.set_speaking(True)

            self._engine.say(text)
            self._engine.runAndWait()

            self._speaking = False

            if self._runtime:
                self._runtime.set_speaking(False)

    def stop(self):
        with self._lock:
            self._engine.stop()
            self._speaking = False

            if self._runtime:
                self._runtime.set_speaking(False)