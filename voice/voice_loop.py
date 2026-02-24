import collections
import time
import queue
import threading

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

        self.runtime = runtime or AssistantRuntime()

        self.vad = VAD()
        self.stt = STT()
        self.tts = TTS(runtime=self.runtime)

        # Fusion owns ContextMemory
        self.fusion = FusionEngine()

        # Inject shared memory into router
# Inject TTS into VisionExecutor
        self.router = DecisionRouter(self.fusion.memory)
        self.router.execution_engine.dispatcher.vision_executor.set_tts(self.tts)
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()

        self.buffer = collections.deque()
        self.silence_frames = 0

        self._threads = []

    # =====================================================
    # START PRODUCTION
    # =====================================================

    def start_production(self):

        print("\n" + "=" * 60)
        print("🚀 PRODUCTION VOICE ASSISTANT STARTED")
        print("=" * 60)

        self._start_threads()

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
    # THREAD MANAGEMENT
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

                # Wait briefly if assistant speaking
                wait_start = time.time()
                while self.runtime.is_speaking() and (time.time() - wait_start) < 2.0:
                    time.sleep(0.05)

                text = self.stt.transcribe(audio, 16000)

                if not text:
                    continue

                text = text.strip()
                print(f"\n🗣️ Heard: {text}")

                # Always allow confirmation words
                if text.lower() in ["yes", "y", "confirm", "no", "n", "cancel"]:
                    self.text_queue.put(text)
                    continue

                words = text.split()

                # Skip useless noise
                if len(words) <= 1 and text.lower() not in ["stop", "exit"]:
                    continue

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

                text = text.lower().strip()

                # ---------------------------------------------
                # CONFIRMATION HANDLING
                # ---------------------------------------------
                if self.runtime.is_awaiting_confirmation():

                    print("DEBUG: awaiting confirmation, got:", text)

                    if text in ["yes", "y", "confirm"]:

                        print("🔒 Confirmation received: executing pending action")

                        pending = self.runtime.pending_intent
                        self._execute_confirmed(pending)

                        self.runtime.clear_confirmation()
                        continue

                    if text in ["no", "n", "cancel"]:
                        print("🔐 Confirmation declined: cancelling action")
                        print("🤖 Assistant: Action cancelled.")
                        self.tts.speak("Action cancelled.")
                        self.runtime.clear_confirmation()
                        continue

                    print("DEBUG: still awaiting confirmation; ignoring input")
                    continue

                # ---------------------------------------------
                # SYSTEM COMMANDS
                # ---------------------------------------------
                if "exit" in text or "quit" in text:
                    print("🛑 Assistant shutting down...")
                    print("🤖 Assistant: Shutting down assistant.")
                    self.tts.speak("Shutting down assistant.")
                    self.runtime.stop()
                    return

                if text in ["hello", "hi"]:
                    print("🤖 Assistant: Hello! How can I help you?")
                    self.tts.speak("Hello! How can I help you?")
                    continue

                if text in ["thank you", "thanks"]:
                    print("🤖 Assistant: You're welcome.")
                    self.tts.speak("You're welcome.")
                    continue

                if text in ["stop", "cancel", "abort"]:
                    print("🛑 Interrupting speech...")
                    self.tts.stop()
                    continue
                if text == "stop camera":
                    print("🛑 Stopping camera...")
                    self.router.execution_engine.dispatcher.vision_executor.camera_detector.stop()
                    continue

                self._handle_intent(text)

            except Exception as e:
                print("⚠️ Intent worker crashed:", e)

    # =====================================================
    # HANDLE INTENT
    # =====================================================

    def _handle_intent(self, text: str):

        decision = self.fusion.process_text(text)
        decision_dict = decision.to_dict()

        status = decision_dict.get("status")
        message = decision_dict.get("message")

        print(f"📊 Decision Status: {status}")

        if status == "BLOCKED":

    # Ignore low confidence noise silently
            if message == "Low confidence input":
                print("… Ignored low confidence input")
                return

            print(f"🚫 {message}")
            self.tts.speak(message or "Action blocked.")
            return
        
        if status == "NEEDS_CONFIRMATION":
            print(f"🔐 {message}")
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
                print("🤖 Assistant: Done.")
                self.tts.speak("Done.")

    # =====================================================
    # EXECUTE CONFIRMED
    # =====================================================

    def _execute_confirmed(self, decision_dict: dict):

        try:
            if not decision_dict:
                print("🤖 Assistant: No pending action.")
                self.tts.speak("No pending action.")
                return

            confirmed_decision = decision_dict.copy()
            confirmed_decision["status"] = "APPROVED"
            confirmed_decision["confirmed"] = True

            self.runtime.start_execution()
            response = self.router.route(confirmed_decision)
            self.runtime.finish_execution()

            if response and hasattr(response, "spoken_message"):
                print(f"🤖 Assistant: {response.spoken_message}")
                self.tts.speak(response.spoken_message)
            else:
                print("🤖 Assistant: Done.")
                self.tts.speak("Done.")

        except Exception as e:
            print("⚠️ Execution after confirmation failed:", e)
            self.tts.speak("I failed to execute the action.")