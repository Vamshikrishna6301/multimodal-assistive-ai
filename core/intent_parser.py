"""
Intent Parser - Phase 2 (Production Hardened)

Deterministic rule-based parser with:
- Input normalization
- Filler word removal
- Cleaner entity extraction
- Robust command detection
"""

import re
import time
from typing import Dict, Optional

from core.intent_schema import (
    Intent,
    IntentType,
    Mode,
    Entity
)


class IntentParser:

    def __init__(self):

        # Order matters (longer phrases first)
        self.command_keywords = {
            "open": "OPEN_APP",
            "close": "CLOSE_APP",
            "delete": "DELETE",
            "remove": "DELETE",
            "shutdown": "SHUTDOWN",
            "restart": "RESTART",
            "search": "SEARCH",
            "type": "TYPE_TEXT",
            "write": "TYPE_TEXT"
        }

        self.question_patterns = [
            r"\bwhat is\b",
            r"\bwho is\b",
            r"\bhow to\b",
            r"\bexplain\b",
            r"\bdefine\b"
        ]

        self.control_patterns = [
            "enable",
            "disable",
            "switch mode",
            "enter dictation",
            "exit dictation"
        ]

        # Common filler words to ignore in targets
        self.filler_words = {"the", "a", "an", "please", "for", "to"}

    # =========================================================

    def parse(self, text: str, current_mode: Mode = Mode.COMMAND) -> Intent:
        timestamp = time.time()
        original_text = text
        text = self._normalize(text)

        # -----------------------------------------------------
        # Dictation override
        # -----------------------------------------------------
        if current_mode == Mode.DICTATION:
            return self._create_dictation_intent(original_text, timestamp)

        # -----------------------------------------------------
        # Question detection
        # -----------------------------------------------------
        for pattern in self.question_patterns:
            if re.search(pattern, text):
                return self._create_question_intent(original_text, timestamp)

        # -----------------------------------------------------
        # Control detection
        # -----------------------------------------------------
        for pattern in self.control_patterns:
            if pattern in text:
                return self._create_control_intent(original_text, timestamp)

        # -----------------------------------------------------
        # Command detection
        # -----------------------------------------------------
        action, keyword = self._detect_command(text)

        if action:
            target = self._extract_target(text, keyword)
            return self._create_command_intent(
                original_text,
                action,
                target,
                timestamp
            )

        # -----------------------------------------------------
        # Fallback
        # -----------------------------------------------------
        return Intent(
            intent_type=IntentType.UNKNOWN,
            text=original_text,
            action="UNKNOWN",
            confidence=0.3,
            confidence_source="fallback",
            timestamp=timestamp
        )

    # =========================================================
    # Command Detection
    # =========================================================

    def _detect_command(self, text: str) -> (Optional[str], Optional[str]):

        for keyword, action in self.command_keywords.items():

            # Match at start OR after polite phrases
            pattern = rf"^(please\s+)?{keyword}\b"

            if re.search(pattern, text):
                return action, keyword

        return None, None

    # =========================================================
    # Target Extraction
    # =========================================================

    def _extract_target(self, text: str, keyword: str) -> Optional[str]:

        # Remove leading keyword
        text = re.sub(rf"^(please\s+)?{keyword}\b", "", text).strip()

        if not text:
            return None

        tokens = text.split()
        cleaned_tokens = [
            token for token in tokens
            if token not in self.filler_words
        ]

        target = " ".join(cleaned_tokens).strip()

        return target if target else None

    # =========================================================
    # Intent Creators
    # =========================================================

    def _create_command_intent(
        self,
        original_text: str,
        action: str,
        target: Optional[str],
        timestamp: float
    ) -> Intent:

        entities: Dict[str, Entity] = {}

        if target:
            entities["target"] = Entity(
                name="target",
                value=target,
                confidence=0.9,
                entity_type="keyword"
            )

        return Intent(
            intent_type=IntentType.COMMAND,
            text=original_text,
            action=action,
            target=target,
            confidence=0.95,
            confidence_source="keyword",
            entities=entities,
            timestamp=timestamp
        )

    # ---------------------------------------------------------

    def _create_question_intent(self, original_text: str, timestamp: float):

        return Intent(
            intent_type=IntentType.QUESTION,
            text=original_text,
            action="ANSWER_QUESTION",
            confidence=0.9,
            confidence_source="regex",
            mode=Mode.QUESTION,
            timestamp=timestamp
        )

    # ---------------------------------------------------------

    def _create_control_intent(self, original_text: str, timestamp: float):

        return Intent(
            intent_type=IntentType.CONTROL,
            text=original_text,
            action="SYSTEM_CONTROL",
            confidence=0.85,
            confidence_source="keyword",
            timestamp=timestamp
        )

    # ---------------------------------------------------------

    def _create_dictation_intent(self, original_text: str, timestamp: float):

        return Intent(
            intent_type=IntentType.DICTATION,
            text=original_text,
            action="TYPE_TEXT",
            confidence=0.99,
            confidence_source="mode_override",
            mode=Mode.DICTATION,
            timestamp=timestamp
        )

    # =========================================================
    # Normalization
    # =========================================================

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        return text
