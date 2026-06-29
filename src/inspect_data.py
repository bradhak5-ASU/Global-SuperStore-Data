import pandas as pd

RAW = "data/raw/global_superstore.csv"

df = pd.read_csv(RAW, encoding="latin-1")

print("Shape (rows, cols):",df.shape)
print("Columns and types: ",df.dtypes)
print("Nulls per column: ",df.isnull().sum())
print("Duplicate Rows: ",df.duplicated().sum())
print("The First 5 Rows:")
print(df.head())
