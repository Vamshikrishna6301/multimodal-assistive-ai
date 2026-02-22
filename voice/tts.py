import pyttsx3
import threading


class TTS:
    """
    Stable low-latency offline TTS.
    Reinitializes engine per call to avoid silent failures.
    """

    def __init__(self):
        self._lock = threading.Lock()

    # =====================================================

    def speak(self, text: str, blocking: bool = True):

        if not text:
            return

        if blocking:
            self._speak(text)
        else:
            threading.Thread(
                target=self._speak,
                args=(text,),
                daemon=True
            ).start()

    # =====================================================

    def _speak(self, text: str):

        with self._lock:
            engine = pyttsx3.init()
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

    # =====================================================

    def stop(self):
        pass