# ------------------------------------------------------------
# SCRIPT 4: ADDITIONAL VISUALIZATIONS
# Beginner-friendly project script
# ------------------------------------------------------------

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_FOLDER / "Data" / "Task 1.xlsx"
VISUALS_FOLDER = PROJECT_FOLDER / "Visuals"

if not DATA_FILE.exists():
    print("Dataset not found. Keep Task 1.xlsx inside the Data folder.")
    raise SystemExit

df = pd.read_excel(DATA_FILE, sheet_name="Raw Data", header=1)
df.columns = df.columns.str.strip()
VISUALS_FOLDER.mkdir(parents=True, exist_ok=True)

# CHART 1: Expected return distribution.
expected_counts = df["Expect"].value_counts().reindex(
    ["10%-20%", "20%-30%", "30%-40%"], fill_value=0
)
expected_percentages = (expected_counts / len(df) * 100).round(1)

plt.figure(figsize=(8, 5))
bars = plt.bar(expected_counts.index, expected_counts.values)
plt.bar_label(
    bars,
    labels=[
        str(count) + " (" + str(expected_percentages[label]) + "%)"
        for label, count in expected_counts.items()
    ],
    padding=4
)
plt.title("Expected Return Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Expected return range")
plt.ylabel("Number of respondents")
plt.ylim(0, max(expected_counts.values) * 1.2)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "05_Expected_Returns.png", dpi=300)
plt.show()

# CHART 2: Main information source.
source_counts = df["Source"].value_counts().sort_values()
source_percentages = (source_counts / len(df) * 100).round(1)

plt.figure(figsize=(9, 5))
bars = plt.barh(source_counts.index, source_counts.values)
plt.bar_label(
    bars,
    labels=[
        str(count) + " (" + str(source_percentages[label]) + "%)"
        for label, count in source_counts.items()
    ],
    padding=4
)
plt.title("Sources of Investment Information", fontsize=14, fontweight="bold")
plt.xlabel("Number of respondents")
plt.ylabel("Information source")
plt.xlim(0, max(source_counts.values) * 1.25)
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "06_Information_Sources.png", dpi=300)
plt.show()

# CHART 3: Savings objectives.
savings_counts = df["What are your savings objectives?"].value_counts().sort_values()
savings_percentages = (savings_counts / len(df) * 100).round(1)

plt.figure(figsize=(9, 5))
bars = plt.barh(savings_counts.index, savings_counts.values)
plt.bar_label(
    bars,
    labels=[
        str(count) + " (" + str(savings_percentages[label]) + "%)"
        for label, count in savings_counts.items()
    ],
    padding=4
)
plt.title("Respondents' Savings Objectives", fontsize=14, fontweight="bold")
plt.xlabel("Number of respondents")
plt.ylabel("Savings objective")
plt.xlim(0, max(savings_counts.values) * 1.25)
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "07_Savings_Objectives.png", dpi=300)
plt.show()

# CHART 4: Investment duration groups in their natural order.
duration_order = [
    "Less than 1 year",
    "1-3 years",
    "3-5 years",
    "More than 5 years"
]
duration_counts = df["Duration"].value_counts().reindex(duration_order, fill_value=0)
duration_percentages = (duration_counts / len(df) * 100).round(1)

plt.figure(figsize=(9, 5))
bars = plt.barh(duration_counts.index, duration_counts.values)
plt.bar_label(
    bars,
    labels=[
        str(count) + " (" + str(duration_percentages[label]) + "%)"
        for label, count in duration_counts.items()
    ],
    padding=4
)
plt.title("Investment Duration of Respondents", fontsize=14, fontweight="bold")
plt.xlabel("Number of respondents")
plt.ylabel("Investment duration")
plt.xlim(0, max(duration_counts.values) * 1.25)
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "08_Investment_Duration.png", dpi=300)
plt.show()

print("All four additional charts have been saved in the Visuals folder.")
