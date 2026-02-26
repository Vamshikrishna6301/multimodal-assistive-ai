from faster_whisper import WhisperModel
import numpy as np
import threading


class STT:
    """
    Production Whisper STT (GPU-EXCLUSIVE MODE)
    Optimized for NVIDIA CUDA with no CPU fallback
    """

    def __init__(self):

        self._lock = threading.Lock()
        self.model = None
        self.device_mode = "GPU"

        print("🔄 Loading Whisper on GPU (CUDA)...")
        try:
            self.model = WhisperModel(
                "small.en",
                device="cuda",
                compute_type="float16"
            )
            print("✅ GPU mode enabled - Whisper loaded on NVIDIA CUDA")
        except Exception as e:
            print(f"❌ CRITICAL: Failed to load Whisper on GPU: {e}")
            print("   Ensure CUDA drivers are installed and PATH includes PyTorch CUDA libs")
            raise

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
            print(f"❌ STT GPU inference error: {e}")
            return ""

        text = " ".join(seg.text for seg in segments).strip().lower()
        text = text.replace(".", "").replace(",", "")

        return text