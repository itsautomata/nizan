"""tests for the headless CLI (argparse) surface."""

import unittest
import argparse


def build_parser():
    """replicate the parser from debate.py's __main__ block."""
    parser = argparse.ArgumentParser()
    parser.add_argument("topic")
    parser.add_argument("--mode", choices=["normal", "decision"], default="normal")
    parser.add_argument("--rounds", type=int, default=2, choices=range(1, 5))
    parser.add_argument("--context", metavar="FILE")
    parser.add_argument("--priorities")
    parser.add_argument("--stress-test", action="store_true")
    return parser


class TestHeadlessCLI(unittest.TestCase):

    def setUp(self):
        self.parser = build_parser()

    def test_topic_only(self):
        args = self.parser.parse_args(["should AI be open source?"])
        self.assertEqual(args.topic, "should AI be open source?")
        self.assertEqual(args.mode, "normal")
        self.assertEqual(args.rounds, 2)
        self.assertIsNone(args.context)
        self.assertIsNone(args.priorities)
        self.assertFalse(args.stress_test)

    def test_full_flags(self):
        args = self.parser.parse_args([
            "--mode", "decision",
            "--rounds", "3",
            "--context", "doc.md",
            "--priorities", "cost,risk tolerance",
            "--stress-test",
            "rust vs go",
        ])
        self.assertEqual(args.topic, "rust vs go")
        self.assertEqual(args.mode, "decision")
        self.assertEqual(args.rounds, 3)
        self.assertEqual(args.context, "doc.md")
        self.assertEqual(args.priorities, "cost,risk tolerance")
        self.assertTrue(args.stress_test)

    def test_priorities_parsing(self):
        """comma-separated priorities split correctly."""
        args = self.parser.parse_args(["--priorities", "cost,optionality,time pressure", "topic"])
        priorities = [p.strip() for p in args.priorities.split(",")]
        self.assertEqual(priorities, ["cost", "optionality", "time pressure"])

    def test_invalid_mode_rejected(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--mode", "reopen", "topic"])

    def test_invalid_rounds_rejected(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--rounds", "5", "topic"])

    def test_zero_rounds_rejected(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--rounds", "0", "topic"])

    def test_missing_topic_rejected(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_stress_test_default_off(self):
        args = self.parser.parse_args(["topic"])
        self.assertFalse(args.stress_test)


if __name__ == "__main__":
    unittest.main()
