"""
Context Memory - Phase 3 (Production Grade + Reference Resolution)

Short-term session memory with inference support.
Designed for multi-turn conversational reasoning.
Thread-safe.
"""

import time
from typing import Optional, List, Dict
from threading import Lock

from .intent_schema import Intent


class ContextMemory:
    """
    Production-ready short-term conversational memory.
    Now supports:
    - Reference resolution ("it", "that")
    - Active app tracking
    - Topic carry-forward
    """

    def __init__(self, max_history: int = 20):
        self.session_id: str = str(int(time.time()))
        self.max_history = max_history
        self.history: List[Intent] = []

        self.last_app: Optional[str] = None
        self.last_file: Optional[str] = None
        self.last_topic: Optional[str] = None

        self.lock = Lock()

    # =====================================================
    # PUBLIC API
    # =====================================================

    def enrich(self, intent: Intent) -> Intent:
        """
        Enrich intent using stored conversational memory.
        """

        with self.lock:

            # ---------------------------------------------
            # Reference Resolution (NEW)
            # ---------------------------------------------
            if intent.target:
                resolved = self.resolve_reference(intent.target)
                if resolved:
                    intent.target = resolved
                    intent.context["reference_resolved"] = True

            # ---------------------------------------------
            # Infer SEARCH target
            # ---------------------------------------------
            if intent.action == "SEARCH" and not intent.target:
                if self.last_app:
                    intent.target = self.last_app
                    intent.context["inferred_from"] = "last_app"
                    intent.context["inference_confidence"] = 0.85

            # ---------------------------------------------
            # Infer DELETE target
            # ---------------------------------------------
            if intent.action == "DELETE" and not intent.target:
                if self.last_file:
                    intent.target = self.last_file
                    intent.context["inferred_from"] = "last_file"
                    intent.context["inference_confidence"] = 0.80

            # ---------------------------------------------
            # Attach previous topic for follow-up questions
            # ---------------------------------------------
            if intent.intent_type.name == "QUESTION" and not intent.context.get("topic"):
                if self.last_topic:
                    intent.context["previous_topic"] = self.last_topic

        return intent

    # -----------------------------------------------------

    def update(self, intent: Intent) -> None:
        """
        Update memory state from processed intent.
        """

        with self.lock:

            # Maintain bounded history
            self.history.append(intent)
            if len(self.history) > self.max_history:
                self.history.pop(0)

            # ---------------------------------------------
            # Update last app
            # ---------------------------------------------
            if intent.action == "OPEN_APP" and intent.target:
                self.last_app = intent.target

            # If closing app, clear active app
            if intent.action == "SYSTEM_CONTROL" and intent.target:
                if self.last_app == intent.target:
                    self.last_app = None

            # ---------------------------------------------
            # Update last file
            # ---------------------------------------------
            if intent.action in ["DELETE", "OPEN_FILE"] and intent.target:
                self.last_file = intent.target

            # ---------------------------------------------
            # Update last topic
            # ---------------------------------------------
            if intent.intent_type.name == "QUESTION":
                self.last_topic = intent.text

    # -----------------------------------------------------

    def resolve_reference(self, target: Optional[str]) -> Optional[str]:
        """
        Resolve pronoun-based references like:
        - it
        - that
        - this

        Returns resolved target if possible.
        """

        if not target:
            return target

        target = target.lower().strip()

        if target in ["it", "that", "this"]:
            return self.last_app or self.last_file

        return target

    # -----------------------------------------------------

    def get_last_intent(self) -> Optional[Intent]:
        if not self.history:
            return None
        return self.history[-1]

    # -----------------------------------------------------

    def clear(self) -> None:
        """
        Clear session memory.
        """
        with self.lock:
            self.history.clear()
            self.last_app = None
            self.last_file = None
            self.last_topic = None

    # -----------------------------------------------------

    def get_memory_snapshot(self) -> Dict:
        """
        Debug view of memory state.
        """
        return {
            "session_id": self.session_id,
            "last_app": self.last_app,
            "last_file": self.last_file,
            "last_topic": self.last_topic,
            "history_size": len(self.history)
        }