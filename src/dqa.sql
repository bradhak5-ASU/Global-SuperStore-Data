SELECT "Order Date", COUNT(*) AS row_count
FROM raw_superstore
GROUP BY "Order Date";

SELECT "Ship Date", COUNT(*) AS row_count
FROM raw_superstore
GROUP BY "Ship Date";

SELECT
    MIN("Year") AS min_year,
    MAX("Year") AS max_year,
    MIN("weeknum") AS min_week,
    MAX("weeknum") AS max_week
FROM raw_superstore;

SELECT "ji_lu-shu", COUNT(*) AS row_count
FROM raw_superstore
GROUP BY "ji_lu-shu";

SELECT "Market", "Market2", COUNT(*) AS row_count
FROM raw_superstore
GROUP BY "Market", "Market2"
ORDER BY "Market";

SELECT COUNT(*) AS mismatched_rows
FROM raw_superstore
WHERE SPLIT_PART("Order ID", '-', 2) <> "Year"::text;

SELECT COUNT(*) AS total_rows, COUNT(DISTINCT "Row ID")  AS distinct_row_ids
FROM raw_superstore;