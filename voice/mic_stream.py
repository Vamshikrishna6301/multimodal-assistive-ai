import sounddevice as sd


class MicrophoneStream:
    """
    Ultra-stable microphone stream.
    Uses default system input device.
    """

    def __init__(self):
        device_info = sd.query_devices(None, 'input')
        self.sample_rate = int(device_info["default_samplerate"])

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=0  # let PortAudio decide (most stable)
        )

    def __enter__(self):
        self.stream.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.stop()
        self.stream.close()

    def read(self):
        audio, _ = self.stream.read(1024)
        return audio.tobytes()

    def get_sample_rate(self):
        return self.sample_rate