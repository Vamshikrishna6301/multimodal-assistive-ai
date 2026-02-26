from faster_whisper import WhisperModel
import numpy as np
import threading


class STT:
    """
    Production Whisper STT (GPU-Optimized)
    Tuned for low latency + stable CUDA usage.
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
                compute_type="float16",
                cpu_threads=4,           # limit CPU thread contention
                num_workers=1            # prevent dataloader overhead
            )

            # 🔥 Warmup run (eliminates first-call latency spike)
            dummy_audio = np.zeros(16000, dtype=np.float32)
            list(self.model.transcribe(dummy_audio, beam_size=1))

            print("✅ GPU mode enabled - Whisper warmed up")

        except Exception as e:
            print(f"❌ CRITICAL: Failed to load Whisper on GPU: {e}")
            raise

    # =====================================================
    # TRANSCRIBE (Optimized)
    # =====================================================

    def transcribe(self, audio_bytes: bytes, input_sample_rate: int) -> str:

        if not audio_bytes:
            return ""

        audio = np.frombuffer(audio_bytes, dtype=np.int16)

        if audio.size == 0:
            return ""

        audio = audio.astype(np.float32) / 32768.0

        # 🔥 Ignore very short clips (< 400ms)
        if len(audio) < input_sample_rate * 0.4:
            return ""

        try:
            with self._lock:

                segments_generator, info = self.model.transcribe(
                    audio,
                    language="en",
                    beam_size=1,
                    best_of=1,
                    temperature=0.0,
                    vad_filter=False,
                    without_timestamps=True,
                    condition_on_previous_text=False
                )

                segments = list(segments_generator)

        except Exception as e:
            print(f"❌ STT GPU inference error: {e}")
            return ""

        text = " ".join(seg.text for seg in segments).strip().lower()
        text = text.replace(".", "").replace(",", "")
        return text