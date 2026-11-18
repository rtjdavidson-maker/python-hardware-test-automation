"""Tests for HTML diagnostics dashboard generation."""
import unittest

from dashboard import make_dashboard
from diagnostics import Reading


class DashboardTests(unittest.TestCase):
    def test_summary_counts(self):
        html = make_dashboard([
            Reading("DEV-001", 5.0, 30.0, 40.0),
            Reading("DEV-002", 5.5, 30.0, 40.0),
        ])
        self.assertIn("50.0%", html)
        self.assertIn("DEV-001", html)
        self.assertIn("DEV-002", html)
        self.assertIn("voltage out of range", html)

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            make_dashboard([])

    def test_device_id_html_escaped(self):
        html = make_dashboard([Reading("<script>alert(1)</script>", 5.0, 30.0, 40.0)])
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


if __name__ == "__main__":
    unittest.main()
