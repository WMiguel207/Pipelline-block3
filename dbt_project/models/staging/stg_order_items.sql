select
    order_id,
    1 as quantity,
    100.00 as price
from {{ ref('stg_orders') }}