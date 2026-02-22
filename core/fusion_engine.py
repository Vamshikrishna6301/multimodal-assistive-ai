import time
import re
from typing import Optional, Dict

from .intent_schema import Intent, IntentType, Mode
from .intent_parser import IntentParser
from .mode_manager import ModeManager
from .context_memory import ContextMemory
from .safety_engine import SafetyEngine


class Decision:

    def __init__(self, status, intent=None, message=None, latency=None):
        self.status = status
        self.intent = intent
        self.message = message
        self.latency = latency

    def to_dict(self) -> Dict:
        return {
            "status": self.status,
            "action": self.intent.action if self.intent else None,
            "target": self.intent.target if self.intent else None,
            "risk_level": self.intent.risk_level if self.intent else None,
            "requires_confirmation": self.intent.requires_confirmation if self.intent else None,
            "blocked_reason": self.intent.blocked_reason if self.intent else None,
            "message": self.message,
            "latency_ms": round(self.latency * 1000, 2) if self.latency else None
        }


class FusionEngine:

    def __init__(self):
        self.parser = IntentParser()
        self.mode_manager = ModeManager()
        self.memory = ContextMemory()
        self.safety = SafetyEngine()

        self.pending_confirmation = None
        self.confirmation_timestamp = None
        self.confirmation_timeout = 10

        self.intent_confidence_threshold = 0.4  # relaxed

    # =========================================================

    def process_text(self, text: str) -> Decision:

        start_time = time.time()
        text = self._normalize_input(text)

        if self.pending_confirmation:
            if self._confirmation_expired():
                expired = self.pending_confirmation
                self._clear_confirmation()
                return self._finalize(
                    Decision("BLOCKED", expired, "Confirmation timed out"),
                    start_time
                )
            return self._finalize(
                self._handle_confirmation(text),
                start_time
            )

        intent = self.parser.parse(
            text,
            current_mode=self.mode_manager.get_mode()
        )

        if intent.intent_type == IntentType.CONTROL:
            self._handle_mode_control(intent)

        intent = self.memory.enrich(intent)
        self.memory.update(intent)

        intent = self.safety.evaluate(intent, self.mode_manager.get_mode())

        if intent.blocked_reason:
            return self._finalize(
                Decision("BLOCKED", intent, intent.blocked_reason),
                start_time
            )

        # 🔥 Only block low confidence if action is UNKNOWN
        if intent.confidence < self.intent_confidence_threshold and intent.action == "UNKNOWN":
            return self._finalize(
                Decision("BLOCKED", intent, "Low confidence input"),
                start_time
            )

        if intent.requires_confirmation:
            self.pending_confirmation = intent
            self.confirmation_timestamp = time.time()
            return self._finalize(
                Decision(
                    "NEEDS_CONFIRMATION",
                    intent,
                    f"Confirm action: {intent.action} {intent.target}"
                ),
                start_time
            )

        return self._finalize(
            Decision("APPROVED", intent, "Action approved"),
            start_time
        )

    # =========================================================

    def _handle_confirmation(self, text: str) -> Decision:

        if text.startswith(("yes", "confirm", "proceed", "do it")):
            confirmed = self.pending_confirmation
            self._clear_confirmation()
            return Decision("APPROVED", confirmed, "Action confirmed")

        if text.startswith(("no", "cancel", "stop")):
            cancelled = self.pending_confirmation
            self._clear_confirmation()
            return Decision("BLOCKED", cancelled, "Action cancelled")

        return Decision(
            "NEEDS_CONFIRMATION",
            self.pending_confirmation,
            "Please respond with yes or no"
        )

    # =========================================================

    def _handle_mode_control(self, intent: Intent):
        text = intent.text.lower()

        if "enter dictation" in text:
            self.mode_manager.set_mode(Mode.DICTATION, "dictation_mode_enabled")
        elif "exit dictation" in text:
            self.mode_manager.set_mode(Mode.COMMAND, "exit_dictation")
        elif "disable" in text:
            self.mode_manager.set_mode(Mode.DISABLED, "disable_command")
        elif "enable" in text:
            self.mode_manager.set_mode(Mode.LISTENING, "enable_assistant")

    # =========================================================

    def _normalize_input(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def _confirmation_expired(self) -> bool:
        if not self.confirmation_timestamp:
            return False
        return (time.time() - self.confirmation_timestamp) > self.confirmation_timeout

    def _clear_confirmation(self):
        self.pending_confirmation = None
        self.confirmation_timestamp = None

    def _finalize(self, decision: Decision, start_time: float) -> Decision:
        decision.latency = time.time() - start_time
        return decision