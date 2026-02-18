import collections
from voice.mic_stream import MicrophoneStream
from voice.vad import VAD
from voice.stt import STT
from voice.tts import TTS
from voice.wakeword import is_wake_word
from config import MAX_SILENCE_FRAMES, WAKE_WORD

class VoiceLoop:
    def __init__(self):
        self.vad = VAD()
        self.stt = STT()
        self.tts = TTS()
        self.buffer = collections.deque()
        self.silence_frames = 0

    def run(self):
        print("🎙️ NeuroGen listening...")

        with MicrophoneStream() as mic:
            while True:
                frame = mic.read()

                if self.vad.is_speech(frame):
                    self.buffer.append(frame)
                    self.silence_frames = 0
                else:
                    self.silence_frames += 1

                if self.silence_frames > MAX_SILENCE_FRAMES and self.buffer:
                    audio = b"".join(self.buffer)
                    self.buffer.clear()

                    text = self.stt.transcribe(audio)

                    # 🔥 Ignore tiny garbage transcriptions
                    if not text or len(text) < 3:
                        continue

                    print(f"🗣️ Heard: {text}")

                    if is_wake_word(text, WAKE_WORD):
                        self.tts.speak("Yes. I am listening.")
