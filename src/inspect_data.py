import pandas as pd

RAW = "data/raw/global_superstore.csv"

df = pd.read_csv(RAW, encoding="latin-1")

print("Shape (rows, cols):",df.shape)
print("Columns and types: ",df.dtypes)
print("Nulls per column: ",df.isnull().sum())
print("Duplicate Rows: ",df.duplicated().sum())
print("The First 10 Rows:")
print(df.head(10))

print(df["Order Date"].head())
print(df["Ship Date"].head())

print("Providing the data info \n",df.info)
print("Providing the stats: ")
print(df.describe())