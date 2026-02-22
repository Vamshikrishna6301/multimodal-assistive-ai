from voice.voice_loop import VoiceLoop

if __name__ == "__main__":
    # Enable real side-effects when launching from CLI
    VoiceLoop(allow_side_effects=True).run()
