
  
    

    create or replace table `miguel-490720`.`miguel_block3`.`mart_sales`
      
    
    

    
    OPTIONS()
    as (
      select
    o.order_id,
    c.customer_id,
    c.country,
    sum(oi.quantity * oi.price) as total_value
from `miguel-490720`.`miguel_block3`.`int_orders_enriched` o
join `miguel-490720`.`miguel_block3`.`stg_customers` c using (customer_id)
join `miguel-490720`.`miguel_block3`.`stg_order_items` oi using (order_id)
group by 1,2,3
    );
  