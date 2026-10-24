"""
Section 1: Data Sanitization Module
Cleans, filters, converts, and clips raw sensor reading lists.
"""

from typing import List, Any


def clean_and_normalize_sensor_readings(raw_values: List[Any]) -> List[float]:
    """
    Cleans mixed sensor readings by:
    1. Converting valid items to float (dropping None, non-numeric strings, negative values).
    2. Clipping values greater than 500.0 to 500.0.
    3. Gracefully handling empty or all-invalid inputs.
    
    :param raw_values: List containing mixed types (str, int, float, None, etc.)
    :return: List of cleaned, non-negative, clipped floats.
    """
    if not isinstance(raw_values, list) or not raw_values:
        return []

    cleaned_readings: List[float] = []

    for item in raw_values:
        if item is None:
            continue

        try:
            val = float(item)
            # Filter out negative error flags
            if val < 0:
                continue
            # Clip upper limit to 500.0
            if val > 500.0:
                val = 500.0
            cleaned_readings.append(val)
        except (ValueError, TypeError):
            # Drop items that cannot be converted to float
            continue

    return cleaned_readings


# --- Test Suite ---
if __name__ == "__main__":
    print("Running Sanitizer Tests...")

    # Test Case 1: Mixed inputs with negative flags and standard values
    test_1 = ["12.5", -999, None, "45.0", "invalid", 600.2, 0.0]
    expected_1 = [12.5, 45.0, 500.0, 0.0]
    assert clean_and_normalize_sensor_readings(test_1) == expected_1, f"Test 1 Failed"
    print("✔ Test 1 Passed: Mixed valid/invalid values handled correctly.")

    # Test Case 2: All invalid inputs
    test_2 = [None, "N/A", -10, "-50", "corrupted"]
    expected_2 = []
    assert clean_and_normalize_sensor_readings(test_2) == expected_2, "Test 2 Failed"
    print("✔ Test 2 Passed: All-invalid list handled gracefully without error.")

    # Test Case 3: Empty input list
    test_3 = []
    expected_3 = []
    assert clean_and_normalize_sensor_readings(test_3) == expected_3, "Test 3 Failed"
    print("✔ Test 3 Passed: Empty list handled gracefully.")

    print("All Sanitizer tests completed successfully!")