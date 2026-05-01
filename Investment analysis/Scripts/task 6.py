import pandas as pd

df = pd.read_csv(
    r"C:\Users\Lenovo\OneDrive\Desktop\Data analytics all files\Task 1.csv",
    encoding="latin1",
    header=1
)

print(df['What are your savings objectives?'].value_counts())
## task 6
print(df['Source'].value_counts())

## task 7
print(df['Duration'].value_counts())

duration_map = {
    'Less than 1 year': 0.5,
    '1-3 years': 2,
    '3-5 years': 4,
    'More than 5 years': 6
}

df['Duration_numeric'] = df['Duration'].map(duration_map)

print(df['Duration_numeric'].mean())

##task 9
print(df['Expect'].value_counts())

##Task 10
import seaborn as sns
import matplotlib.pyplot as plt

# Select numerical columns
numeric_df = df.select_dtypes(include=['int64', 'float64'])

# Correlation matrix
corr = numeric_df.corr()

print(corr)

# Heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm')

plt.title("Correlation Matrix")
plt.show()
