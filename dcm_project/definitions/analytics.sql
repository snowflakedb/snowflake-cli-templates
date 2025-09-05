define schema DCM_PROJECT_{{db}}.ANALYTICS;

define dynamic table DCM_PROJECT_{{db}}.ANALYTICS.V_ENRICHED_ORDER_DETAILS
warehouse = DCM_PROJECT_WH_{{db}}
target_lag = '12 hours'
as
select
    oh.ORDER_ID,
    oh.ORDER_TS,
    od.QUANTITY,
    m.MENU_ITEM_NAME,
    m.ITEM_CATEGORY,
    m.SALE_PRICE_USD,
    m.COST_OF_GOODS_USD,
    (od.QUANTITY * m.SALE_PRICE_USD) as LINE_ITEM_REVENUE,
    (od.QUANTITY * (m.SALE_PRICE_USD - m.COST_OF_GOODS_USD)) as LINE_ITEM_PROFIT,
    c.CUSTOMER_ID,
    c.FIRST_NAME,
    c.LAST_NAME,
    c.CITY as CUSTOMER_CITY,
    t.TRUCK_ID,
    t.TRUCK_BRAND_NAME
from
    DCM_PROJECT_{{db}}.RAW.ORDER_HEADER oh
join
    DCM_PROJECT_{{db}}.RAW.ORDER_DETAIL od
    on oh.ORDER_ID = od.ORDER_ID
join
    DCM_PROJECT_{{db}}.RAW.MENU m
    on od.MENU_ITEM_ID = m.MENU_ITEM_ID
join
    DCM_PROJECT_{{db}}.RAW.CUSTOMER c
    on oh.CUSTOMER_ID = c.CUSTOMER_ID
join
    DCM_PROJECT_{{db}}.RAW.TRUCK t
    on oh.TRUCK_ID = t.TRUCK_ID
;


define dynamic table DCM_PROJECT_{{db}}.ANALYTICS.V_MENU_ITEM_POPULARITY
warehouse = DCM_PROJECT_WH_{{db}}
target_lag = '12 hours'
as
select
    MENU_ITEM_NAME,
    ITEM_CATEGORY,
    count(DISTINCT ORDER_ID) as NUMBER_OF_ORDERS,
    sum(QUANTITY) as TOTAL_QUANTITY_SOLD,
    sum(LINE_ITEM_REVENUE) as TOTAL_REVENUE
from
    DCM_PROJECT_{{db}}.ANALYTICS.V_ENRICHED_ORDER_DETAILS
group by
    MENU_ITEM_NAME, ITEM_CATEGORY
order by
    TOTAL_REVENUE desc
;


define dynamic table DCM_PROJECT_{{db}}.ANALYTICS.V_CUSTOMER_SPENDING_SUMMARY
warehouse = DCM_PROJECT_WH_{{db}}
target_lag = '12 hours'
as
select
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    CUSTOMER_CITY,
    count(DISTINCT ORDER_ID) as TOTAL_ORDERS,
    sum(LINE_ITEM_REVENUE) as TOTAL_SPEND_USD,
    min(ORDER_TS) as FIRST_ORDER_DATE,
    max(ORDER_TS) as LATEST_ORDER_DATE
from
    DCM_PROJECT_{{db}}.ANALYTICS.V_ENRICHED_ORDER_DETAILS
group by
    CUSTOMER_ID, FIRST_NAME, LAST_NAME, CUSTOMER_CITY
order by
    TOTAL_SPEND_USD desc
;


define dynamic table DCM_PROJECT_{{db}}.ANALYTICS.V_TRUCK_PERFORMANCE
warehouse = DCM_PROJECT_WH_{{db}}
target_lag = '12 hours'
as
select
    TRUCK_BRAND_NAME,
    count(DISTINCT ORDER_ID) as TOTAL_ORDERS,
    sum(LINE_ITEM_REVENUE) as TOTAL_REVENUE,
    sum(LINE_ITEM_PROFIT) as TOTAL_PROFIT
from
    DCM_PROJECT_{{db}}.ANALYTICS.V_ENRICHED_ORDER_DETAILS
group by
    TRUCK_BRAND_NAME
order by
    TOTAL_REVENUE desc
;
