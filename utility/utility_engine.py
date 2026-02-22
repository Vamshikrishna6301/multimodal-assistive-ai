import math
import re
from core.response_model import UnifiedResponse


class UtilityEngine:
    """
    Production-Level Utility Engine

    Supports:
    - Advanced math expressions
    - Safe evaluation (restricted environment)
    """

    def __init__(self):
        # Whitelisted math functions and constants
        self.allowed_names = {
            name: getattr(math, name)
            for name in dir(math)
            if not name.startswith("__")
        }

        # Add common aliases
        self.allowed_names.update({
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "round": round
        })

    def handle(self, decision: dict) -> UnifiedResponse:

        action = decision.get("action")
        target = decision.get("target")

        if action == "CALCULATE":
            return self.calculate(target)

        elif action == "GET_TIME":
            return self.get_time()

        return UnifiedResponse.error_response(
            category="utility",
            spoken_message="Unsupported utility request.",
            error_code="UTILITY_UNSUPPORTED"
        )

    # -----------------------------
    # Advanced Calculator
    # -----------------------------

    def calculate(self, expression: str) -> UnifiedResponse:

        if not expression:
            return UnifiedResponse.error_response(
                category="utility",
                spoken_message="No expression provided.",
                error_code="NO_EXPRESSION"
            )

        try:
            # Replace caret with power
            expression = expression.replace("^", "**")

            # Security check: only allow safe characters
            if not re.match(r'^[0-9\.\+\-\*\/\%\(\)\s,a-zA-Z_]*$', expression):
                return UnifiedResponse.error_response(
                    category="utility",
                    spoken_message="Invalid characters in expression.",
                    error_code="INVALID_EXPRESSION"
                )

            result = eval(
                expression,
                {"__builtins__": None},
                self.allowed_names
            )

            return UnifiedResponse.success_response(
                category="utility",
                spoken_message=f"The result is {result}."
            )

        except Exception:
            return UnifiedResponse.error_response(
                category="utility",
                spoken_message="I could not calculate that expression.",
                error_code="CALCULATION_ERROR"
            )

    # -----------------------------
    # Get Current Time
    # -----------------------------

    def get_time(self):
        from datetime import datetime

        now = datetime.now().strftime("%I:%M %p")

        return UnifiedResponse.success_response(
            category="utility",
            spoken_message=f"The current time is {now}."
        )