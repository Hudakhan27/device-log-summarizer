"""
Unit tests for Section 1: Data Sanitization Module
Run using: python -m unittest test_sanitizer.py
"""

import unittest
from sanitizer import clean_and_normalize_sensor_readings


class TestSensorSanitizer(unittest.TestCase):

    def test_mixed_inputs_and_clipping(self):
        """Test conversion, negative filtering, and clipping values > 500.0."""
        raw = ["12.5", -999, None, "45.0", "invalid", 600.2, 0.0]
        expected = [12.5, 45.0, 500.0, 0.0]
        self.assertEqual(clean_and_normalize_sensor_readings(raw), expected)

    def test_all_invalid_inputs(self):
        """Test list containing entirely invalid or negative entries."""
        raw = [None, "N/A", -10, "-50", "corrupted"]
        expected = []
        self.assertEqual(clean_and_normalize_sensor_readings(raw), expected)

    def test_empty_list(self):
        """Test handling of an empty list input gracefully."""
        raw = []
        expected = []
        self.assertEqual(clean_and_normalize_sensor_readings(raw), expected)


if __name__ == "__main__":
    unittest.main()