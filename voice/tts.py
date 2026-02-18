import threading
import pyttsx3

class TTS:
    def __init__(self):
        self.lock = threading.Lock()

    def speak(self, text: str):
        def run():
            with self.lock:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                engine.stop()

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        # pyttsx3 cannot reliably interrupt on Windows
        # We handle stop logically instead
        pass
