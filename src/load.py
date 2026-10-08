import getpass

import pandas as pd
import psycopg


INPUT_FILE = "data/processed/AAPL_clean.csv"

DB_NAME = "financial_market"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"


# ----------------------------------------
# 1. Load processed data
# ----------------------------------------

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

print(f"Loaded {len(df):,} processed rows.")


# ----------------------------------------
# 2. Connect to PostgreSQL
# ----------------------------------------

password = getpass.getpass("Enter PostgreSQL password: ")

connection = psycopg.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=password,
    host=DB_HOST,
    port=DB_PORT
)

cursor = connection.cursor()

print("Connected to PostgreSQL.")


# ----------------------------------------
# 3. Load dim_security
# ----------------------------------------

ticker = df["ticker"].iloc[0]

cursor.execute(
    """
    INSERT INTO dim_security (ticker)
    VALUES (%s)
    ON CONFLICT (ticker) DO NOTHING;
    """,
    (ticker,)
)

connection.commit()

print(f"Security loaded: {ticker}")


# ----------------------------------------
# 4. Retrieve security_id
# ----------------------------------------

cursor.execute(
    """
    SELECT security_id
    FROM dim_security
    WHERE ticker = %s;
    """,
    (ticker,)
)

security_id = cursor.fetchone()[0]

print(f"security_id: {security_id}")


# ----------------------------------------
# 5. Load dim_date
# ----------------------------------------

for date in df["date"].drop_duplicates():

    cursor.execute(
        """
        INSERT INTO dim_date (
            full_date,
            year,
            month,
            day
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (full_date) DO NOTHING;
        """,
        (
            date.date(),
            date.year,
            date.month,
            date.day
        )
    )

connection.commit()

print("Date dimension loaded.")


# ----------------------------------------
# 6. Load fact_market_price
# ----------------------------------------

for _, row in df.iterrows():

    cursor.execute(
        """
        SELECT date_id
        FROM dim_date
        WHERE full_date = %s;
        """,
        (row["date"].date(),)
    )

    date_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO fact_market_price (
            security_id,
            date_id,
            open_price,
            high_price,
            low_price,
            close_price,
            adj_close,
            volume,
            daily_return,
            ma_7,
            ma_30
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (security_id, date_id)
        DO NOTHING;
        """,
        (
            security_id,
            date_id,
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            row["adj_close"],
            int(row["volume"]),
            None if pd.isna(row["daily_return"]) else row["daily_return"],
            None if pd.isna(row["ma_7"]) else row["ma_7"],
            None if pd.isna(row["ma_30"]) else row["ma_30"]
        )
    )

connection.commit()

print("Market price fact table loaded.")


# ----------------------------------------
# 7. Verify row counts
# ----------------------------------------

cursor.execute("SELECT COUNT(*) FROM dim_security;")
security_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM dim_date;")
date_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM fact_market_price;")
fact_count = cursor.fetchone()[0]


print("\nLoad Summary")
print("-" * 40)
print(f"dim_security rows: {security_count:,}")
print(f"dim_date rows: {date_count:,}")
print(f"fact_market_price rows: {fact_count:,}")


# ----------------------------------------
# 8. Close connection
# ----------------------------------------

cursor.close()
connection.close()

print("\nDatabase load complete.")