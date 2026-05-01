import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset correctly
df = pd.read_csv(
    r"C:\Users\Lenovo\OneDrive\Desktop\Data analytics all files\Task 1.csv",
    encoding="latin1",
    header=1
)

# Show first 5 rows
print(df.head())

# Dataset info
print("\nDataset Info:")
print(df.info())

# Column names
print("\nColumns:")
print(df.columns)

print(df['gender'].value_counts())

import matplotlib.pyplot as plt

df['gender'].value_counts().plot(kind='bar')

plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")

plt.show()

print(df['gender'].value_counts())
sns.countplot(x='gender', data=df)
plt.title("Gender Distribution")
plt.show()

