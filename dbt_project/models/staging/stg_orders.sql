select
    cast(order_id as int64) as order_id,
    cast(customer_id as int64) as customer_id,
    status,
    cast(order_date as timestamp) as order_date
from {{ source('raw', 'raw_orders') }}