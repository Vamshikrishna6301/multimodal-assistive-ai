"""
Intent Schema - Phase 2
Defines Intent dataclasses and types following industry standards
Inspired by Mycroft, Home Assistant, OpenAssistant patterns
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any


class IntentType(Enum):
    """Intent classification following OpenAssistant safety levels"""
    COMMAND = auto()          # Execute action (Open Chrome, Delete file)
    DICTATION = auto()        # Type/write text
    QUESTION = auto()         # Ask information
    CONTROL = auto()           # Enable/disable features
    UNKNOWN = auto()          # Unrecognized


class Mode(Enum):
    """Assistant operation modes - Finite State Machine states"""
    COMMAND = auto()          # Execute commands
    DICTATION = auto()        # Accept text input
    QUESTION = auto()         # Answer questions
    DISABLED = auto()         # Assistant disabled
    LISTENING = auto()        # Waiting for input


class ConfidenceLevel(Enum):
    """Three-tier confidence hierarchy (Mycroft + OpenAssistant pattern)"""
    HIGH = 0.95               # Execute immediately
    MEDIUM = 0.80             # Request confirmation
    LOW = 0.50                # Request clarification


@dataclass
class Entity:
    """Extracted entity with confidence score"""
    name: str
    value: str
    confidence: float
    entity_type: str = "keyword"  # keyword, regex, context, nl


@dataclass
class Intent:
    """
    Core Intent structure - Multi-layered approach
    Follows Mycroft dual-engine and Home Assistant constraint patterns
    """
    # Identification
    intent_type: IntentType
    text: str
    
    # Core extraction
    action: str                           # What to do
    target: Optional[str] = None          # What to do it on
    
    # Confidence (Mycroft: 0.0-1.0)
    confidence: float = 0.5               # Overall confidence
    confidence_source: str = "unknown"    # keyword | regex | ml | context
    
    # Entities (Home Assistant pattern)
    entities: Dict[str, Entity] = field(default_factory=dict)
    
    # Context (OpenAssistant ROTs)
    context: Dict[str, Any] = field(default_factory=dict)
    mode: Mode = Mode.COMMAND
    
    # Safety
    requires_confirmation: bool = False
    risk_level: int = 0                   # 0-9 scale (OpenAssistant)
    blocked_reason: Optional[str] = None
    
    # Metadata
    timestamp: float = 0.0
    session_id: str = ""
    
    def __post_init__(self):
        """Validate intent consistency"""
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if self.risk_level < 0 or self.risk_level > 9:
            raise ValueError("Risk level must be between 0-9")


@dataclass
class IntentBuffer:
    """
    Multimodal intent buffering (Phase 8 preparation)
    Stores recent intents for conflict resolution
    """
    intents: List[Intent] = field(default_factory=list)
    max_size: int = 10
    timeout_secs: int = 5
    
    def add(self, intent: Intent) -> None:
        """Add intent with FIFO eviction"""
        self.intents.append(intent)
        if len(self.intents) > self.max_size:
            self.intents.pop(0)
    
    def get_recent(self, count: int = 3) -> List[Intent]:
        """Get last N intents"""
        return self.intents[-count:]
    
    def has_conflict(self) -> bool:
        """Detect conflicting intents (preparation for Phase 8)"""
        if len(self.intents) < 2:
            return False
        recent = self.get_recent(2)
        # Simple conflict: contradictory actions
        return recent[0].action != recent[1].action
