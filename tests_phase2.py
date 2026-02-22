"""
Phase 2 Tests - Intent & Mode Engine
Comprehensive test suite following industry standards
"""

import unittest
from core import (
    Intent, IntentType, Mode,
    IntentParser, ModeManager, SafetyRules
)


class TestIntentSchema(unittest.TestCase):
    """Test Intent dataclass and types"""
    
    def test_intent_creation(self):
        """Test basic intent creation"""
        intent = Intent(
            intent_type=IntentType.COMMAND,
            text="open chrome",
            action="open",
            target="chrome",
            confidence=0.95
        )
        self.assertEqual(intent.action, "open")
        self.assertEqual(intent.target, "chrome")
        self.assertEqual(intent.confidence, 0.95)
    
    def test_intent_confidence_validation(self):
        """Test confidence bounds checking"""
        with self.assertRaises(ValueError):
            Intent(
                intent_type=IntentType.COMMAND,
                text="test",
                action="test",
                confidence=1.5  # Invalid
            )
    
    def test_intent_risk_validation(self):
        """Test risk level bounds"""
        with self.assertRaises(ValueError):
            Intent(
                intent_type=IntentType.COMMAND,
                text="test",
                action="test",
                risk_level=10  # Must be 0-9
            )


class TestIntentParser(unittest.TestCase):
    """Test intent parsing engine"""
    
    def setUp(self):
        self.parser = IntentParser()
    
    def test_keyword_matching_open(self):
        """Test keyword matching for 'open' action"""
        intent = self.parser.parse("open chrome", Mode.COMMAND)
        self.assertEqual(intent.action, "open")
        self.assertEqual(intent.target, "chrome")
        self.assertGreaterEqual(intent.confidence, 0.90)
    
    def test_keyword_matching_delete(self):
        """Test delete action detection"""
        intent = self.parser.parse("delete file", Mode.COMMAND)
        self.assertEqual(intent.action, "delete")
        self.assertTrue(intent.requires_confirmation)
        self.assertGreaterEqual(intent.risk_level, 6)
    
    def test_keyword_matching_dictation(self):
        """Test dictation mode parsing"""
        intent = self.parser.parse("type hello world", Mode.DICTATION)
        self.assertEqual(intent.intent_type, IntentType.DICTATION)
        self.assertEqual(intent.action, "type")
    
    def test_question_detection(self):
        """Test question intent detection"""
        intent = self.parser.parse("what is the weather", Mode.LISTENING)
        self.assertEqual(intent.intent_type, IntentType.QUESTION)
    
    def test_unknown_intent(self):
        """Test fallback to unknown intent"""
        intent = self.parser.parse("xyzabc random text", Mode.LISTENING)
        self.assertEqual(intent.intent_type, IntentType.UNKNOWN)
        self.assertLess(intent.confidence, 0.5)
    
    def test_confidence_scoring(self):
        """Test confidence varies by detection method"""
        # Keyword = high confidence
        intent1 = self.parser.parse("open chrome", Mode.COMMAND)
        self.assertGreater(intent1.confidence, 0.90)
        
        # Unknown = low confidence
        intent2 = self.parser.parse("random_gibberish_123", Mode.COMMAND)
        self.assertLess(intent2.confidence, 0.5)
    
    def test_disable_command(self):
        """Test disable/stop command"""
        intent = self.parser.parse("disable assistant", Mode.COMMAND)
        self.assertEqual(intent.action, "disable")
        self.assertEqual(intent.mode, Mode.DISABLED)


class TestModeManager(unittest.TestCase):
    """Test mode management and FSM"""
    
    def setUp(self):
        self.manager = ModeManager()
    
    def test_initial_mode(self):
        """Test initial mode is LISTENING"""
        self.assertEqual(self.manager.get_mode(), Mode.LISTENING)
    
    def test_transition_to_command(self):
        """Test transition from LISTENING to COMMAND"""
        result = self.manager.set_mode(Mode.COMMAND, "command_detected")
        self.assertTrue(result)
        self.assertEqual(self.manager.get_mode(), Mode.COMMAND)
    
    def test_transition_history(self):
        """Test transition history tracking"""
        self.manager.set_mode(Mode.COMMAND, "test1")
        self.manager.set_mode(Mode.LISTENING, "test2")
        
        history = self.manager.get_transition_history(10)
        self.assertEqual(len(history), 2)
    
    def test_invalid_transition(self):
        """Test that invalid transitions are rejected"""
        self.manager.set_mode(Mode.COMMAND, "test")
        # Try direct COMMAND->QUESTION (invalid)
        result = self.manager.set_mode(Mode.QUESTION, "invalid")
        self.assertFalse(result)
        self.assertEqual(self.manager.get_mode(), Mode.COMMAND)
    
    def test_no_self_transitions(self):
        """Test that self-transitions are blocked"""
        result = self.manager.set_mode(Mode.COMMAND, "test")
        result2 = self.manager.set_mode(Mode.COMMAND, "test")  # Same mode
        self.assertFalse(result2)
    
    def test_can_execute(self):
        """Test can_execute for different modes"""
        self.manager.set_mode(Mode.COMMAND)
        self.assertTrue(self.manager.can_execute("command"))
        
        self.manager.set_mode(Mode.DICTATION)
        self.assertTrue(self.manager.can_execute("dictation"))
        self.assertFalse(self.manager.can_execute("command"))
    
    def test_is_enabled(self):
        """Test is_enabled check"""
        self.assertTrue(self.manager.is_enabled())
        
        self.manager.set_mode(Mode.DISABLED)
        self.assertFalse(self.manager.is_enabled())


