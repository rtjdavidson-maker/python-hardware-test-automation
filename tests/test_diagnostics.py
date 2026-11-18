"""Unit tests for simulated device diagnostics."""
import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from diagnostics import Reading, evaluate, simulate_readings, write_report


class DiagnosticsTests(unittest.TestCase):
    def test_good_reading_passes(self):
        reading = Reading("DEV-001", 5.0, 25.0, 50.0)
        self.assertEqual(evaluate(reading)[0], "PASS")

    def test_bad_voltage_fails(self):
        reading = Reading("DEV-002", 5.5, 25.0, 50.0)
        self.assertIn("voltage out of range", evaluate(reading)[1])

    def test_hot_device_fails(self):
        reading = Reading("DEV-003", 5.0, 75.0, 50.0)
        self.assertIn("temperature out of range", evaluate(reading)[1])

    def test_slow_device_fails(self):
        reading = Reading("DEV-004", 5.0, 25.0, 120.0)
        self.assertIn("latency too high", evaluate(reading)[1])

    def test_simulation_is_reproducible(self):
        self.assertEqual(simulate_readings(seed=42), simulate_readings(seed=42))

    def test_csv_report(self):
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "reports" / "diagnostics.csv"
            write_report([Reading("DEV-005", 5.0, 25.0, 50.0)], destination)
            with destination.open(newline="", encoding="utf-8") as source:
                rows = list(csv.DictReader(source))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
