import pandas as pd


INPUT_FILE = "data/raw/AAPL.csv"
OUTPUT_FILE = "data/processed/AAPL_clean.csv"
TICKER = "AAPL"


# ----------------------------------------
# 1. Load raw data
# ----------------------------------------

df = pd.read_csv(INPUT_FILE)


# ----------------------------------------
# 2. Convert date
# ----------------------------------------

df["Date"] = pd.to_datetime(df["Date"])


# ----------------------------------------
# 3. Standardise column names
# ----------------------------------------

df.columns = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume"
]


# ----------------------------------------
# 4. Add ticker identifier
# ----------------------------------------

df["ticker"] = TICKER


# ----------------------------------------
# 5. Inspect data
# ----------------------------------------

print(df.head())
print(df.shape)
print(df.dtypes)


# ----------------------------------------
# 6. Basic validation
# ----------------------------------------

duplicate_dates = df["date"].duplicated().sum()

print(f"Duplicate dates: {duplicate_dates}")


invalid_prices = (
    (df["open"] <= 0)
    | (df["high"] <= 0)
    | (df["low"] <= 0)
    | (df["close"] <= 0)
    | (df["adj_close"] <= 0)
).sum()

print(f"Invalid price records: {invalid_prices}")


invalid_volume = (df["volume"] < 0).sum()

print(f"Invalid volume records: {invalid_volume}")


# ----------------------------------------
# 7. Validate OHLC relationships
# ----------------------------------------

invalid_ohlc = (
    (df["high"] < df["low"])
    | (df["high"] < df["open"])
    | (df["high"] < df["close"])
    | (df["low"] > df["open"])
    | (df["low"] > df["close"])
).sum()

print(f"Invalid OHLC records: {invalid_ohlc}")


# ----------------------------------------
# 8. Sort chronologically
# ----------------------------------------

df = df.sort_values("date").reset_index(drop=True)


# ----------------------------------------
# 9. Create calculated financial fields
# ----------------------------------------

df["daily_return"] = df["close"].pct_change()

df["ma_7"] = df["close"].rolling(window=7).mean()

df["ma_30"] = df["close"].rolling(window=30).mean()


# ----------------------------------------
# 10. Inspect calculated fields
# ----------------------------------------

print(
    df[
        ["date", "ticker", "close", "daily_return", "ma_7", "ma_30"]
    ].head(35)
)


# ----------------------------------------
# 11. Check expected null values
# ----------------------------------------

print("\nCalculated field nulls:")

print(
    df[
        ["daily_return", "ma_7", "ma_30"]
    ].isnull().sum()
)


# ----------------------------------------
# 12. Save processed dataset
# ----------------------------------------

df.to_csv(OUTPUT_FILE, index=False)


print(f"\nProcessed data saved to: {OUTPUT_FILE}")
print(f"Processed rows: {len(df):,}")
print(f"Processed columns: {len(df.columns)}")