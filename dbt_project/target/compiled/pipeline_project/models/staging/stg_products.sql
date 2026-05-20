select
    cast(product_id as int64) as product_id,
    cast(product_name as string) as product_name,
    cast(category as string) as category
from `miguel-490720`.`miguel_block3`.`raw_products`
where product_id is not null