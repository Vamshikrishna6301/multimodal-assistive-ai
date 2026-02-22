import sounddevice as sd
import queue


class MicrophoneStream:
    """
    VAD-compatible microphone stream.
    Fixed 16kHz, 30ms frames.
    """

    def __init__(self):

        self.sample_rate = 16000
        self.frame_duration_ms = 30
        self.frame_size = int(self.sample_rate * self.frame_duration_ms / 1000)  # 480 samples

        self.q = queue.Queue()

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.frame_size,
            callback=self._callback
        )

    def _callback(self, indata, frames, time_info, status):
        if status:
            print("Mic status:", status)
        self.q.put(indata.copy())

    def __enter__(self):
        self.stream.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.stop()
        self.stream.close()

    def read(self):
        data = self.q.get()
        return data.tobytes()

    def get_sample_rate(self):
        return self.sample_rate