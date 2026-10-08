CREATE TABLE IF NOT EXISTS dim_security (
    security_id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_market_price (
    market_price_id SERIAL PRIMARY KEY,

    security_id INT NOT NULL
        REFERENCES dim_security(security_id),

    date_id INT NOT NULL
        REFERENCES dim_date(date_id),

    open_price NUMERIC(18,6),
    high_price NUMERIC(18,6),
    low_price NUMERIC(18,6),
    close_price NUMERIC(18,6),
    adj_close NUMERIC(18,6),

    volume BIGINT,

    daily_return NUMERIC(18,10),
    ma_7 NUMERIC(18,6),
    ma_30 NUMERIC(18,6),

    UNIQUE (security_id, date_id)
);