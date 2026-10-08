-- ============================================
-- 1. MARKET PRICE OVERVIEW
-- ============================================

SELECT
    s.ticker,
    d.full_date,
    f.open_price,
    f.high_price,
    f.low_price,
    f.close_price,
    f.volume,
    f.daily_return,
    f.ma_7,
    f.ma_30
FROM fact_market_price AS f
JOIN dim_security AS s
    ON f.security_id = s.security_id
JOIN dim_date AS d
    ON f.date_id = d.date_id
ORDER BY d.full_date
LIMIT 10;

-- ============================================
-- 2. YEARLY MARKET SUMMARY
-- ============================================

SELECT
    s.ticker,
    d.year,
    COUNT(*) AS trading_days,
    ROUND(AVG(f.close_price), 2) AS avg_close_price,
    ROUND(MIN(f.low_price), 2) AS lowest_price,
    ROUND(MAX(f.high_price), 2) AS highest_price,
    SUM(f.volume) AS total_volume,
    ROUND(AVG(f.daily_return) * 100, 4) AS avg_daily_return_pct
FROM fact_market_price AS f
JOIN dim_security AS s
    ON f.security_id = s.security_id
JOIN dim_date AS d
    ON f.date_id = d.date_id
GROUP BY
    s.ticker,
    d.year
ORDER BY
    d.year;

    -- ============================================
-- 3. YEARLY PRICE RETURN USING A CTE
-- ============================================

WITH yearly_prices AS (
    SELECT
        s.ticker,
        d.year,
        FIRST_VALUE(f.close_price) OVER (
            PARTITION BY s.ticker, d.year
            ORDER BY d.full_date
        ) AS first_close,

        FIRST_VALUE(f.close_price) OVER (
            PARTITION BY s.ticker, d.year
            ORDER BY d.full_date DESC
        ) AS last_close
    FROM fact_market_price AS f
    JOIN dim_security AS s
        ON f.security_id = s.security_id
    JOIN dim_date AS d
        ON f.date_id = d.date_id
)

SELECT
    ticker,
    year,
    ROUND(MIN(first_close), 2) AS first_close,
    ROUND(MIN(last_close), 2) AS last_close,
    ROUND(
        ((MIN(last_close) - MIN(first_close))
        / MIN(first_close)) * 100,
        2
    ) AS yearly_return_pct
FROM yearly_prices
GROUP BY
    ticker,
    year
ORDER BY
    year;

-- ============================================
-- 4. RANK YEARS BY PERFORMANCE
-- ============================================

WITH yearly_prices AS (
    SELECT
        s.ticker,
        d.year,

        FIRST_VALUE(f.close_price) OVER (
            PARTITION BY s.ticker, d.year
            ORDER BY d.full_date
        ) AS first_close,

        FIRST_VALUE(f.close_price) OVER (
            PARTITION BY s.ticker, d.year
            ORDER BY d.full_date DESC
        ) AS last_close

    FROM fact_market_price AS f

    JOIN dim_security AS s
        ON f.security_id = s.security_id

    JOIN dim_date AS d
        ON f.date_id = d.date_id
),

yearly_returns AS (
    SELECT
        ticker,
        year,

        ((MIN(last_close) - MIN(first_close))
        / MIN(first_close)) * 100 AS yearly_return_pct

    FROM yearly_prices

    GROUP BY
        ticker,
        year
)

SELECT
    ticker,
    year,

    ROUND(yearly_return_pct, 2)
        AS yearly_return_pct,

    RANK() OVER (
        PARTITION BY ticker
        ORDER BY yearly_return_pct DESC
    ) AS performance_rank

FROM yearly_returns

ORDER BY
    performance_rank;