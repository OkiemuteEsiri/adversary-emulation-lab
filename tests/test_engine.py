import unittest

from src.engine import assess, execution_gate, score
from src.models import Exercise, Observation, Technique


def technique(approved=True):
    return Technique("T1078", "Valid Accounts", "Initial Access", "Validate detection", ("idp", "siem"), approved)


def exercise(**overrides):
    values = dict(exercise_id="E1", name="Lab", environment="isolated", owner="Purple Team", authorized=True, production=False, stop_conditions=("scope ambiguity",), techniques=(technique(),))
    values.update(overrides)
    return Exercise(**values)


class EngineTests(unittest.TestCase):
    def test_gate_allows_authorized_nonproduction(self):
        self.assertEqual(execution_gate(exercise()), (True, ()))

    def test_gate_blocks_unauthorized(self):
        allowed, reasons = execution_gate(exercise(authorized=False))
        self.assertFalse(allowed)
        self.assertIn("exercise is not explicitly authorized", reasons)

    def test_gate_blocks_production(self):
        self.assertFalse(execution_gate(exercise(production=True))[0])

    def test_gate_blocks_unapproved_technique(self):
        ex = exercise(techniques=(technique(False),))
        self.assertFalse(execution_gate(ex)[0])

    def test_missing_observation_is_high(self):
        findings = assess(exercise(), ())
        self.assertEqual(findings[0].severity, "high")

    def test_detection_gap_is_high(self):
        obs = (Observation("T1078", "idp", "not_detected", "E1"), Observation("T1078", "siem", "not_detected", "E2"))
        self.assertTrue(any(f.title == "Detection objective not met" for f in assess(exercise(), obs)))

    def test_missing_source_is_medium(self):
        obs = (Observation("T1078", "idp", "detected", "E1"),)
        self.assertTrue(any(f.severity == "medium" for f in assess(exercise(), obs)))

    def test_missing_evidence_is_low(self):
        obs = (Observation("T1078", "idp", "detected", ""), Observation("T1078", "siem", "detected", "E2"))
        self.assertTrue(any(f.severity == "low" for f in assess(exercise(), obs)))

    def test_finding_ids_are_deterministic(self):
        self.assertEqual(assess(exercise(), ())[0].finding_id, assess(exercise(), ())[0].finding_id)

    def test_score_bounded(self):
        self.assertGreaterEqual(score(assess(exercise(), ())), 0)
        self.assertLessEqual(score(assess(exercise(), ())), 100)


if __name__ == "__main__":
    unittest.main()
