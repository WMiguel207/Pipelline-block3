select
    cast(order_id as int64) as order_id,
    cast(customer_id as int64) as customer_id,
    cast(status as string) as status,
    cast(order_date as timestamp) as order_date,
    cast(total_amount as numeric) as total_amount,
    cast(shipping_country as string) as shipping_country
from {{ source('raw', 'raw_orders') }}
