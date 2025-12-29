-- This cleans up the raw product data
SELECT
    ID as product_id,
    TITLE as product_name,
    PRICE as product_price,
    CATEGORY as product_category
FROM RETAIL_DB.RAW_DATA.PRODUCTS