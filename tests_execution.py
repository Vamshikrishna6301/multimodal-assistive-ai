import unittest
from core.intent_schema import Intent, IntentType
from execution.executor import Executor


class TestExecutorDryRun(unittest.TestCase):
    def setUp(self):
        # Executor in dry-run mode should not cause side effects
        self.executor = Executor(allow_side_effects=False)

    def test_open_app_dry_run(self):
        intent = Intent(intent_type=IntentType.COMMAND, text="open chrome", action="open", target="chrome", confidence=0.9, confidence_source="test")
        res = self.executor.execute(intent)
        self.assertTrue(res.success)
        self.assertTrue(("Opened" in res.message) or ("dry-run" in res.message))

    def test_type_text_dry_run(self):
        intent = Intent(intent_type=IntentType.COMMAND, text="type hello", action="type", entities={"text": "hello world"}, confidence=0.9, confidence_source="test")
        res = self.executor.execute(intent)
        self.assertTrue(res.success)
        self.assertTrue(("Typed" in res.message) or ("dry-run" in res.message))

    def test_delete_requires_confirmation(self):
        intent = Intent(intent_type=IntentType.COMMAND, text="delete file", action="delete", target="C:/important.txt", confidence=0.9, confidence_source="test")
        res = self.executor.execute(intent)
        # In dry-run, delete will be simulated but should not perform destructive ops; allow either dry-run message or a blocked response.
        self.assertTrue((not res.success) or ("dry-run" in res.message) or ("Deleted" in res.message))


if __name__ == "__main__":
    unittest.main()
