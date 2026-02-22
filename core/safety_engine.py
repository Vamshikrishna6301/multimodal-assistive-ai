"""
Safety Engine - Phase 2 (Production Grade)

Implements risk scoring, confirmation requirements,
and execution blocking based on policy rules.
Inspired by OpenAssistant & enterprise moderation pipelines.
"""

import re
from typing import Dict

from .intent_schema import Intent, Mode


class SafetyEngine:
    """
    Risk scoring + confirmation + blocking engine
    """

    def __init__(self):
        self.high_risk_actions = {
            "DELETE": 7,
            "SHUTDOWN": 9,
            "RESTART": 6,
        }

        self.medium_risk_actions = {
            "OPEN_APP": 2,
            "CLOSE_APP": 3,
        }

        self.danger_patterns = [
            r"delete all",
            r"format",
            r"remove system",
            r"shutdown now",
            r"wipe"
        ]

    # =====================================================

    def evaluate(self, intent: Intent, current_mode: Mode) -> Intent:
        """
        Evaluate intent safety.
        Modifies intent in-place.
        """

        # -------------------------------------------------
        # Mode-based blocking
        # -------------------------------------------------
        if current_mode == Mode.DISABLED:
            intent.blocked_reason = "Assistant is disabled"
            intent.risk_level = 9
            return intent

        # -------------------------------------------------
        # Assign base risk
        # -------------------------------------------------
        intent.risk_level = self._assign_risk(intent)

        # -------------------------------------------------
        # Pattern-based escalation
        # -------------------------------------------------
        for pattern in self.danger_patterns:
            if re.search(pattern, intent.text):
                intent.risk_level = max(intent.risk_level, 8)
                intent.context["danger_pattern_detected"] = pattern

        # -------------------------------------------------
        # Confirmation rules
        # -------------------------------------------------
        if intent.risk_level >= 6:
            intent.requires_confirmation = True

        # -------------------------------------------------
        # Hard blocking rule
        # -------------------------------------------------
        if intent.risk_level >= 9:
            intent.blocked_reason = "Operation blocked due to extreme risk"

        return intent

    # =====================================================

    def _assign_risk(self, intent: Intent) -> int:
        """
        Assign baseline risk score.
        """

        if intent.action in self.high_risk_actions:
            return self.high_risk_actions[intent.action]

        if intent.action in self.medium_risk_actions:
            return self.medium_risk_actions[intent.action]

        # Low-risk default
        return 1
