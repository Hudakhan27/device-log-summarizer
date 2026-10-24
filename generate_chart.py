"""
Section 3: Visualization Script
Generates a bar chart from output_summary.json comparing average device temperature.
"""

import json
import sys
import matplotlib.pyplot as plt


def generate_temperature_chart(json_path: str = "output_summary.json", save_path: str = "device_temperature_chart.png"):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Output file '{json_path}' not found. Run Section 2 first.")
        sys.exit(1)

    if not data:
        print("No device data available to plot.")
        return

    devices = [d["device_id"] for d in data]
    avg_temps = [d["avg_temperature"] for d in data]

    # Plot Configuration
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(devices, avg_temps, color="#3498db", edgecolor="#2980b9", width=0.5)

    # Threshold indicator line at 80°C limit
    ax.axhline(y=80.0, color="r", linestyle="--", alpha=0.7, label="Threshold Cutoff (80°C)")

    # Data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}°C",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold"
        )

    # Chart Labeling & Aesthetics
    ax.set_title("Average Temperature per Device (Filtered ≤ 80°C)", fontsize=14, pad=15, fontweight="bold")
    ax.set_xlabel("Device ID", fontsize=11, labelpad=10)
    ax.set_ylabel("Average Temperature (°C)", fontsize=11)
    ax.set_ylim(0, max(avg_temps, default=100) + 15)
    ax.legend(loc="upper right")

    # Tight layout prevents label clipping
    plt.tight_layout()

    # Save chart
    plt.savefig(save_path, dpi=300)
    print(f"Chart successfully saved to '{save_path}'")
    plt.close()


if __name__ == "__main__":
    generate_temperature_chart()