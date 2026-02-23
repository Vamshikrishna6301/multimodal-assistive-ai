from enum import Enum, auto
import threading


class AssistantState(Enum):
    IDLE = auto()
    LISTENING = auto()
    EXECUTING = auto()
    SPEAKING = auto()
    SHUTTING_DOWN = auto()


class AssistantRuntime:
    """
    Production Runtime Controller

    - Execution state machine
    - Speaking state control
    - Confirmation handled independently
    """

    def __init__(self):
        self._lock = threading.Lock()

        self.running = True
        self.state = AssistantState.LISTENING

        # 🔒 Confirmation handled independently
        self.awaiting_confirmation = False
        self.pending_intent = None

        self.interrupted = False

    # =====================================================
    # STATE MANAGEMENT
    # =====================================================

    def set_state(self, new_state: AssistantState):
        with self._lock:
            self.state = new_state

    def get_state(self) -> AssistantState:
        with self._lock:
            return self.state

    # =====================================================
    # CONFIRMATION (Independent)
    # =====================================================

    def set_confirmation(self, intent):
        with self._lock:
            self.pending_intent = intent
            self.awaiting_confirmation = True

    def clear_confirmation(self):
        with self._lock:
            self.pending_intent = None
            self.awaiting_confirmation = False

    def is_awaiting_confirmation(self) -> bool:
        with self._lock:
            return self.awaiting_confirmation

    # =====================================================
    # SPEAKING CONTROL
    # =====================================================

    def start_speaking(self):
        with self._lock:
            self.state = AssistantState.SPEAKING

    def stop_speaking(self):
        with self._lock:
            self.state = AssistantState.LISTENING

    def is_speaking(self) -> bool:
        with self._lock:
            return self.state == AssistantState.SPEAKING

    # =====================================================
    # EXECUTION CONTROL
    # =====================================================

    def start_execution(self):
        with self._lock:
            self.state = AssistantState.EXECUTING

    def finish_execution(self):
        with self._lock:
            self.state = AssistantState.LISTENING

    # =====================================================
    # INTERRUPT
    # =====================================================

    def request_interrupt(self):
        with self._lock:
            self.interrupted = True

    def clear_interrupt(self):
        with self._lock:
            self.interrupted = False

    # =====================================================
    # SHUTDOWN
    # =====================================================

    def stop(self):
        with self._lock:
            self.state = AssistantState.SHUTTING_DOWN
            self.running = False