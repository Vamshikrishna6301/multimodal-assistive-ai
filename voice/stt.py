from faster_whisper import WhisperModel
import numpy as np
import threading


class STT:
    """
    Production Whisper STT (GPU-safe + Thread-safe)
    """

    def __init__(self):

        self._lock = threading.Lock()

        try:
            print("🔄 Loading Whisper on GPU...")
            self.model = WhisperModel(
                "small.en",
                device="cuda",
                compute_type="float16"
            )
            print("✅ GPU mode enabled")
        except Exception as e:
            print("⚠️ GPU unavailable, falling back to CPU:", e)
            self.model = WhisperModel(
                "small.en",
                device="cpu",
                compute_type="int8"
            )

    # =====================================================
    # TRANSCRIBE (Safe)
    # =====================================================

    def transcribe(self, audio_bytes: bytes, input_sample_rate: int) -> str:

        if not audio_bytes:
            return ""

        audio = np.frombuffer(audio_bytes, dtype=np.int16)

        if audio.size == 0:
            return ""

        audio = audio.astype(np.float32) / 32768.0

        # Ignore very short clips (< 300ms)
        if len(audio) < input_sample_rate * 0.3:
            return ""

        try:
            with self._lock:

                segments_generator, info = self.model.transcribe(
                    audio,
                    language="en",
                    beam_size=1,
                    best_of=1,
                    temperature=0.0,
                    vad_filter=False
                )

                # 🔥 CRITICAL FIX:
                # Fully exhaust generator to avoid GPU deadlock
                segments = list(segments_generator)

        except Exception as e:
            print("⚠️ STT inference error:", e)
            return ""

        text = " ".join(seg.text for seg in segments).strip().lower()
        text = text.replace(".", "").replace(",", "")

        return text