import sys
import time
import sounddevice as sd
import numpy as np

from core.fusion_engine import FusionEngine
from voice.stt import STT
from voice.tts import TTS


SAMPLE_RATE = 16000
RECORD_SECONDS = 1.6


class VoicePhase2Assistant:

    def __init__(self):
        self.engine = FusionEngine()
        self.stt = STT()
        self.tts = TTS()
        self.running = True

    # =====================================================

    def start(self):
        print("\n🎤 Voice Assistant Phase 2 Started")
        print("Say 'exit' to stop.\n")

        while self.running:

            try:
                print("Listening...")

                audio = sd.rec(
                    int(SAMPLE_RATE * RECORD_SECONDS),
                    samplerate=SAMPLE_RATE,
                    channels=1,
                    dtype="int16"
                )

                sd.wait()

                audio_bytes = audio.flatten().tobytes()

                text = self.stt.transcribe(audio_bytes, SAMPLE_RATE)

                if not text:
                    continue

                print(f"You said: {text}")

                if "exit" in text:
                    self._shutdown()
                    break

                decision = self.engine.process_text(text)
                self._handle_decision(decision)

            except KeyboardInterrupt:
                self._shutdown()
                sys.exit(0)

            except Exception as e:
                print("Runtime Error:", e)
                time.sleep(0.3)

    # =====================================================

    def _handle_decision(self, decision):

        data = decision.to_dict()

        print("\n--- Decision ---")
        print(data)
        print("----------------\n")

        response = data.get("message")

        if response:
            self.tts.speak(response, blocking=True)

    # =====================================================

    def _shutdown(self):
        print("👋 Shutting down assistant.")
        self.tts.speak("Goodbye.", blocking=True)
        self.running = False


if __name__ == "__main__":
    assistant = VoicePhase2Assistant()
    assistant.start()