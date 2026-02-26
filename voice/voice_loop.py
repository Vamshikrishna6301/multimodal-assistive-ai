import collections
import time
import queue
import threading
import re

from voice.mic_stream import MicrophoneStream
from voice.vad import VAD
from voice.stt import STT
from voice.tts import TTS
from voice.assistant_runtime import AssistantRuntime

from config import MAX_SILENCE_FRAMES
from core.fusion_engine import FusionEngine
from router.decision_router import DecisionRouter


class VoiceLoop:

    def __init__(self, runtime: AssistantRuntime = None):

        print("🔧 Initializing Voice Assistant components...")
        
        self.runtime = runtime or AssistantRuntime()
        print("  ✓ Runtime initialized")

        self.vad = VAD()
        print("  ✓ VAD initialized")
        
        self.stt = STT()
        print("  ✓ STT initialized (Whisper loaded)")
        
        self.tts = TTS(runtime=self.runtime)
        print("  ✓ TTS initialized")

        self.fusion = FusionEngine()
        print("  ✓ Fusion engine initialized")

        self.router = DecisionRouter(self.fusion.memory)
        self.router.execution_engine.dispatcher.vision_executor.set_tts(self.tts)
        print("  ✓ Router initialized")
        
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()

        self.buffer = collections.deque()
        self.silence_frames = 0

        self._threads = []
        
        print("✅ All components initialized successfully!\n")

    # =====================================================
    # START
    # =====================================================

    def start_production(self):

        print("\n" + "=" * 60)
        print("🚀 PRODUCTION VOICE ASSISTANT STARTED")
        print("=" * 60)
        print("📢 Initializing audio threads...")

        self._start_threads()
        
        print("✅ All threads started. Ready to listen for voice commands.")
        print("   Speak clearly when ready... (say 'stop' to exit)\n")

        try:
            while self.runtime.running:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received.")
            self.runtime.stop()

        print("🧹 Cleaning up threads...")
        for t in self._threads:
            t.join(timeout=2)

        print("✅ Assistant terminated cleanly.")

    # =====================================================
    # THREADS
    # =====================================================

    def _start_threads(self):

        workers = [
            self._mic_worker,
            self._stt_worker,
            self._intent_worker
        ]

        for worker in workers:
            t = threading.Thread(target=worker)
            t.start()
            self._threads.append(t)

    # =====================================================
    # MIC WORKER
    # =====================================================

    def _mic_worker(self):

        try:
            with MicrophoneStream() as mic:

                MIN_SPEECH_FRAMES = 8

                while self.runtime.running:

                    frame = mic.read()

                    if self.vad.is_speech(frame):
                        self.buffer.append(frame)
                        self.silence_frames = 0
                    else:
                        self.silence_frames += 1

                    if (
                        self.silence_frames > MAX_SILENCE_FRAMES
                        and len(self.buffer) > MIN_SPEECH_FRAMES
                    ):
                        audio = b"".join(self.buffer)
                        self.buffer.clear()
                        self.silence_frames = 0
                        self.audio_queue.put(audio)

        except Exception as e:
            print("⚠️ Mic worker crashed:", e)
            self.runtime.stop()

    # =====================================================
    # STT WORKER
    # =====================================================

    def _stt_worker(self):

        while self.runtime.running:

            try:
                try:
                    audio = self.audio_queue.get(timeout=1)
                except queue.Empty:
                    continue

                wait_start = time.time()
                while self.runtime.is_speaking() and (time.time() - wait_start) < 2.0:
                    time.sleep(0.05)

                text = self.stt.transcribe(audio, 16000)

                if not text:
                    continue

                print(f"\n🗣️ Heard: {text}")

                self.text_queue.put(text)

            except Exception as e:
                print("⚠️ STT worker crashed:", e)

    # =====================================================
    # INTENT WORKER
    # =====================================================

    def _intent_worker(self):

        while self.runtime.running:

            try:
                try:
                    text = self.text_queue.get(timeout=1)
                except queue.Empty:
                    continue

                clean_text = self._normalize(text)

                # =====================================================
                # HARD SYSTEM INTERRUPTS (Highest Priority)
                # =====================================================

                if self._is_exit_command(clean_text):
                    print("🛑 Assistant shutting down...")
                    self.tts.stop()
                    self.tts.speak("Shutting down assistant.")
                    self.runtime.stop()
                    return

                if self._is_stop_command(clean_text):
                    print("🛑 Interrupting speech...")
                    self.tts.stop()
                    continue

                # =====================================================
                # Confirmation handling
                # =====================================================

                if self.runtime.is_awaiting_confirmation():

                    if clean_text in ["yes", "y", "confirm"]:
                        pending = self.runtime.pending_intent
                        self._execute_confirmed(pending)
                        self.runtime.clear_confirmation()
                        continue

                    if clean_text in ["no", "n", "cancel"]:
                        print("🤖 Assistant: Action cancelled.")
                        self.tts.speak("Action cancelled.")
                        self.runtime.clear_confirmation()
                        continue

                    continue

                # =====================================================
                # Social small talk
                # =====================================================

                if clean_text in ["hello", "hi"]:
                    self.tts.speak("Hello! How can I help you?")
                    continue

                if clean_text in ["thank you", "thanks"]:
                    self.tts.speak("You're welcome.")
                    continue

                # =====================================================
                # Normal Intent Handling
                # =====================================================

                self._handle_intent(clean_text)

            except Exception as e:
                print("⚠️ Intent worker crashed:", e)

    # =====================================================
    # INTENT ROUTING
    # =====================================================

    def _handle_intent(self, text: str):

        decision = self.fusion.process_text(text)
        decision_dict = decision.to_dict()

        status = decision_dict.get("status")
        message = decision_dict.get("message")

        print(f"📊 Decision Status: {status}")

        if status == "BLOCKED":
            if message == "Low confidence input":
                print("… Ignored low confidence input")
                return
            self.tts.speak(message or "Action blocked.")
            return
        
        if status == "NEEDS_CONFIRMATION":
            self.runtime.set_confirmation(decision_dict)
            self.tts.speak(message or "Please confirm.")
            return

        if status == "APPROVED":

            self.runtime.start_execution()
            response = self.router.route(decision_dict)
            self.runtime.finish_execution()

            if response and hasattr(response, "spoken_message"):
                print(f"🤖 Assistant: {response.spoken_message}")
                self.tts.speak(response.spoken_message)
            else:
                self.tts.speak("Done.")

    # =====================================================
    # CONFIRMED EXECUTION
    # =====================================================

    def _execute_confirmed(self, decision_dict: dict):

        if not decision_dict:
            self.tts.speak("No pending action.")
            return

        confirmed_decision = decision_dict.copy()
        confirmed_decision["status"] = "APPROVED"
        confirmed_decision["confirmed"] = True

        self.runtime.start_execution()
        response = self.router.route(confirmed_decision)
        self.runtime.finish_execution()

        if response and hasattr(response, "spoken_message"):
            self.tts.speak(response.spoken_message)
        else:
            self.tts.speak("Done.")

    # =====================================================
    # UTILITIES
    # =====================================================

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def _is_stop_command(self, text: str) -> bool:
        return text.startswith("stop") or text in ["cancel", "abort"]

    def _is_exit_command(self, text: str) -> bool:
        return text in ["exit", "quit", "shutdown assistant"]