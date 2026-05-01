import pandas as pd

# Load dataset (must come first)
df = pd.read_csv(
    r"C:\Users\Lenovo\OneDrive\Desktop\Data analytics all files\Task 1.csv",
    encoding="latin1",
    header=1
)

# Select numerical columns
numeric_df = df.select_dtypes(include=['int64'])

# Descriptive statistics
print(numeric_df.describe())


import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(
    r"C:\Users\Lenovo\OneDrive\Desktop\Data analytics all files\Task 1.csv",
    encoding="latin1",
    header=1
)

# Investment columns
investment_cols = [
    'Mutual_Funds', 'Equity_Market', 'Debentures',
    'Government_Bonds', 'Fixed_Deposits', 'PPF', 'Gold'
]

# Sum of each investment type
print(df[investment_cols].sum())

# Visualization
df[investment_cols].sum().plot(kind='bar')

plt.title("Most Preferred Investment Avenue")
plt.ylabel("Total Score")
plt.xticks(rotation=45)

print(df['Reason_Equity'].value_counts())
print(df['Reason_Mutual'].value_counts())
print(df['Reason_Bonds'].value_counts())
print(df['Reason_FD'].value_counts())

plt.show()

top_investment = df[investment_cols].sum().idxmax()
print("Most Preferred Investment:", top_investment)

print(df['Reason_Equity'].value_counts())

print(df['What are your savings objectives?'].value_counts())
