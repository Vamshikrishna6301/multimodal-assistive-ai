"""
Intent Parser - Phase 2
Multi-layered intent parsing engine
Implements Mycroft dual-engine (keyword + regex) + confidence scoring
"""

import re
from typing import Optional, Tuple, Dict
from datetime import datetime
from .intent_schema import Intent, IntentType, Mode, Entity, ConfidenceLevel


class IntentParser:
    """
    Industry-standard intent parser combining:
    - Keyword matching (Mycroft Adapt layer)
    - Regex patterns (structured extraction)
    - Confidence scoring (0.0-1.0)
    - Context awareness
    """
    
    def __init__(self):
        self.intent_patterns = self._build_patterns()
        self.keywords = self._build_keywords()
        self.block_list = self._build_block_list()
        self.context = {}
    
    def parse(self, text: str, mode: Mode = Mode.LISTENING) -> Intent:
        """
        Parse text into Intent with confidence scoring
        Three-layer approach: keyword → regex → context
        """
        text = text.lower().strip()
        
        # Layer 1: Keyword matching (highest confidence)
        intent = self._match_keywords(text, mode)
        if intent:
            return intent  # Return immediately - keyword matches are reliable
        
        # Layer 2: Regex pattern matching (medium confidence)
        intent = self._match_patterns(text, mode)
        if intent:
            return intent  # Return regex match
        
        # Layer 3: Context-aware inference (lower confidence - fallback)
        intent = self._infer_from_context(text, mode)
        
        return intent
    
    def _match_keywords(self, text: str, mode: Mode) -> Optional[Intent]:
        """Keyword matching layer (Mycroft Adapt pattern)"""
        words = text.split()
        
        # DICTATION mode - check first (highest priority)
        if mode == Mode.DICTATION:
            if any(w in text for w in self.keywords["type"]):
                content = self._extract_dictation(text)
                if content:
                    return Intent(
                        intent_type=IntentType.DICTATION,
                        text=text,
                        action="type",
                        target=content,
                        confidence=0.93,
                        confidence_source="keyword",
                        mode=Mode.DICTATION,
                        risk_level=1
                    )
        
        # COMMAND mode keywords
        if mode in (Mode.COMMAND, Mode.LISTENING):
            # App launching
            if any(w in text for w in self.keywords["open"]):
                app = self._extract_app_name(text)
                if app:
                    return Intent(
                        intent_type=IntentType.COMMAND,
                        text=text,
                        action="open",
                        target=app,
                        confidence=0.95,
                        confidence_source="keyword",
                        mode=Mode.COMMAND,
                        requires_confirmation=False,
                        risk_level=1
                    )
            
            # Dangerous commands - check BEFORE question keywords
            if any(w in text for w in self.keywords["delete"]):
                return Intent(
                    intent_type=IntentType.COMMAND,
                    text=text,
                    action="delete",
                    target=self._extract_target(text),
                    confidence=0.92,
                    confidence_source="keyword",
                    mode=Mode.COMMAND,
                    requires_confirmation=True,  # Safety first!
                    risk_level=7
                )
            
            # Disable/stop commands
            if any(w in text for w in self.keywords["disable"]):
                return Intent(
                    intent_type=IntentType.CONTROL,
                    text=text,
                    action="disable",
                    confidence=0.90,
                    confidence_source="keyword",
                    mode=Mode.DISABLED,
                    requires_confirmation=True,
                    risk_level=5
                )
            
            # QUESTION mode - check for question keywords
            if any(w in text for w in self.keywords["question"]):
                return Intent(
                    intent_type=IntentType.QUESTION,
                    text=text,
                    action="answer",
                    confidence=0.85,
                    confidence_source="keyword",
                    mode=Mode.QUESTION,
                    risk_level=1
                )
        
        return None
    
    def _match_patterns(self, text: str, mode: Mode) -> Optional[Intent]:
        """Regex pattern matching layer (Mycroft Padatious pattern)"""
        
        for pattern_key, pattern_info in self.intent_patterns.items():
            pattern = pattern_info["regex"]
            match = re.search(pattern, text)
            
            if match:
                groups = match.groupdict()
                return Intent(
                    intent_type=pattern_info["type"],
                    text=text,
                    action=pattern_info["action"],
                    target=groups.get("target"),
                    entities=self._extract_entities(match),
                    confidence=0.75,
                    confidence_source="regex",
                    mode=Mode.COMMAND,
                    requires_confirmation=pattern_info.get("confirm", False),
                    risk_level=pattern_info.get("risk", 1)
                )
        
        return None
    
    def _infer_from_context(self, text: str, mode: Mode) -> Intent:
        """Context-aware inference - fallback layer"""
        # Store context
        self.context["last_text"] = text
        self.context["last_time"] = datetime.now()
        
        # Return low-confidence unknown intent
        return Intent(
            intent_type=IntentType.UNKNOWN,
            text=text,
            action="unknown",
            confidence=0.3,
            confidence_source="context",
            mode=mode,
            risk_level=0
        )
    
    def _build_keywords(self) -> Dict[str, list]:
        """Build keyword dictionary (Mycroft Adapt vocabulary)"""
        return {
            "open": ["open", "launch", "start", "run"],
            "delete": ["delete", "remove", "erase", "clear"],
            "disable": ["disable", "stop", "pause", "off"],
            "type": ["type", "write", "say", "dictate"],
            "question": ["what", "how", "why", "tell", "explain"],
            "confirm": ["yes", "ok", "okay", "confirm", "proceed"],
            "cancel": ["no", "cancel", "abort", "stop", "wait"],
        }
    
    def _build_patterns(self) -> Dict[str, dict]:
        """Build regex patterns for structured extraction"""
        return {
            "app_open": {
                "regex": r"open\s+(?P<target>\w+)",
                "type": IntentType.COMMAND,
                "action": "open",
                "risk": 1
            },
            "file_delete": {
                "regex": r"delete\s+(?P<target>[\w\s\.]+)",
                "type": IntentType.COMMAND,
                "action": "delete",
                "confirm": True,
                "risk": 8
            },
            "search": {
                "regex": r"search\s+(?P<target>[\w\s]+)",
                "type": IntentType.QUESTION,
                "action": "search",
                "risk": 1
            },
        }
    
    def _build_block_list(self) -> list:
        """Dangerous operations that require confirmation or blocking"""
        return [
            "delete all",
            "format drive",
            "system shutdown",
            "uninstall",
            "remove user",
        ]
    
    def _extract_app_name(self, text: str) -> Optional[str]:
        """Extract application name from text"""
        apps = ["chrome", "firefox", "notepad", "calculator", "explorer"]
        for app in apps:
            if app in text:
                return app
        return None
    
    def _extract_target(self, text: str) -> Optional[str]:
        """Extract operation target from text"""
        # Simple extraction: last noun/word after action
        words = text.split()
        for i, word in enumerate(words):
            if word in self.keywords["delete"] and i + 1 < len(words):
                return " ".join(words[i+1:])
        return None
    
    def _extract_dictation(self, text: str) -> Optional[str]:
        """Extract text to be dictated"""
        # Remove action keywords
        for keyword in self.keywords["type"]:
            text = text.replace(keyword, "").strip()
        return text if text else None
    
    def _extract_entities(self, match) -> Dict[str, Entity]:
        """Extract entities from regex match"""
        entities = {}
        for name, value in match.groupdict().items():
            if value:
                entities[name] = Entity(
                    name=name,
                    value=value,
                    confidence=0.75,
                    entity_type="regex"
                )
        return entities
