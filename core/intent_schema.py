"""
Intent Schema - Phase 2
Defines Intent dataclasses and types following industry standards
Inspired by Mycroft, Home Assistant, OpenAssistant patterns
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any


class IntentType(Enum):
    COMMAND = auto()
    DICTATION = auto()
    QUESTION = auto()
    CONTROL = auto()
    UNKNOWN = auto()


class Mode(Enum):
    COMMAND = auto()
    DICTATION = auto()
    QUESTION = auto()
    DISABLED = auto()
    LISTENING = auto()


class ConfidenceLevel(Enum):
    HIGH = 0.95
    MEDIUM = 0.80
    LOW = 0.50


@dataclass
class Entity:
    name: str
    value: str
    confidence: float
    entity_type: str = "keyword"


@dataclass
class Intent:
    intent_type: IntentType
    text: str

    action: str
    target: Optional[str] = None

    confidence: float = 0.5
    confidence_source: str = "unknown"

    entities: Dict[str, Entity] = field(default_factory=dict)

    context: Dict[str, Any] = field(default_factory=dict)
    mode: Mode = Mode.COMMAND

    requires_confirmation: bool = False
    risk_level: int = 0
    blocked_reason: Optional[str] = None

    timestamp: float = 0.0
    session_id: str = ""

    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if not 0 <= self.risk_level <= 9:
            raise ValueError("Risk level must be between 0-9")


@dataclass
class IntentBuffer:
    intents: List[Intent] = field(default_factory=list)
    max_size: int = 10
    timeout_secs: int = 5

    def add(self, intent: Intent) -> None:
        self.intents.append(intent)
        if len(self.intents) > self.max_size:
            self.intents.pop(0)

    def get_recent(self, count: int = 3) -> List[Intent]:
        return self.intents[-count:]

    def has_conflict(self) -> bool:
        if len(self.intents) < 2:
            return False
        recent = self.get_recent(2)
        return recent[0].action != recent[1].action
