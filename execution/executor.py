"""
Executor that turns validated `Intent` objects into safe actions.
- Uses the smaller helper modules in `execution/`.
- Respects `dry_run` by default; requires explicit `allow_side_effects=True` to perform real actions.
"""
from typing import Tuple
from core.intent_schema import Intent, Entity as IntentEntity
from core.safety_rules import SafetyRules
from execution import app_control, keyboard_mouse, file_ops


class ExecutionResult:
    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message


class Executor:
    def __init__(self, allow_side_effects: bool = False):
        self.allow_side_effects = allow_side_effects

    def execute(self, intent: Intent) -> ExecutionResult:
        # Basic guard: only execute if intent validated by safety rules
        safety = SafetyRules()
        allowed, reason, requires_confirmation = safety.validate(intent)
        if not allowed:
            return ExecutionResult(False, f"Blocked by safety: {reason}")
        if requires_confirmation and not self.allow_side_effects:
            return ExecutionResult(False, "Requires explicit confirmation before execution")

        action = intent.action.lower() if intent.action else ""
        # Prefer explicit Intent.target, fallback to entities map
        target = intent.target or (intent.entities.get("target") if intent.entities else None)

        # Helper to extract value when entities may be either raw strings or IntentEntity
        def _extract(val):
            if val is None:
                return None
            if isinstance(val, IntentEntity):
                return val.value
            return val

        try:
            if action in ("open", "launch"):
                target_val = _extract(target)
                if not target_val:
                    return ExecutionResult(False, "No target specified for open action")
                if self.allow_side_effects:
                    err = app_control.open_app(target_val)
                    if err:
                        return ExecutionResult(False, str(err))
                    return ExecutionResult(True, f"Opened {target_val}")
                else:
                    return ExecutionResult(True, f"dry-run: would open {target_val}")

            if action in ("close", "quit", "kill"):
                target_val = _extract(target)
                if not target_val:
                    return ExecutionResult(False, "No target specified for close action")
                if self.allow_side_effects:
                    err = app_control.close_app(target_val)
                    if err:
                        return ExecutionResult(False, str(err))
                    return ExecutionResult(True, f"Closed {target_val}")
                else:
                    return ExecutionResult(True, f"dry-run: would close {target_val}")

            if action in ("type", "write"):
                text = intent.entities.get("text") if intent.entities else None
                text_val = _extract(text)
                if not text_val:
                    return ExecutionResult(False, "No text specified to type")
                if self.allow_side_effects:
                    err = keyboard_mouse.type_text(text_val, dry_run=not self.allow_side_effects)
                    if err:
                        return ExecutionResult(False, str(err))
                    return ExecutionResult(True, "Typed text")
                else:
                    return ExecutionResult(True, f"dry-run: would type '{text_val}'")

            if action in ("delete",):
                path = intent.entities.get("path") if intent.entities else None
                path_val = _extract(path)
                if not path_val:
                    return ExecutionResult(False, "No path specified for delete")
                # destructive: require explicit allow_side_effects
                if self.allow_side_effects:
                    err = file_ops.delete_file(path_val, dry_run=not self.allow_side_effects)
                    if err:
                        return ExecutionResult(False, str(err))
                    return ExecutionResult(True, f"Deleted {path_val}")
                else:
                    return ExecutionResult(True, f"dry-run: would delete {path_val}")

            return ExecutionResult(False, f"Unknown action '{action}'")
        except Exception as e:
            return ExecutionResult(False, str(e))
