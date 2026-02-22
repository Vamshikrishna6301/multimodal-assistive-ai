from core.intent_parser import IntentParser
from core.context_memory import ContextMemory
from core.mode_manager import ModeManager
from core.safety_engine import SafetyEngine

parser = IntentParser()
memory = ContextMemory()
mode_manager = ModeManager()
safety = SafetyEngine()

commands = [
    "open chrome",
    "delete report.pdf",
    "delete all files in system",
    "shutdown now"
]

for cmd in commands:
    intent = parser.parse(cmd, current_mode=mode_manager.get_mode())
    intent = memory.enrich(intent)
    memory.update(intent)
    intent = safety.evaluate(intent, mode_manager.get_mode())

    print("\nInput:", cmd)
    print("Action:", intent.action)
    print("Risk Level:", intent.risk_level)
    print("Requires Confirmation:", intent.requires_confirmation)
    print("Blocked:", intent.blocked_reason)
    print("Context:", intent.context)
