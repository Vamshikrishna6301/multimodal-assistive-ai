import time
import re
from typing import Dict

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

    # 🔥 FIXED: parameters now preserved
    def to_dict(self) -> Dict:
        return {
            "status": self.status,
            "action": self.intent.action if self.intent else None,
            "target": self.intent.target if self.intent else None,
            "parameters": self.intent.parameters if self.intent else {},
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

        self.intent_confidence_threshold = 0.4

    def process_text(self, text: str) -> Decision:

        start_time = time.time()
        text = self._normalize_input(text)

        intent = self.parser.parse(
            text,
            current_mode=self.mode_manager.get_mode()
        )

        if intent.intent_type == IntentType.CONTROL:
            self._handle_mode_control(intent)

        # Enrich context
        intent = self.memory.enrich(intent)

        # Safety evaluation
        intent = self.safety.evaluate(intent, self.mode_manager.get_mode())

        if intent.blocked_reason:
            return self._finalize(
                Decision("BLOCKED", intent, intent.blocked_reason),
                start_time
            )

        if intent.confidence < self.intent_confidence_threshold and intent.action == "UNKNOWN":
            return self._finalize(
                Decision("BLOCKED", intent, "Low confidence input"),
                start_time
            )

        if intent.requires_confirmation:
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

    def _normalize_input(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def _finalize(self, decision: Decision, start_time: float) -> Decision:
        decision.latency = time.time() - start_time
        return decision