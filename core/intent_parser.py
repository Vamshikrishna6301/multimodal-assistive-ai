"""
Intent Parser - Phase 2 Production Upgrade (Flexible NLP)

Upgraded to:
- Keyword detection anywhere in sentence
- Multi-word normalization (shut down → shutdown)
- Natural speech tolerance
- Structured parameters
- Risk scoring
- Confirmation flagging
"""

import re
import time
from typing import Dict, Optional, Tuple

from core.intent_schema import (
    Intent,
    IntentType,
    Mode,
    Entity
)


class IntentParser:

    def __init__(self):

        # Keyword → (IntentType, risk_level)
        self.command_keywords = {
            "open": (IntentType.OPEN_APP, 1),
            "close": (IntentType.SYSTEM_CONTROL, 2),
            "delete": (IntentType.FILE_OPERATION, 8),
            "remove": (IntentType.FILE_OPERATION, 8),
            "shutdown": (IntentType.SYSTEM_CONTROL, 9),
            "restart": (IntentType.SYSTEM_CONTROL, 7),
            "search": (IntentType.SEARCH, 1),
            "type": (IntentType.TYPE_TEXT, 1),
            "write": (IntentType.TYPE_TEXT, 1),
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

        self.filler_words = {
            "the", "a", "an", "please", "for", "to",
            "about", "can", "you", "could", "would",
            "hey", "assistant"
        }

    # =========================================================
    # MAIN PARSE
    # =========================================================

    def parse(self, text: str, current_mode: Mode = Mode.COMMAND) -> Intent:

        timestamp = time.time()
        original_text = text
        text = self._normalize(text)

        # Normalize common variations
        text = text.replace("shut down", "shutdown")

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
        intent_type, risk_level, keyword = self._detect_command(text)

        if intent_type:
            target = self._extract_target(text, keyword)
            return self._create_command_intent(
                original_text,
                intent_type,
                target,
                risk_level,
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
            risk_level=0,
            timestamp=timestamp
        )

    # =========================================================
    # COMMAND DETECTION
    # =========================================================

    def _detect_command(self, text: str) -> Tuple[Optional[IntentType], int, Optional[str]]:

        for keyword, (intent_type, risk_level) in self.command_keywords.items():

            # Match keyword anywhere in sentence
            pattern = rf"\b{keyword}\b"

            if re.search(pattern, text):
                return intent_type, risk_level, keyword

        return None, 0, None

    # =========================================================
    # TARGET EXTRACTION
    # =========================================================

    def _extract_target(self, text: str, keyword: str) -> Optional[str]:

        parts = text.split(keyword, 1)

        if len(parts) < 2:
            return None

        text_after_keyword = parts[1].strip()

        if not text_after_keyword:
            return None

        tokens = text_after_keyword.split()

        cleaned_tokens = [
            token for token in tokens
            if token not in self.filler_words
        ]

        target = " ".join(cleaned_tokens).strip()

        return target if target else None

    # =========================================================
    # INTENT CREATORS
    # =========================================================

    def _create_command_intent(
        self,
        original_text: str,
        intent_type: IntentType,
        target: Optional[str],
        risk_level: int,
        timestamp: float
    ) -> Intent:

        entities: Dict[str, Entity] = {}
        parameters: Dict[str, str] = {}

        if target:
            entities["target"] = Entity(
                name="target",
                value=target,
                confidence=0.9
            )
            parameters["target"] = target

        requires_confirmation = risk_level >= 7

        return Intent(
            intent_type=intent_type,
            text=original_text,
            action=intent_type.name,
            target=target,
            parameters=parameters,
            confidence=0.95 if risk_level < 7 else 0.85,
            confidence_source="keyword_rule",
            entities=entities,
            risk_level=risk_level,
            requires_confirmation=requires_confirmation,
            timestamp=timestamp
        )

    # ---------------------------------------------------------

    def _create_question_intent(self, original_text: str, timestamp: float) -> Intent:

        return Intent(
            intent_type=IntentType.QUESTION,
            text=original_text,
            action="ANSWER_QUESTION",
            confidence=0.9,
            confidence_source="regex",
            mode=Mode.QUESTION,
            risk_level=0,
            timestamp=timestamp
        )

    # ---------------------------------------------------------

    def _create_control_intent(self, original_text: str, timestamp: float) -> Intent:

        return Intent(
            intent_type=IntentType.CONTROL,
            text=original_text,
            action="SYSTEM_CONTROL",
            confidence=0.85,
            confidence_source="keyword",
            risk_level=2,
            timestamp=timestamp
        )

    # ---------------------------------------------------------

    def _create_dictation_intent(self, original_text: str, timestamp: float) -> Intent:

        return Intent(
            intent_type=IntentType.DICTATION,
            text=original_text,
            action="TYPE_TEXT",
            confidence=0.99,
            confidence_source="mode_override",
            mode=Mode.DICTATION,
            risk_level=0,
            timestamp=timestamp
        )

    # =========================================================
    # NORMALIZATION
    # =========================================================

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text