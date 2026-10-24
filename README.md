# Device Log Summarizer CLI Tool

A lightweight Python command-line utility designed to sanitize sensor telemetry, aggregate device metrics, export JSON summaries, and visualize performance data.

---

## Project Structure

```text
device-log-summarizer/
├── device_telemetry.csv         # Input raw telemetry dataset
├── sanitizer.py                 # Section 1: Data cleaning & sanitization module
├── summarizer.py                # Section 2: Core data processing CLI tool
├── generate_chart.py            # Section 3: Matplotlib visualization script
├── test_sanitizer.py            # Unit tests for Section 1
├── output_summary.json          # Filtered aggregated JSON output
├── device_temperature_chart.png # Generated visualization chart
└── PROMPT_LOG.md                # AI collaboration and prompt log
