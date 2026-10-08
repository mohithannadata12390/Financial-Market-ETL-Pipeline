import os

import kagglehub
import pandas as pd


DATASET = "jacksoncrow/stock-market-dataset"
TICKER = "AAPL"
SOURCE_FILE = f"stocks/{TICKER}.csv"
OUTPUT_FILE = f"data/raw/{TICKER}.csv"


# --------------------------------------------------
# 1. Extract
# --------------------------------------------------

print("=" * 50)
print("Financial Market Data Extraction")
print("=" * 50)

print(f"\nSource: Kaggle")
print(f"Dataset: {DATASET}")
print(f"Ticker: {TICKER}")

path = kagglehub.dataset_download(
    DATASET,
    path=SOURCE_FILE
)

print("\nKaggle download successful.")


# --------------------------------------------------
# 2. Load into Pandas
# --------------------------------------------------

df = pd.read_csv(path)

print("Data loaded into Pandas.")


# --------------------------------------------------
# 3. Save raw data
# --------------------------------------------------

os.makedirs("data/raw", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 4. Basic verification
# --------------------------------------------------

missing_values = df.isnull().sum().sum()

print("\n" + "=" * 50)
print("Extraction Summary")
print("=" * 50)

print(f"Rows extracted: {len(df):,}")
print(f"Columns extracted: {len(df.columns)}")
print(f"Missing values: {missing_values:,}")

print(f"\nColumns:")
print(df.columns.tolist())

print(f"\nFirst record:")
print(df.iloc[0].to_dict())

print(f"\nLast record:")
print(df.iloc[-1].to_dict())

print(f"\nRaw data saved to:")
print(OUTPUT_FILE)

print("\nExtraction successful.")
print("=" * 50)