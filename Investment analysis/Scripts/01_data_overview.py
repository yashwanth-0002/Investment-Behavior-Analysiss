# ------------------------------------------------------------
# SCRIPT 1: DATA OVERVIEW
# Beginner-friendly project script
# ------------------------------------------------------------

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# These lines find the project folders automatically.
# This means the code can work on another computer after download.
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_FOLDER / "Data" / "Task 1.xlsx"
VISUALS_FOLDER = PROJECT_FOLDER / "Visuals"

# Read the Raw Data worksheet. Row 1 is the title, row 2 has column names.
if not DATA_FILE.exists():
    print("Dataset not found. Keep Task 1.xlsx inside the Data folder.")
    raise SystemExit

df = pd.read_excel(DATA_FILE, sheet_name="Raw Data", header=1)
df.columns = df.columns.str.strip()

print("=" * 60)
print("INVESTMENT BEHAVIOUR SURVEY - DATA OVERVIEW")
print("=" * 60)
print("Number of respondents:", df.shape[0])
print("Number of variables:", df.shape[1])

print("\nFirst five records:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nNumber of duplicate rows:", df.duplicated().sum())

# Count the number of respondents in each gender category.
gender_counts = df["gender"].value_counts()
gender_percentages = (gender_counts / len(df) * 100).round(1)

gender_table = pd.DataFrame({
    "Respondents": gender_counts,
    "Percentage": gender_percentages
})

print("\nGender distribution:")
print(gender_table)

# Create and save the gender chart.
VISUALS_FOLDER.mkdir(parents=True, exist_ok=True)
plt.figure(figsize=(8, 5))
bars = plt.bar(gender_counts.index, gender_counts.values)
plt.bar_label(
    bars,
    labels=[
        str(count) + " (" + str(gender_percentages[gender]) + "%)"
        for gender, count in gender_counts.items()
    ],
    padding=4
)
plt.title("Respondent Gender Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Gender")
plt.ylabel("Number of respondents")
plt.ylim(0, max(gender_counts.values) * 1.2)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "01_Gender_Distribution.png", dpi=300)
plt.show()

print("\nScript 1 completed. Gender chart saved in the Visuals folder.")
