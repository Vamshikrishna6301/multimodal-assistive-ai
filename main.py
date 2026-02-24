import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from voice.voice_loop import VoiceLoop

if __name__ == "__main__":
    assistant = VoiceLoop()
    assistant.start_production()