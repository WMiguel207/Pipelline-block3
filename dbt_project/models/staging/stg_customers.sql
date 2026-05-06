select distinct
    customer_id,
    'Unknown' as country
from {{ ref('stg_orders') }}
where customer_id is not null