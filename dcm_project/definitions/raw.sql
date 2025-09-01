define database DCM_PROJECT_{{db}}
    comment = 'This is a Quickstart Demo for DCM Projects Private Preview';

define schema DCM_PROJECT_{{db}}.RAW;


define table DCM_PROJECT_{{db}}.RAW.ALL_ITEMS(
    ITEM_NAME varchar,
    ITEM_ID varchar,
    ITEM_CATEGORY array
)
change_tracking = TRUE;


define table DCM_PROJECT_{{db}}.RAW.ALL_REGIONS(
    REGION varchar,
    REGION_ID number,
    COUNTRY varchar,
    CATEGORIES array,
    ONLINE boolean
)
change_tracking = TRUE;


define table DCM_PROJECT_{{db}}.RAW.INVENTORY(
    ITEM_ID number,
    REGION_ID number,
    IN_STOCK number,
    COUNTED_ON date
)
change_tracking = TRUE;



define table DCM_PROJECT_{{db}}.RAW.MENU (
    MENU_ITEM_ID NUMBER,
    MENU_ITEM_NAME VARCHAR,
    ITEM_CATEGORY VARCHAR,
    COST_OF_GOODS_USD NUMBER(10, 2),
    SALE_PRICE_USD NUMBER(10, 2)
)
change_tracking = TRUE;

define table DCM_PROJECT_{{db}}.RAW.TRUCK (
    TRUCK_ID NUMBER,
    TRUCK_BRAND_NAME VARCHAR,
    MENU_TYPE VARCHAR
)
change_tracking = TRUE;

define table DCM_PROJECT_{{db}}.RAW.CUSTOMER (
    CUSTOMER_ID NUMBER,
    FIRST_NAME VARCHAR,
    LAST_NAME VARCHAR,
    CITY VARCHAR
)
change_tracking = TRUE;

define table DCM_PROJECT_{{db}}.RAW.ORDER_HEADER (
    ORDER_ID NUMBER,
    CUSTOMER_ID NUMBER,
    TRUCK_ID NUMBER,
    ORDER_TS TIMESTAMP_NTZ -- Using a timezone-neutral timestamp
)
change_tracking = TRUE
;

define table DCM_PROJECT_{{db}}.RAW.ORDER_DETAIL (
    ORDER_ID NUMBER,
    MENU_ITEM_ID NUMBER,
    QUANTITY NUMBER
)
change_tracking = TRUE;
