import collections
import time
from voice.mic_stream import MicrophoneStream
from voice.vad import VAD
from voice.stt import STT
from voice.tts import TTS
from voice.wakeword import is_wake_word
from config import MAX_SILENCE_FRAMES, WAKE_WORD
from core import IntentParser, ModeManager, SafetyRules, Mode
from execution.executor import Executor


class VoiceLoop:
    def __init__(self, allow_side_effects: bool = False):
        self.vad = VAD()
        self.stt = STT()
        self.tts = TTS()
        
        # Phase 2: Intent & Mode Engine integration
        self.intent_parser = IntentParser()
        self.mode_manager = ModeManager()
        self.safety_rules = SafetyRules()
        # Phase 3: Executor (dry-run by default unless enabled)
        import os
        env_enable = os.environ.get("ENABLE_SIDE_EFFECTS", "false").lower() in ("1", "true", "yes")
        self.executor = Executor(allow_side_effects=(allow_side_effects or env_enable))
        
        self.buffer = collections.deque()
        self.silence_frames = 0
        self.last_intent = None

    def run(self):
        print("\n" + "="*60)
        print("🎙️  Phase 1 + 2 INTEGRATED: Voice Loop with Intent Engine")
        print("="*60)

        with MicrophoneStream() as mic:
            while True:
                frame = mic.read()

                if self.vad.is_speech(frame):
                    self.buffer.append(frame)
                    self.silence_frames = 0
                else:
                    self.silence_frames += 1

                if self.silence_frames > MAX_SILENCE_FRAMES and self.buffer:
                    audio = b"".join(self.buffer)
                    self.buffer.clear()

                    text = self.stt.transcribe(audio)

                    # 🔥 Ignore tiny garbage transcriptions
                    if not text or len(text) < 3:
                        continue

                    print(f"\n🗣️  Heard: {text}")
                    
                    # Phase 2: Intent parsing and processing
                    if is_wake_word(text, WAKE_WORD):
                        self.tts.speak("Yes. I am listening.")
                        self._process_voice_input()
                    else:
                        # Parse intent even without wake word (for learning)
                        self._handle_intent(text)

    def _process_voice_input(self):
        """
        Wait for next voice input after wake word
        Temporary: just listen for next command
        """
        print("   📍 Ready for command...")
        # TODO: In Phase 3, this will wait for actual command execution

    def _handle_intent(self, text: str) -> None:
        """
        Process text through intent parser, mode manager, and safety rules
        Industry-standard intent pipeline
        """
        current_mode = self.mode_manager.get_mode()
        
        # Phase 2 Layer 1: Parse intent
        intent = self.intent_parser.parse(text, current_mode)
        self.last_intent = intent
        
        print(f"   📊 Intent: {intent.intent_type.name}")
        print(f"   📈 Confidence: {intent.confidence:.2f} ({intent.confidence_source})")
        print(f"   ⚠️  Risk Level: {intent.risk_level}/9")
        
        # Phase 2 Layer 2: Safety validation
        allowed, block_reason, requires_confirmation = self.safety_rules.validate(intent)
        
        if not allowed:
            print(f"   ❌ BLOCKED: {block_reason}")
            self.tts.speak(f"Action blocked: {block_reason}")
            return
        
        # Phase 2 Layer 3: Confirmation check
        if requires_confirmation:
            print(f"   🔐 Requires confirmation")
            self.tts.speak("This action requires confirmation. Say yes or no.")
            # TODO: In Phase 2.1, implement confirmation prompt
            return
        
        # Phase 2 Layer 4: Mode transition
        if intent.mode and intent.mode != current_mode:
            success = self.mode_manager.set_mode(intent.mode, f"intent:{intent.action}")
            if not success:
                print(f"   ⚠️  Mode transition blocked")
                return
        
        print(f"   ✅ Intent validated. Action: {intent.action}")
        if intent.target:
            print(f"   🎯 Target: {intent.target}")

        # Execute with Executor (dry-run unless allow_side_effects=True)
        result = self.executor.execute(intent)
        if result.success:
            print(f"   🟢 Execution: {result.message}")
            self.tts.speak(result.message)
        else:
            print(f"   🔴 Execution blocked/failure: {result.message}")
            self.tts.speak(result.message)
