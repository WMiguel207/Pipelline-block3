select
    o.order_id,
    c.customer_id,
    c.country,
    sum(oi.quantity * oi.price) as total_value
from {{ ref('int_orders_enriched') }} o
join {{ ref('stg_customers') }} c using (customer_id)
join {{ ref('stg_order_items') }} oi using (order_id)
group by 1,2,3