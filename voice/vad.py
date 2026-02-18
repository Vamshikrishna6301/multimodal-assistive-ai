import webrtcvad
from config import SAMPLE_RATE, FRAME_DURATION_MS, VAD_AGGRESSIVENESS

class VAD:
    def __init__(self):
        self.vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
        self.frame_bytes = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000) * 2

    def is_speech(self, frame: bytes) -> bool:
        return self.vad.is_speech(frame, SAMPLE_RATE)
