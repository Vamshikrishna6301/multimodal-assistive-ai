import json
import os
import time
from threading import Lock
from typing import Dict

LOG_FILE = "execution_logs.json"


class ExecutionLogger:
    """
    Production-grade structured execution logger.
    Thread-safe JSON line logger.
    """

    def __init__(self, log_file: str = LOG_FILE):
        self.log_file = log_file
        self._lock = Lock()

        # Ensure file exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                pass

    # -----------------------------------------------------

    def log(self, decision: Dict, response) -> None:

        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": decision.get("action"),
            "target": decision.get("target"),
            "risk_level": decision.get("risk_level"),
            "requires_confirmation": decision.get("requires_confirmation"),
            "status": decision.get("status"),
            "success": response.success,
            "error_code": response.error_code,
            "category": response.category,
            "spoken_message": response.spoken_message
        }

        with self._lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")