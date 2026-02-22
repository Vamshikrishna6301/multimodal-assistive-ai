"""
Mode Manager - Phase 2
Finite state machine for assistant modes
Implements state transitions following Home Assistant pattern
"""

from enum import Enum
from typing import Optional, Callable, Dict, List
from .intent_schema import Mode


class ModeTransition:
    """Represents valid mode transitions"""
    def __init__(self, from_mode: Mode, to_mode: Mode, trigger: str):
        self.from_mode = from_mode
        self.to_mode = to_mode
        self.trigger = trigger


class ModeManager:
    """
    Finite State Machine for assistant modes
    Home Assistant pattern: State management with transitions
    """
    
    def __init__(self):
        self.current_mode = Mode.LISTENING
        self.previous_mode = Mode.LISTENING
        self.transition_history: List[tuple] = []
        self.callbacks: Dict[Mode, List[Callable]] = {mode: [] for mode in Mode}
        self.max_history = 100
        
        # Define valid transitions (FSM state graph)
        self.transitions = self._define_transitions()
    
    def set_mode(self, new_mode: Mode, reason: str = "unknown") -> bool:
        """
        Transition to new mode with validation
        Returns True if transition succeeded, False otherwise
        """
        # Validate transition
        if not self._can_transition(self.current_mode, new_mode):
            print(f"❌ Cannot transition from {self.current_mode} to {new_mode}")
            return False
        
        # Record history
        self.previous_mode = self.current_mode
        self.current_mode = new_mode
        self.transition_history.append((self.previous_mode, new_mode, reason))
        
        # Keep history bounded
        if len(self.transition_history) > self.max_history:
            self.transition_history.pop(0)
        
        # Execute callbacks
        self._execute_callbacks(new_mode)
        
        print(f"🔄 Mode: {self.previous_mode.name} → {new_mode.name} ({reason})")
        return True
    
    def get_mode(self) -> Mode:
        """Get current mode"""
        return self.current_mode
    
    def get_previous_mode(self) -> Mode:
        """Get previous mode for context"""
        return self.previous_mode
    
    def on_mode_change(self, mode: Mode, callback: Callable) -> None:
        """Register callback for mode changes"""
        if mode in self.callbacks:
            self.callbacks[mode].append(callback)
    
    def is_enabled(self) -> bool:
        """Check if assistant is enabled"""
        return self.current_mode != Mode.DISABLED
    
    def can_execute(self, intent_type: str) -> bool:
        """Check if current mode allows executing intent type"""
        mode_permissions = {
            Mode.COMMAND: ["command", "control"],
            Mode.DICTATION: ["dictation"],
            Mode.QUESTION: ["question"],
            Mode.DISABLED: [],
            Mode.LISTENING: ["question"],  # Listening can only answer Qs
        }
        return intent_type in mode_permissions.get(self.current_mode, [])
    
    def get_mode_description(self) -> Dict:
        """Get description of current mode"""
        descriptions = {
            Mode.COMMAND: {
                "name": "COMMAND",
                "active": True,
                "allows": ["open apps", "delete files", "control system"],
                "requires_confirmation": True
            },
            Mode.DICTATION: {
                "name": "DICTATION",
                "active": True,
                "allows": ["type text", "write"],
                "requires_confirmation": False
            },
            Mode.QUESTION: {
                "name": "QUESTION",
                "active": True,
                "allows": ["answer questions", "provide info"],
                "requires_confirmation": False
            },
            Mode.DISABLED: {
                "name": "DISABLED",
                "active": False,
                "allows": [],
                "requires_confirmation": False
            },
            Mode.LISTENING: {
                "name": "LISTENING",
                "active": True,
                "allows": ["await input"],
                "requires_confirmation": False
            },
        }
        return descriptions.get(self.current_mode, {})
    
    def get_transition_history(self, limit: int = 10) -> List[tuple]:
        """Get recent transition history"""
        return self.transition_history[-limit:]
    
    # ========================= Private Methods =========================
    
    def _define_transitions(self) -> List[ModeTransition]:
        """
        Define valid FSM transitions
        Home Assistant follows strict state graphs
        """
        return [
            # From LISTENING
            ModeTransition(Mode.LISTENING, Mode.COMMAND, "command_detected"),
            ModeTransition(Mode.LISTENING, Mode.QUESTION, "question_detected"),
            ModeTransition(Mode.LISTENING, Mode.DICTATION, "dictation_mode_enabled"),
            ModeTransition(Mode.LISTENING, Mode.DISABLED, "disable_command"),
            
            # From COMMAND
            ModeTransition(Mode.COMMAND, Mode.LISTENING, "command_completed"),
            ModeTransition(Mode.COMMAND, Mode.DICTATION, "switch_to_dictation"),
            ModeTransition(Mode.COMMAND, Mode.DISABLED, "disable_command"),
            
            # From DICTATION
            ModeTransition(Mode.DICTATION, Mode.LISTENING, "exit_dictation"),
            ModeTransition(Mode.DICTATION, Mode.COMMAND, "switch_to_command"),
            ModeTransition(Mode.DICTATION, Mode.DISABLED, "disable_command"),
            
            # From QUESTION
            ModeTransition(Mode.QUESTION, Mode.LISTENING, "question_answered"),
            ModeTransition(Mode.QUESTION, Mode.COMMAND, "switch_to_command"),
            ModeTransition(Mode.QUESTION, Mode.DISABLED, "disable_command"),
            
            # From DISABLED
            ModeTransition(Mode.DISABLED, Mode.LISTENING, "enable_assistant"),
        ]
    
    def _can_transition(self, from_mode: Mode, to_mode: Mode) -> bool:
        """Check if transition is valid"""
        if from_mode == to_mode:
            return False  # No self-transitions
        
        for transition in self.transitions:
            if transition.from_mode == from_mode and transition.to_mode == to_mode:
                return True
        return False
    
    def _execute_callbacks(self, mode: Mode) -> None:
        """Execute registered callbacks for mode change"""
        for callback in self.callbacks.get(mode, []):
            try:
                callback(mode)
            except Exception as e:
                print(f"⚠️ Error in mode callback: {e}")
