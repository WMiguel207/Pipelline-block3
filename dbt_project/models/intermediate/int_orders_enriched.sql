with ranked as (
    select *,
        row_number() over (
            partition by order_id
            order by order_date desc
        ) as rn
    from {{ ref('stg_orders') }}
)

select *
from ranked
where rn = 1