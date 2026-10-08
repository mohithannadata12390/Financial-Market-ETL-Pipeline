import pandas as pd

INPUT_FILE = "data/processed/AAPL_clean.csv"

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])


EXPECTED_COLUMNS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "ticker",
    "daily_return",
    "ma_7",
    "ma_30"
]

missing_columns = [
    column
    for column in EXPECTED_COLUMNS
    if column not in df.columns
]

print(f"Missing expected columns: {missing_columns}")

df["date"].duplicated()

duplicate_records = df.duplicated(
    subset=["ticker", "date"]
).sum()

print(f"Duplicate ticker-date records: {duplicate_records}")

CORE_COLUMNS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "ticker"
]

missing_core_values = df[CORE_COLUMNS].isnull().sum()

print("\nMissing core values:")
print(missing_core_values)

# Check invalid prices
invalid_prices = (
    (df["open"] <= 0)
    | (df["high"] <= 0)
    | (df["low"] <= 0)
    | (df["close"] <= 0)
    | (df["adj_close"] <= 0)
).sum()

print(f"\nInvalid price records: {invalid_prices}")


# Check invalid volume
invalid_volume = (df["volume"] < 0).sum()

print(f"Invalid volume records: {invalid_volume}")


# Check OHLC business rules
invalid_ohlc = (
    (df["high"] < df["low"])
    | (df["high"] < df["open"])
    | (df["high"] < df["close"])
    | (df["low"] > df["open"])
    | (df["low"] > df["close"])
).sum()

print(f"Invalid OHLC records: {invalid_ohlc}")


# Check ticker values
invalid_tickers = (df["ticker"] != "AAPL").sum()

print(f"Invalid ticker records: {invalid_tickers}")

validation_passed = (
    len(missing_columns) == 0
    and duplicate_records == 0
    and missing_core_values.sum() == 0
    and invalid_prices == 0
    and invalid_volume == 0
    and invalid_ohlc == 0
    and invalid_tickers == 0
)

print("\n" + "=" * 40)

if validation_passed:
    print("VALIDATION PASSED")
else:
    print("VALIDATION FAILED")

print("=" * 40)