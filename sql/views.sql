-- ============================================
-- MARKET PRICE ANALYTICAL VIEW
-- ============================================

CREATE OR REPLACE VIEW vw_market_prices AS

SELECT
    s.ticker,
    d.full_date,
    d.year,
    d.month,
    d.day,

    f.open_price,
    f.high_price,
    f.low_price,
    f.close_price,
    f.adj_close,
    f.volume,

    f.daily_return,
    f.ma_7,
    f.ma_30

FROM fact_market_price AS f

JOIN dim_security AS s
    ON f.security_id = s.security_id

JOIN dim_date AS d
    ON f.date_id = d.date_id;