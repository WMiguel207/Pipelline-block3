
  
    

    create or replace table `miguel-490720`.`miguel_block3`.`int_orders_enriched`
      
    
    

    
    OPTIONS()
    as (
      with ranked as (
    select *,
        row_number() over (
            partition by order_id
            order by order_date desc
        ) as rn
    from `miguel-490720`.`miguel_block3`.`stg_orders`
)

select *
from ranked
where rn = 1
    );
  