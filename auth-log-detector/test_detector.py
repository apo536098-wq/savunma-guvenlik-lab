import json
import tempfile
import unittest
from pathlib import Path

from src.detector import detect


class DetectorTests(unittest.TestCase):
    def test_detects_burst_and_ignores_success(self):
        events = [
            {"timestamp": f"2026-01-01T00:00:0{i}+00:00", "source_ip": "192.0.2.1", "result": "failure"}
            for i in range(5)
        ] + [{"timestamp": "2026-01-01T00:00:06+00:00", "source_ip": "192.0.2.1", "result": "success"}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")
            alerts = detect(path, threshold=5, window_seconds=60)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["attempt_count"], 5)

    def test_does_not_alert_outside_window(self):
        events = [
            {"timestamp": f"2026-01-01T00:00:{second:02d}+00:00", "source_ip": "192.0.2.2", "result": "failure"}
            for second in (0, 20, 40, 59, 61)
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")
            alerts = detect(path, threshold=5, window_seconds=60)
        self.assertEqual(alerts, [])

    def test_rejects_invalid_ip(self):
        event = {"timestamp": "2026-01-01T00:00:00+00:00", "source_ip": "not-an-ip", "result": "failure"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text(json.dumps(event), encoding="utf-8")
            with self.assertRaises(ValueError):
                detect(path)


if __name__ == "__main__":
    unittest.main()
