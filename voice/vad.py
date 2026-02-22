import webrtcvad


class VAD:
    """
    Balanced WebRTC VAD
    """

    def __init__(self):
        self.sample_rate = 16000
        self.vad = webrtcvad.Vad(2)  # balanced mode

    def is_speech(self, frame: bytes) -> bool:
        return self.vad.is_speech(frame, self.sample_rate)