"""
Production-Grade Structured Logging System
Provides centralized logging with multiple outputs and severity levels
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from enum import Enum


class LogLevel(Enum):
    """Log severity levels"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class StructuredLogger:
    """
    Industry-standard structured logger with:
    - JSON output for log aggregation
    - Multiple handlers (file, console)
    - Contextual information
    - Performance tracking
    """

    def __init__(self, name: str, level: LogLevel = LogLevel.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level.value)
        
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # JSON file handler for structured logs
        json_handler = logging.FileHandler(log_dir / "app.json.log")
        json_handler.setFormatter(logging.Formatter(
            '%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        
        # Console handler for CLI output
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s - %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # Error file handler
        error_handler = logging.FileHandler(log_dir / "app.error.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(json_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)
        
        self.context = {}

    def set_context(self, **kwargs):
        """Set contextual information for logs"""
        self.context.update(kwargs)

    def _format_log(self, level: str, message: str, **kwargs):
        """Format log as JSON for aggregation"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "context": self.context,
            **kwargs
        }
        return json.dumps(log_data)

    def debug(self, message: str, **kwargs):
        """Debug level log"""
        self.logger.debug(self._format_log("DEBUG", message, **kwargs))

    def info(self, message: str, **kwargs):
        """Info level log"""
        self.logger.info(self._format_log("INFO", message, **kwargs))

    def warning(self, message: str, **kwargs):
        """Warning level log"""
        self.logger.warning(self._format_log("WARNING", message, **kwargs))

    def error(self, message: str, exception: Exception = None, **kwargs):
        """Error level log"""
        if exception:
            kwargs['exception'] = str(exception)
            kwargs['exception_type'] = type(exception).__name__
        self.logger.error(self._format_log("ERROR", message, **kwargs))

    def critical(self, message: str, exception: Exception = None, **kwargs):
        """Critical level log"""
        if exception:
            kwargs['exception'] = str(exception)
        self.logger.critical(self._format_log("CRITICAL", message, **kwargs))

    def audit(self, action: str, user: str = "system", **details):
        """Audit log for compliance and tracking"""
        audit_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "AUDIT",
            "action": action,
            "user": user,
            "details": details
        }
        self.logger.info(json.dumps(audit_data))


# Global logger instance
_logger = None


def get_logger(name: str) -> StructuredLogger:
    """Get or create structured logger"""
    global _logger
    if _logger is None:
        _logger = StructuredLogger(name)
    return _logger


def init_logger(log_level: str = "INFO"):
    """Initialize global logger"""
    global _logger
    level = LogLevel[log_level.upper()]
    _logger = StructuredLogger("MMAIAssistant", level)
    return _logger
