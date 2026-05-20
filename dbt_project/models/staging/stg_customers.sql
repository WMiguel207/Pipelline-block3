select distinct
    cast(customer_id as int64) as customer_id,
    cast(country as string) as country
from {{ source('raw', 'raw_customers') }}
where customer_id is not null
