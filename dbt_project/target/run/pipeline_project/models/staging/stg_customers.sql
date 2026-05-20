
  
    

    create or replace table `miguel-490720`.`miguel_block3`.`stg_customers`
      
    
    

    
    OPTIONS()
    as (
      select distinct
    cast(customer_id as int64) as customer_id,
    cast(country as string) as country
from `miguel-490720`.`miguel_block3`.`raw_customers`
where customer_id is not null
    );
  