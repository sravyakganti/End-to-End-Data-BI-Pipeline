-- This flattens the list of products inside every order
with raw_orders as (
    select * from RETAIL_DB.RAW_DATA.ORDERS
)

select
    o.ID as order_id,
    o.USERID as customer_id,
    p.value:id::integer as product_id,
    p.value:quantity::integer as quantity
from raw_orders o,
lateral flatten(input => o.PRODUCTS) p