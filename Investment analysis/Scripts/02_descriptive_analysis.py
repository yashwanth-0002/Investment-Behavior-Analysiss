"""Descriptive analysis for the Investment Behaviour Survey.

Run this file from IDLE or a terminal. It reads the workbook from the
project's Data folder and saves charts to the project's Visuals folder.

Interpretation note:
The seven investment columns contain ranks 1 through 7 for each respondent.
This script reports average ranks. Treat a lower average as a stronger
preference ONLY if the original questionnaire defined rank 1 as the top rank.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Resolve project paths relative to this script (not a personal computer path).
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_PATH = PROJECT_DIR / "Data" / "Task 1.xlsx"
VISUALS_DIR = PROJECT_DIR / "Visuals"

INVESTMENT_RANK_COLUMNS = [
    "Mutual_Funds",
    "Equity_Market",
    "Debentures",
    "Government_Bonds",
    "Fixed_Deposits",
    "PPF",
    "Gold",
]

DISPLAY_NAMES = {
    "Mutual_Funds": "Mutual Funds",
    "Equity_Market": "Equity Market",
    "Debentures": "Debentures",
    "Government_Bonds": "Government Bonds",
    "Fixed_Deposits": "Fixed Deposits",
    "PPF": "PPF",
    "Gold": "Gold",
}

CATEGORICAL_COLUMNS = [
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
    "Source",
]


def print_frequency_table(df: pd.DataFrame, column: str) -> None:
    """Print category counts and percentages for one survey column."""
    counts = df[column].value_counts(dropna=False)
    summary = counts.rename_axis("Response").reset_index(name="Count")
    summary["Percentage"] = (summary["Count"] / len(df) * 100).round(1)
    print(f"\n{column}")
    print(summary.to_string(index=False))


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Keep 'Task 1.xlsx' inside the project's Data folder."
        )

    # Row 1 of the workbook is a title; row 2 contains column headers.
    df = pd.read_excel(DATA_PATH, sheet_name="Raw Data", header=1)
    df.columns = df.columns.astype(str).str.strip()

    missing_columns = [
        column
        for column in INVESTMENT_RANK_COLUMNS + CATEGORICAL_COLUMNS + ["age"]
        if column not in df.columns
    ]
    if missing_columns:
        raise KeyError(
            "The workbook is missing required columns: "
            + ", ".join(missing_columns)
        )

    print("=" * 68)
    print("INVESTMENT BEHAVIOUR SURVEY — DESCRIPTIVE ANALYSIS")
    print("=" * 68)
    print(f"Respondents: {len(df)}")

    # Basic respondent age summary.
    print("\nAGE SUMMARY")
    age_summary = df["age"].describe().round(2)
    print(age_summary.to_string())

    # Show response distributions for key survey questions.
    print("\nSURVEY RESPONSE DISTRIBUTIONS")
    for column in CATEGORICAL_COLUMNS:
        print_frequency_table(df, column)

    # Validate the seven ranking columns before calculating average ranks.
    ranks = df[INVESTMENT_RANK_COLUMNS].apply(pd.to_numeric, errors="coerce")
    expected_ranks = list(range(1, len(INVESTMENT_RANK_COLUMNS) + 1))
    valid_rows = ranks.apply(
        lambda row: sorted(row.dropna().tolist()) == expected_ranks,
        axis=1,
    )
    print("\nINVESTMENT RANK VALIDATION")
    print(f"Rows with ranks 1 through 7 exactly once: {int(valid_rows.sum())}/{len(df)}")

    if not valid_rows.all():
        print(
            "WARNING: Some rows do not contain each rank from 1 to 7 exactly once. "
            "Review the ranking data before interpreting average ranks."
        )

    rank_summary = pd.DataFrame(
        {
            "Investment Avenue": [DISPLAY_NAMES[column] for column in INVESTMENT_RANK_COLUMNS],
            "Total Rank Score": ranks.sum().values,
            "Average Rank": ranks.mean().round(3).values,
        }
    ).sort_values("Average Rank", ascending=True)

    print("\nAVERAGE INVESTMENT RANK")
    print(rank_summary.to_string(index=False))
    print(
        "\nInterpretation note: a lower average rank indicates a stronger "
        "preference only if the questionnaire defined rank 1 as the highest preference."
    )

    # Count the single response recorded in the separate 'Avenue' question.
    avenue_counts = df["Avenue"].value_counts().rename_axis("Investment Avenue")
    avenue_summary = avenue_counts.reset_index(name="Respondents")
    avenue_summary["Percentage"] = (
        avenue_summary["Respondents"] / len(df) * 100
    ).round(1)
    print("\nMOST FREQUENTLY REPORTED INVESTMENT AVENUE")
    print(avenue_summary.to_string(index=False))

    # Save reproducible charts for the GitHub project.
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    rank_plot = rank_summary.sort_values("Average Rank", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(rank_plot["Investment Avenue"], rank_plot["Average Rank"])
    ax.bar_label(bars, fmt="%.2f", padding=4, fontsize=9)
    ax.set_title("Average Rank by Investment Avenue", fontsize=14, weight="bold")
    ax.set_xlabel("Average rank (lower indicates higher preference if rank 1 is best)")
    ax.set_ylabel("Investment avenue")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(rank_plot["Average Rank"]) * 1.2)
    fig.tight_layout()
    rank_chart_path = VISUALS_DIR / "02_Average_Investment_Rank.png"
    fig.savefig(rank_chart_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

    selection_plot = avenue_summary.sort_values("Respondents", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(selection_plot["Investment Avenue"], selection_plot["Respondents"])
    labels = [
        f"{int(count)} ({percentage:.1f}%)"
        for count, percentage in zip(
            selection_plot["Respondents"], selection_plot["Percentage"]
        )
    ]
    ax.bar_label(bars, labels=labels, padding=4, fontsize=9)
    ax.set_title("Reported Investment Avenue", fontsize=14, weight="bold")
    ax.set_xlabel("Number of respondents")
    ax.set_ylabel("Investment avenue")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(selection_plot["Respondents"]) * 1.25)
    fig.tight_layout()
    avenue_chart_path = VISUALS_DIR / "03_Reported_Investment_Avenue.png"
    fig.savefig(avenue_chart_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

    print("\nCHARTS SAVED")
    print(rank_chart_path)
    print(avenue_chart_path)
    print("\nDescriptive analysis completed.")


if __name__ == "__main__":
    main()
