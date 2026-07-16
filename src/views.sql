CREATE OR REPLACE VIEW v_sales_by_region AS
SELECT market, market_group, region, 
 COUNT(DISTINCT order_id) AS order_count,
 SUM(quantity) AS units_sold,
 SUM(sales) AS total_sales,
 ROUND(SUM(profit)::numeric,2) AS total_profit,
 ROUND(AVG(discount)::numeric,3) AS avg_discount
FROM clean_superstore
GROUP BY market, market_group, region;


CREATE OR REPLACE VIEW v_monthly_trend AS
SELECT
    DATE_TRUNC('month', order_date_approx)::date AS order_month,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(sales) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit
FROM clean_superstore
GROUP BY DATE_TRUNC('month', order_date_approx)
ORDER BY order_month;


CREATE OR REPLACE VIEW v_product_performance AS
SELECT category, sub_category,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS units_sold,
    SUM(sales) AS total_sales,
    ROUND(SUM(profit)::numeric, 2)    AS total_profit,
    CASE
        WHEN SUM(profit) < 0 THEN 'LOSS-MAKING'
        ELSE 'PROFITABLE'
    END   AS profitability_flag
FROM clean_superstore
GROUP BY category, sub_category;

CREATE OR REPLACE VIEW v_segment_summary AS
SELECT segment, market_group,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(DISTINCT order_id)  AS order_count,
    SUM(sales)  AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit
FROM clean_superstore
GROUP BY segment, market_group;