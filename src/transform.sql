DROP TABLE IF EXISTS clean_superstore CASCADE;
CREATE TABLE clean_superstore AS
SELECT
    "Row ID" AS row_id,
    TRIM("Order ID") AS order_id,
    TRIM("Order Priority") AS order_priority,
    TRIM("Customer ID") AS customer_id,
    TRIM("Customer Name") AS customer_name,
    TRIM("Segment") AS segment,
    TRIM("City") AS city,
    TRIM("State") AS state,
    TRIM("Country") AS country,
    TRIM("Region") AS region,
    TRIM("Market") AS market,
    TRIM("Market2") AS market_group,
    TRIM("Product ID") AS product_id,
    TRIM("Product Name") AS product_name,
    TRIM("Category") AS category,
    TRIM("Sub-Category") AS sub_category,
    "Sales" AS sales,
    "Quantity" AS quantity,
    "Discount" AS discount,
    "Profit" AS profit,
    "Shipping Cost" AS shipping_cost,
    TRIM("Ship Mode") AS ship_mode,
    "Year" AS order_year,
    "weeknum" AS order_weeknum,

    (MAKE_DATE("Year"::int, 1, 1) + ("weeknum"::int -1) * INTERVAL '7 days')::date AS order_date_approx
    FROM raw_superstore;