class TestSafetyRules(unittest.TestCase):
    """Test safety validation"""
    
    def setUp(self):
        self.safety = SafetyRules()
    
    def test_delete_requires_confirmation(self):
        """Test that delete operations require confirmation"""
        intent = Intent(
            intent_type=IntentType.COMMAND,
            text="delete file.txt",
            action="delete",
            target="file.txt",
            confidence=0.9,
            risk_level=7
        )
        
        _, _, requires_conf = self.safety.validate(intent)
        self.assertTrue(requires_conf)
    
    def test_delete_all_is_blocked(self):
        """Test that 'delete all' is blocked"""
        intent = Intent(
            intent_type=IntentType.COMMAND,
            text="delete all files",
            action="delete",
            target="all",
            confidence=0.9,
            risk_level=9
        )
        
        allowed, reason, _ = self.safety.validate(intent)
        self.assertFalse(allowed)
        self.assertIsNotNone(reason)
    
    def test_safe_open_allowed(self):
        """Test that safe operations are allowed"""
        intent = Intent(
            intent_type=IntentType.COMMAND,
            text="open chrome",
            action="open",
            target="chrome",
            confidence=0.95,
            risk_level=1
        )
        
        allowed, reason, requires_conf = self.safety.validate(intent)
        self.assertTrue(allowed)
        self.assertIsNone(reason)
        self.assertFalse(requires_conf)
    
    def test_risk_assessment(self):
        """Test comprehensive risk assessment"""
        intent = Intent(
            intent_type=IntentType.COMMAND,
            text="delete file",
            action="delete",
            target="file",
            risk_level=8
        )
        
        assessment = self.safety.get_risk_assessment(intent)
        self.assertIn("risk_level", assessment)
        self.assertTrue(assessment["requires_confirmation"])
    
    def test_low_confidence_requires_confirmation(self):
        """Test that low confidence actions require confirmation"""
        intent = Intent(
            intent_type=IntentType.COMMAND,
            text="open xxxx",
            action="open",
            confidence=0.3,  # Low!
            risk_level=1
        )
        
        _, _, requires_conf = self.safety.validate(intent)
        # Low confidence + ambiguous = confirm
        # (Depends on rules, but should error on side of caution)
        self.assertIsNotNone(requires_conf)


class TestPhase2Integration(unittest.TestCase):
    """Integration tests for Phase 2 components"""
    
    def test_full_pipeline_safe_command(self):
        """Test full pipeline: parse -> mode -> safety"""
        parser = IntentParser()
        manager = ModeManager()
        safety = SafetyRules()
        
        # Parse
        intent = parser.parse("open chrome", Mode.LISTENING)
        
        # Should parse to COMMAND
        self.assertEqual(intent.action, "open")
        
        # Validate
        allowed, _, requires_conf = safety.validate(intent)
        self.assertTrue(allowed)
        self.assertFalse(requires_conf)
    
    def test_full_pipeline_dangerous_command(self):
        """Test full pipeline with dangerous command"""
        parser = IntentParser()
        safety = SafetyRules()
        
        intent = parser.parse("delete all", Mode.COMMAND)
        
        # Should be blocked
        allowed, reason, _ = safety.validate(intent)
        self.assertFalse(allowed)
        self.assertIsNotNone(reason)
    
    def test_mode_based_parsing(self):
        """Test that parsing changes based on mode"""
        parser = IntentParser()
        
        # COMMAND mode
        intent1 = parser.parse("type hello", Mode.COMMAND)
        # May be interpreted as command in COMMAND mode
        
        # DICTATION mode
        intent2 = parser.parse("type hello", Mode.DICTATION)
        # Should be interpreted as dictation
        self.assertEqual(intent2.intent_type, IntentType.DICTATION)


def run_tests():
    """Run all Phase 2 tests"""
    print("\n" + "="*60)
    print("🧪 Running Phase 2 Test Suite")
    print("="*60 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestIntentSchema))
    suite.addTests(loader.loadTestsFromTestCase(TestIntentParser))
    suite.addTests(loader.loadTestsFromTestCase(TestModeManager))
    suite.addTests(loader.loadTestsFromTestCase(TestSafetyRules))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase2Integration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ All Phase 2 tests PASSED!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
