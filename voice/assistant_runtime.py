# voice/assistant_runtime.py

import threading


class AssistantRuntime:
    """
    Shared runtime state for production voice assistant.
    Handles speaking state, confirmation lifecycle,
    interrupt control, and shutdown.
    """

    def __init__(self):
        self.running = True

        # Speaking control
        self._is_speaking = False

        # Confirmation lifecycle
        self.awaiting_confirmation = False
        self.pending_intent = None

        # Interrupt state
        self.interrupted = False

        # Thread safety
        self._lock = threading.Lock()

    # -----------------------------------------------------

    def set_speaking(self, value: bool):
        with self._lock:
            self._is_speaking = value

    def is_speaking(self) -> bool:
        with self._lock:
            return self._is_speaking

    # -----------------------------------------------------

    def set_confirmation(self, intent):
        with self._lock:
            self.awaiting_confirmation = True
            self.pending_intent = intent

    def clear_confirmation(self):
        with self._lock:
            self.awaiting_confirmation = False
            self.pending_intent = None

    # -----------------------------------------------------

    def request_interrupt(self):
        with self._lock:
            self.interrupted = True

    def clear_interrupt(self):
        with self._lock:
            self.interrupted = False

    # -----------------------------------------------------

    def stop(self):
        with self._lock:
            self.running = False