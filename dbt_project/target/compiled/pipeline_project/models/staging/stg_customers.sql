select distinct
    customer_id,
    'Unknown' as country
from `miguel-490720`.`miguel_block3`.`stg_orders`
where customer_id is not null