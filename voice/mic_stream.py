import sounddevice as sd
from config import SAMPLE_RATE, CHANNELS

class MicrophoneStream:
    def __init__(self):
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=int(SAMPLE_RATE * 0.03),
        )

    def __enter__(self):
        self.stream.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.stop()
        self.stream.close()

    def read(self):
        audio, _ = self.stream.read(self.stream.blocksize)
        return audio.tobytes()
