
  
    

    create or replace table `miguel-490720`.`miguel_block3`.`stg_order_items`
      
    
    

    
    OPTIONS()
    as (
      select
    order_id,
    1 as quantity,
    100.00 as price
from `miguel-490720`.`miguel_block3`.`stg_orders`
    );
  