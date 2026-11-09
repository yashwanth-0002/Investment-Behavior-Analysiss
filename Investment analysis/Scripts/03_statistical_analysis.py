# ------------------------------------------------------------
# SCRIPT 3: STATISTICAL ANALYSIS
# Beginner-friendly project script
# ------------------------------------------------------------

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_FOLDER / "Data" / "Task 1.xlsx"
VISUALS_FOLDER = PROJECT_FOLDER / "Visuals"
RESULTS_FOLDER = PROJECT_FOLDER / "Results"

if not DATA_FILE.exists():
    print("Dataset not found. Keep Task 1.xlsx inside the Data folder.")
    raise SystemExit

df = pd.read_excel(DATA_FILE, sheet_name="Raw Data", header=1)
df.columns = df.columns.str.strip()
VISUALS_FOLDER.mkdir(parents=True, exist_ok=True)
RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 68)
print("INVESTMENT BEHAVIOUR SURVEY - STATISTICAL ANALYSIS")
print("=" * 68)

# PART 1: Investment duration distribution.
print("\nINVESTMENT DURATION")
duration_counts = df["Duration"].value_counts()
duration_percentages = (duration_counts / len(df) * 100).round(1)
print(pd.DataFrame({"Count": duration_counts, "Percentage": duration_percentages}))

# Convert duration categories into approximate numbers of years.
# These are representative values, not the exact duration of each person.
duration_map = {
    "Less than 1 year": 0.5,
    "1-3 years": 2,
    "3-5 years": 4,
    "More than 5 years": 6
}

df["Duration_Numeric"] = df["Duration"].map(duration_map)
average_duration = df["Duration_Numeric"].mean()

print("\nApproximate average investment duration:", round(average_duration, 2), "years")
print("Note: The average uses representative values of 0.5, 2, 4 and 6 years for the four duration groups.")

# PART 2: Spearman correlation.
# Spearman is used because the investment columns contain ranking data.
rank_columns = [
    "Mutual_Funds",
    "Equity_Market",
    "Debentures",
    "Government_Bonds",
    "Fixed_Deposits",
    "PPF",
    "Gold"
]

correlation_columns = ["age"] + rank_columns
correlation_data = df[correlation_columns]
spearman_correlation = correlation_data.corr(method="spearman")

print("\nSPEARMAN CORRELATION MATRIX")
print(spearman_correlation.round(2))

# Save the correlation table as a CSV file for reference.
spearman_correlation.to_csv(RESULTS_FOLDER / "Spearman_Correlation.csv")

# Use shorter labels so the heatmap is easier to read.
short_names = {
    "age": "Age",
    "Mutual_Funds": "Mutual Funds",
    "Equity_Market": "Equity Market",
    "Debentures": "Debentures",
    "Government_Bonds": "Govt Bonds",
    "Fixed_Deposits": "Fixed Deposits",
    "PPF": "PPF",
    "Gold": "Gold"
}

heatmap_data = spearman_correlation.rename(
    index=short_names,
    columns=short_names
)

plt.figure(figsize=(10, 8))
sns.heatmap(
    heatmap_data,
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt=".2f",
    square=True,
    linewidths=0.5
)
plt.title("Spearman Correlation - Age and Investment Rankings", fontsize=14, fontweight="bold")
plt.xticks(rotation=35, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "04_Spearman_Correlation_Heatmap.png", dpi=300)
plt.show()

print("\nScript 3 completed.")
print("Correlation table saved in the Results folder.")
print("Correlation heatmap saved in the Visuals folder.")
print("Reminder: Correlation shows association, not cause and effect.")
