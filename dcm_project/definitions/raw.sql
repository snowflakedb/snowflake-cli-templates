define database DCM_PROJECT_{{db}}
    comment = 'This is a Quickstart Demo for DCM Projects Private Preview';

define schema DCM_PROJECT_{{db}}.RAW;


define table DCM_PROJECT_{{db}}.RAW.ALL_ITEMS(
    ITEM_NAME varchar,
    ITEM_ID varchar,
    ITEM_CATEGORY array
)
change_tracking = true;


define table DCM_PROJECT_{{db}}.RAW.ALL_REGIONS(
    REGION varchar,
    REGION_ID number,
    COUNTRY varchar,
    CATEGORIES array,
    ONLINE boolean
)
change_tracking = true;


define table DCM_PROJECT_{{db}}.RAW.INVENTORY(
    ITEM_ID number,
    REGION_ID number,
    IN_STOCK number,
    COUNTED_ON date
)
change_tracking = true;



define table DCM_PROJECT_{{db}}.RAW.MENU (
    MENU_ITEM_ID number,
    MENU_ITEM_NAME varchar,
    ITEM_CATEGORY varchar,
    COST_OF_GOODS_USD number(10, 2),
    SALE_PRICE_USD number(10, 2)
)
change_tracking = true;

define table DCM_PROJECT_{{db}}.RAW.TRUCK (
    TRUCK_ID number,
    TRUCK_BRAND_NAME varchar,
    MENU_TYPE varchar
)
change_tracking = true;

define table DCM_PROJECT_{{db}}.RAW.CUSTOMER (
    CUSTOMER_ID number,
    FIRST_NAME varchar,
    LAST_NAME varchar,
    CITY varchar
)
change_tracking = true;

define table DCM_PROJECT_{{db}}.RAW.ORDER_HEADER (
    ORDER_ID number,
    CUSTOMER_ID number,
    TRUCK_ID number,
    ORDER_TS timestamp_ntz -- Using a timezone-neutral timestamp
)
change_tracking = true
;

define table DCM_PROJECT_{{db}}.RAW.ORDER_DETAIL (
    ORDER_ID number,
    MENU_ITEM_ID number,
    QUANTITY number
)
change_tracking = true;
