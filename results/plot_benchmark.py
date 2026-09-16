import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "results" / "agent_speed_comparison.csv"
OUT_PATH = ROOT / "results" / "benchmark_chart.png"

# Load CSV data
df = pd.read_csv(CSV_PATH)

print("Benchmark data:")
print(df)

# Calculate average execution time
baseline_avg = df["BaselineSeconds"].mean()
agent02_avg = df["Agent02Seconds"].mean()

# Calculate number of faster tasks
baseline_faster = (df["FasterAgent"] == "baseline").sum()
agent02_faster = (df["FasterAgent"] == "agent_02").sum()

# Data for chart
agents = ["Baseline", "Agent 02"]
average_times = [baseline_avg, agent02_avg]

# Create chart
plt.figure(figsize=(9, 6))

bars = plt.bar(agents, average_times)

plt.title("Agent Benchmark Comparison")
plt.xlabel("Agent")
plt.ylabel("Average Execution Time (seconds)")

# Display values above bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.3f}s",
        ha="center",
        va="bottom",
    )

plt.tight_layout()

# Save chart
plt.savefig(OUT_PATH, dpi=300)

print("\nAverage execution times:")
print(f"Baseline: {baseline_avg:.3f} seconds")
print(f"Agent 02: {agent02_avg:.3f} seconds")

print("\nFaster task count:")
print(f"Baseline: {baseline_faster} tasks")
print(f"Agent 02: {agent02_faster} tasks")

print(f"\nChart saved successfully at:\n{OUT_PATH}")

# plt.show()