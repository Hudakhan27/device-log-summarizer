"""
Section 2: Device Log Summarizer CLI Tool
Processes telemetry CSV data, aggregates stats per device, filters out 
devices exceeding mean 80.0°C, and outputs JSON + CLI terminal table.
"""

import sys
import json
import logging
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def process_telemetry_data(input_csv_path: str, output_json_path: str) -> None:
    csv_file = Path(input_csv_path)

    # File existence check
    if not csv_file.exists():
        logging.error(f"Input file non-existent: '{input_csv_path}'")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        logging.error(f"Failed to read CSV file: {e}")
        sys.exit(1)

    # Validate required columns
    required_cols = {"device_id", "status", "temperature"}
    if not required_cols.issubset(df.columns):
        logging.error(f"CSV missing required columns. Expected {required_cols}")
        sys.exit(1)

    # Clean temperature data using numeric conversion
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df = df.dropna(subset=["temperature"])

    # Aggregation logic
    grouped = df.groupby("device_id").agg(
        total_records=("status", "count"),
        avg_temperature=("temperature", "mean"),
        error_count=("status", lambda s: (s == "ERROR").sum())
    ).reset_index()

    # Round average temperature to 2 decimal places
    grouped["avg_temperature"] = grouped["avg_temperature"].round(2)

    # Filter out devices with avg_temperature > 80.0
    filtered_df = grouped[grouped["avg_temperature"] <= 80.0]

    # Convert results to list of dicts for JSON serialization
    results = filtered_df.to_dict(orient="records")

    # Export to JSON
    try:
        with open(output_json_path, "w") as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results successfully saved to '{output_json_path}'")
    except IOError as e:
        logging.error(f"Failed writing JSON output: {e}")
        sys.exit(1)

    # Print terminal summary table
    print("\n" + "="*55)
    print(f"{'DEVICE SUMMARY REPORT (Filtered Avg Temp <= 80°C)':^55}")
    print("="*55)
    print(f"{'Device ID':<12} | {'Total Logs':<12} | {'Avg Temp (°C)':<15} | {'Error Count':<10}")
    print("-" * 55)
    for row in results:
        print(f"{row['device_id']:<12} | {row['total_records']:<12} | {row['avg_temperature']:<15.2f} | {row['error_count']:<10}")
    print("="*55 + "\n")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "device_telemetry.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_summary.json"
    process_telemetry_data(input_file, output_file)