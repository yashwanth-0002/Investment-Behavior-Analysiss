from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Resolve paths relative to this script so the project works after cloning
# the GitHub repository on another computer.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_PATH = PROJECT_DIR / "Data" / "Task 1.xlsx"
VISUALS_DIR = PROJECT_DIR / "Visuals"
OUTPUT_PATH = VISUALS_DIR / "01_Gender_Distribution.png"


def main() -> None:
    """Load the survey workbook, summarize data quality, and chart gender."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Check that Task 1.xlsx is inside the project's Data folder."
        )

    # The workbook's first row is a title; row 2 contains the column headers.
    df = pd.read_excel(DATA_PATH, sheet_name="Raw Data", header=1)
    df.columns = df.columns.astype(str).str.strip()

    if "gender" not in df.columns:
        raise KeyError(
            "Required column 'gender' was not found. "
            f"Available columns: {df.columns.tolist()}"
        )

    print("=" * 60)
    print("INVESTMENT BEHAVIOUR SURVEY — DATA OVERVIEW")
    print("=" * 60)
    print(f"Dataset shape: {df.shape[0]} respondents × {df.shape[1]} variables")

    print("\nFirst five records:")
    print(df.head())

    print("\nData types and non-null counts:")
    df.info()

    print("\nMissing values by column:")
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.sort_values(ascending=False))

    duplicate_count = int(df.duplicated().sum())
    print(f"\nDuplicate rows: {duplicate_count}")

    gender_counts = df["gender"].value_counts(dropna=False)
    gender_summary = (
        gender_counts.rename_axis("Gender")
        .reset_index(name="Respondents")
    )
    gender_summary["Percentage"] = (
        gender_summary["Respondents"] / len(df) * 100
    ).round(1)

    print("\nGender distribution:")
    print(gender_summary.to_string(index=False))

    # Create one chart only; save it as a high-resolution project visual.
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(
        gender_summary["Gender"].astype(str),
        gender_summary["Respondents"],
    )
    labels = [
        f"{int(count)} ({percentage:.1f}%)"
        for count, percentage in zip(
            gender_summary["Respondents"],
            gender_summary["Percentage"],
        )
    ]
    ax.bar_label(bars, labels=labels, padding=4, fontsize=10)
    ax.set_title("Respondent Gender Distribution", fontsize=14, weight="bold")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Number of respondents")
    ax.set_ylim(0, max(gender_summary["Respondents"]) * 1.2)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)

    print(f"\nChart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
