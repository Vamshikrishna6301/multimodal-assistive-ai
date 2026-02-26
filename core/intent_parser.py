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
            "calculate": ("CALCULATE", 0),  # fixed
        }

        self.question_patterns = [
            r"\bwhat is\b",
            r"\bwho is\b",
            r"\bhow to\b",
            r"\bexplain\b",
            r"\bdefine\b"
        ]

        self.small_talk_patterns = [
            r"\bhello\b",
            r"\bhi\b",
            r"\bbye\b",
            r"\bthanks?\b",
            r"\bthank you\b"
        ]

        self.filler_words = {
            "the", "a", "an", "please", "for", "to",
            "about", "can", "you", "could", "would",
            "hey", "assistant", "my"
        }

    # =========================================================

    def parse(self, text: str, current_mode: Mode = Mode.COMMAND) -> Intent:

        timestamp = time.time()
        original_text = text
        text = self._normalize(text)
        text = text.replace("shut down", "shutdown")

        # =====================================================
        # STOP CAMERA
        # =====================================================

        if "stop camera" in text:
            return Intent(
                intent_type=IntentType.CONTROL,
                text=original_text,
                action="STOP_CAMERA",
                confidence=0.95,
                confidence_source="camera_control",
                risk_level=0,
                timestamp=timestamp
            )

        # =====================================================
        # START CAMERA
        # =====================================================

        if text.strip() == "open camera":
            return Intent(
                intent_type=IntentType.CONTROL,
                text=original_text,
                action="VISION",
                target="camera",
                parameters={"task": "detect_objects"},
                confidence=0.95,
                confidence_source="camera_open_rule",
                risk_level=0,
                timestamp=timestamp
            )

        # =====================================================
        # VISION QUERY RULES
        # =====================================================

        match = re.search(r"\bwhere is (?:my )?(?P<object>\w+)", text)
        if match:
            obj_name = match.group("object")
            return Intent(
                intent_type=IntentType.QUESTION,
                text=original_text,
                action="VISION_QUERY",
                target=obj_name,
                parameters={"query_type": "location"},
                confidence=0.92,
                confidence_source="vision_where_rule",
                risk_level=0,
                timestamp=timestamp
            )

        match = re.search(r"\bhow many (?P<object>\w+)", text)
        if match:
            obj_name = match.group("object")
            return Intent(
                intent_type=IntentType.QUESTION,
                text=original_text,
                action="VISION_QUERY",
                target=obj_name,
                parameters={"query_type": "count"},
                confidence=0.9,
                confidence_source="vision_count_rule",
                risk_level=0,
                timestamp=timestamp
            )

        if "anyone" in text or "anybody" in text:
            return Intent(
                intent_type=IntentType.QUESTION,
                text=original_text,
                action="VISION_QUERY",
                target="person",
                parameters={"query_type": "presence"},
                confidence=0.9,
                confidence_source="vision_presence_rule",
                risk_level=0,
                timestamp=timestamp
            )

        if "what do you see" in text or "what can you see" in text:
            return Intent(
                intent_type=IntentType.QUESTION,
                text=original_text,
                action="VISION_QUERY",
                parameters={"query_type": "summary"},
                confidence=0.9,
                confidence_source="vision_summary_rule",
                risk_level=0,
                timestamp=timestamp
            )

        # =====================================================
        # TIME QUERY
        # =====================================================

        if re.search(r"\btime\b", text):
            return Intent(
                intent_type=IntentType.QUESTION,
                text=original_text,
                action="GET_TIME",
                confidence=0.95,
                confidence_source="keyword_time",
                risk_level=0,
                timestamp=timestamp
            )

        # =====================================================
        # KNOWLEDGE QUESTIONS
        # =====================================================

        for pattern in self.question_patterns:
            if re.search(pattern, text):
                return Intent(
                    intent_type=IntentType.QUESTION,
                    text=original_text,
                    action="KNOWLEDGE_QUERY",
                    target=original_text,
                    confidence=0.9,
                    confidence_source="regex",
                    risk_level=0,
                    timestamp=timestamp
                )

        # =====================================================
        # GENERIC COMMANDS
        # =====================================================

        intent_type, risk_level, keyword = self._detect_command(text)

        if intent_type:

            # Special case: calculate
            if keyword == "calculate":
                expression = text.replace("calculate", "").strip()
                return Intent(
                    intent_type=IntentType.QUESTION,
                    text=original_text,
                    action="CALCULATE",
                    target=expression,
                    confidence=0.95,
                    confidence_source="keyword_rule",
                    risk_level=0,
                    timestamp=timestamp
                )

            target = self._extract_target(text, keyword)

            return Intent(
                intent_type=intent_type,
                text=original_text,
                action=intent_type.name,
                target=target,
                parameters={"target": target} if target else {},
                confidence=0.95 if risk_level < 7 else 0.85,
                confidence_source="keyword_rule",
                risk_level=risk_level,
                requires_confirmation=risk_level >= 7,
                timestamp=timestamp
            )

        # =====================================================
        # SMALL TALK (Moved to bottom)
        # =====================================================

        for pattern in self.small_talk_patterns:
            if re.search(pattern, text):
                return Intent(
                    intent_type=IntentType.UNKNOWN,
                    text=original_text,
                    action="SMALL_TALK",
                    confidence=0.7,
                    confidence_source="small_talk",
                    risk_level=0,
                    timestamp=timestamp
                )

        # =====================================================
        # FALLBACK
        # =====================================================

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

    def _detect_command(self, text: str) -> Tuple[Optional[IntentType], int, Optional[str]]:
        for keyword, value in self.command_keywords.items():
            if re.search(rf"\b{keyword}\b", text):
                if keyword == "calculate":
                    return IntentType.QUESTION, 0, keyword
                return value[0], value[1], keyword
        return None, 0, None

    # =========================================================

    def _extract_target(self, text: str, keyword: str) -> Optional[str]:
        parts = text.split(keyword, 1)
        if len(parts) < 2:
            return None
        tokens = parts[1].strip().split()
        cleaned = [t for t in tokens if t not in self.filler_words]
        return " ".join(cleaned).strip() or None

    # =========================================================

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text