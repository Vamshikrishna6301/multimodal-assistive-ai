import numpy as np
from faster_whisper import WhisperModel

class STT:
    def __init__(self):
        self.model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

    def transcribe(self, audio_bytes: bytes) -> str:
        # Convert bytes → int16 numpy
        audio = np.frombuffer(audio_bytes, dtype=np.int16)

        # Convert to float32 [-1, 1]
        audio = audio.astype(np.float32) / 32768.0

        # IMPORTANT: must be 1-D array
        if audio.ndim != 1:
            audio = audio.flatten()

        # Call transcribe WITHOUT sampling_rate
        segments, _ = self.model.transcribe(
            audio,
            beam_size=1,
            language="en"
        )

        return " ".join(seg.text for seg in segments).strip().lower()
