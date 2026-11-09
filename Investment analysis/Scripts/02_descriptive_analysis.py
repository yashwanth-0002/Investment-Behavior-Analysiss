# ------------------------------------------------------------
# SCRIPT 2: DESCRIPTIVE ANALYSIS
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

print("=" * 68)
print("INVESTMENT BEHAVIOUR SURVEY - DESCRIPTIVE ANALYSIS")
print("=" * 68)
print("Number of respondents:", len(df))

# Summary of respondent ages.
print("\nAGE SUMMARY")
print(df["age"].describe().round(2))

# Show counts and percentages for important survey questions.
columns_to_check = [
    "Investment_Avenues",
    "Stock_Marktet",
    "Factor",
    "Objective",
    "Purpose",
    "Duration",
    "Invest_Monitor",
    "Expect",
    "Avenue",
    "What are your savings objectives?",
    "Reason_Equity",
    "Reason_Mutual",
    "Reason_Bonds",
    "Reason_FD",
    "Source"
]

print("\nSURVEY RESPONSE DISTRIBUTIONS")
for column in columns_to_check:
    counts = df[column].value_counts()
    percentages = (counts / len(df) * 100).round(1)
    result = pd.DataFrame({"Count": counts, "Percentage": percentages})
    print("\n" + column)
    print(result)

# The seven investment columns contain respondent ranking values.
rank_columns = [
    "Mutual_Funds",
    "Equity_Market",
    "Debentures",
    "Government_Bonds",
    "Fixed_Deposits",
    "PPF",
    "Gold"
]

# Check whether every respondent used each rank from 1 to 7 once.
valid_rows = 0
for row_number in range(len(df)):
    respondent_ranks = df.loc[row_number, rank_columns].tolist()
    respondent_ranks.sort()
    if respondent_ranks == [1, 2, 3, 4, 5, 6, 7]:
        valid_rows = valid_rows + 1

print("\nINVESTMENT RANK VALIDATION")
print("Rows with ranks 1 to 7 exactly once:", valid_rows, "out of", len(df))

# Calculate the average rank for each investment type.
# IMPORTANT: A lower average is better only if rank 1 means highest preference.
average_ranks = df[rank_columns].mean().sort_values()
rank_names = {
    "Mutual_Funds": "Mutual Funds",
    "Equity_Market": "Equity Market",
    "Debentures": "Debentures",
    "Government_Bonds": "Government Bonds",
    "Fixed_Deposits": "Fixed Deposits",
    "PPF": "PPF",
    "Gold": "Gold"
}

rank_table = pd.DataFrame({
    "Investment Avenue": [rank_names[name] for name in average_ranks.index],
    "Average Rank": average_ranks.values
})

print("\nAVERAGE INVESTMENT RANK")
print(rank_table.round(3).to_string(index=False))
print("Note: Interpret a lower average as a stronger preference only if the questionnaire says rank 1 is the top preference.")

# Count the answer to the separate question called Avenue.
avenue_counts = df["Avenue"].value_counts()
avenue_percentages = (avenue_counts / len(df) * 100).round(1)
avenue_table = pd.DataFrame({
    "Respondents": avenue_counts,
    "Percentage": avenue_percentages
})
print("\nREPORTED INVESTMENT AVENUE")
print(avenue_table)

# Chart 1: Average rank by investment type.
rank_chart_data = average_ranks.sort_values(ascending=False)
rank_chart_names = [rank_names[name] for name in rank_chart_data.index]

plt.figure(figsize=(9, 5.5))
bars = plt.barh(rank_chart_names, rank_chart_data.values)
plt.bar_label(bars, fmt="%.2f", padding=4)
plt.title("Average Rank by Investment Avenue", fontsize=14, fontweight="bold")
plt.xlabel("Average rank (lower is better only if rank 1 is the top rank)")
plt.ylabel("Investment avenue")
plt.xlim(0, max(rank_chart_data.values) * 1.2)
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "02_Average_Investment_Rank.png", dpi=300)
plt.show()

# Chart 2: Number of respondents for each answer in the Avenue question.
avenue_chart_data = avenue_counts.sort_values()
avenue_chart_percentages = (avenue_chart_data / len(df) * 100).round(1)

plt.figure(figsize=(9, 5))
bars = plt.barh(avenue_chart_data.index, avenue_chart_data.values)
plt.bar_label(
    bars,
    labels=[
        str(count) + " (" + str(avenue_chart_percentages[name]) + "%)"
        for name, count in avenue_chart_data.items()
    ],
    padding=4
)
plt.title("Reported Investment Avenue", fontsize=14, fontweight="bold")
plt.xlabel("Number of respondents")
plt.ylabel("Investment avenue")
plt.xlim(0, max(avenue_chart_data.values) * 1.25)
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(VISUALS_FOLDER / "03_Reported_Investment_Avenue.png", dpi=300)
plt.show()

print("\nScript 2 completed. Two charts saved in the Visuals folder.")
