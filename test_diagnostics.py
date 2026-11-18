import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from diagnostics import Reading, evaluate, simulate_readings, write_report


class DiagnosticsTests(unittest.TestCase):
    def test_good_reading_passes(self):
        self.assertEqual(evaluate(Reading("A", 5.0, 35, 50))[0], "PASS")

    def test_bad_voltage_fails(self):
        self.assertIn("voltage", evaluate(Reading("B", 5.4, 35, 50))[1])

    def test_hot_device_fails(self):
        self.assertIn("temperature", evaluate(Reading("C", 5.0, 75, 50))[1])

    def test_slow_device_fails(self):
        self.assertIn("latency", evaluate(Reading("D", 5.0, 35, 110))[1])

    def test_simulation_is_reproducible(self):
        self.assertEqual(simulate_readings(seed=12), simulate_readings(seed=12))

    def test_csv_report(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "results.csv"
            write_report([Reading("A", 5.0, 35, 50)], path)
            self.assertIn("PASS", path.read_text())


if __name__ == "__main__":
    unittest.main()
