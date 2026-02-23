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

        self.fusion = FusionEngine()
        self.router = DecisionRouter()

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

                MIN_SPEECH_FRAMES = 8  # ~240ms minimum speech

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
                print("DEBUG: waiting for audio")

                try:
                    audio = self.audio_queue.get(timeout=1)
                except queue.Empty:
                    continue

                print("DEBUG: running transcribe")

                text = self.stt.transcribe(audio, 16000)

                if not text:
                    continue

                words = text.split()

                if len(words) <= 1 and text not in ["stop", "exit", "yes", "no"]:
                    continue
                if self.runtime.is_speaking():
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

                text = text.lower().strip()

                if "exit assistant" in text or text in ["exit", "quit"]:
                    print("🛑 Assistant shutting down...")
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

                if text in ["okay", "ok"]:
                    continue

                if text in ["stop", "cancel", "abort"]:
                    print("🛑 Interrupting speech...")
                    self.tts.stop()
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
            print(f"🚫 {message}")
            self.tts.speak(message or "Action blocked.")
            return

        if status == "NEEDS_CONFIRMATION":
            print(f"🔐 {message}")
            self.tts.speak(message or "Please confirm.")
            return

        if status == "APPROVED":

            response = self.router.route(decision_dict)

            if response and hasattr(response, "spoken_message"):
                print(f"🤖 Assistant: {response.spoken_message}")
                self.tts.speak(response.spoken_message)
            else:
                print("🤖 Assistant: Done.")
                self.tts.speak("Done.")