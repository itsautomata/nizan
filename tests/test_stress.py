"""tests for the stress-test feature."""

import unittest
from unittest.mock import patch, call
from core.sigil import Sigil


def fake_call(system_prompt, transcript):
    """mock LLM that returns the mode it was called with."""
    if "BREAK" in system_prompt:
        return "stress-challenge-response"
    if "stress test" in system_prompt.lower():
        return "stress-judge-response"
    if "Moderator" in system_prompt:
        return "framing-response"
    if "Advocate" in system_prompt:
        return "advocate-response"
    if "Critic" in system_prompt:
        return "critic-response"
    if "Judge" in system_prompt:
        return "judge-response"
    return "unknown"


def _patch_all_agents():
    """patch call where each agent module imported it."""
    return [
        patch("agents.moderator.call", side_effect=fake_call),
        patch("agents.advocate.call", side_effect=fake_call),
        patch("agents.critic.call", side_effect=fake_call),
        patch("agents.judge.call", side_effect=fake_call),
    ]


class TestStressTest(unittest.TestCase):

    def test_stress_prompts_exist(self):
        """all three agents have a stress prompt key."""
        from agents.advocate import PROMPTS as adv
        from agents.critic import PROMPTS as crt
        from agents.judge import PROMPTS as jdg

        self.assertIn("stress", adv)
        self.assertIn("stress", crt)
        self.assertIn("stress", jdg)

    def test_stress_prompt_is_adversarial(self):
        """stress prompts instruct the agent to break the ruling."""
        from agents.advocate import PROMPTS as adv
        from agents.critic import PROMPTS as crt

        self.assertIn("BREAK", adv["stress"])
        self.assertIn("BREAK", crt["stress"])

    def _run_with_mocks(self, topic="test topic", mode="normal", rounds=1, stress_test=False):
        """helper: run debate with all LLM calls mocked, return list of started mocks."""
        import debate

        patches = _patch_all_agents()
        mocks = [p.start() for p in patches]
        try:
            with patch("builtins.input", return_value=""):
                debate.run(topic, mode=mode, rounds=rounds, interactive=False, stress_test=stress_test)
        finally:
            for p in patches:
                p.stop()
        return mocks

    def test_stress_off_skips_extra_rounds(self):
        """with stress_test=False, no stress round happens."""
        mocks = self._run_with_mocks(stress_test=False)
        total = sum(m.call_count for m in mocks)
        # moderator, advocate, critic, judge = 4
        self.assertEqual(total, 4)

    def test_stress_on_adds_three_calls(self):
        """with stress_test=True, three extra LLM calls happen."""
        mocks = self._run_with_mocks(stress_test=True)
        total = sum(m.call_count for m in mocks)
        # 4 base + 3 stress = 7
        self.assertEqual(total, 7)

    def test_stress_entries_in_sigil(self):
        """stress-test responses are recorded in the sigil."""
        mocks = self._run_with_mocks(stress_test=True)
        total = sum(m.call_count for m in mocks)
        self.assertEqual(total, 7)

    def test_stress_works_with_decision_mode(self):
        """stress-test works in decision mode too."""
        mocks = self._run_with_mocks(topic="A vs B", mode="decision", stress_test=True)
        total = sum(m.call_count for m in mocks)
        self.assertEqual(total, 7)


if __name__ == "__main__":
    unittest.main()
