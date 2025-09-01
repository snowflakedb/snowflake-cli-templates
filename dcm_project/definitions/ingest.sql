define stage DCM_PROJECT_{{db}}.RAW.TASTY_BYTES_ORDERS_STAGE
    comment = 'Internal stage for daily incoming Tasty Bytes order files (CSV)';


define table DCM_PROJECT_{{db}}.RAW.DAILY_ORDERS_INCOMING (
    ORDER_ID NUMBER,
    CUSTOMER_ID NUMBER,
    TRUCK_ID NUMBER,
    ORDER_TS TIMESTAMP_NTZ,
    MENU_ITEM_ID NUMBER,
    QUANTITY NUMBER
)
change_tracking = TRUE
;



define task DCM_PROJECT_{{db}}.ANALYTICS.TSK_INGEST_DAILY_ORDERS
    warehouse = 'DCM_PROJECT_WH_{{db}}'
    schedule = 'USING CRON 0 4 * * * UTC'
as
begin
    -- Copy data from any new files in the stage into our landing table
    copy into
        DCM_PROJECT_{{db}}.RAW.DAILY_ORDERS_INCOMING
    from
        @DCM_PROJECT_{{db}}.RAW.TASTY_BYTES_ORDERS_STAGE
    file_format = (
        TYPE = 'CSV',
        FIELD_DELIMITER = ',',
        SKIP_HEADER = 1,
        NULL_IF = ('NULL', 'null'),
        EMPTY_FIELD_AS_NULL = true,
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    )
    ON_ERROR = 'CONTINUE';

    -- Insert new order headers, avoiding duplicates
    insert into
        DCM_PROJECT_{{db}}.RAW.ORDER_HEADER (ORDER_ID, CUSTOMER_ID, TRUCK_ID, ORDER_TS)
    select
        distinct ORDER_ID,
        CUSTOMER_ID,
        TRUCK_ID,
        ORDER_TS
    from
        DCM_PROJECT_{{db}}.RAW.DAILY_ORDERS_INCOMING src
    where not exists (
        select
            1
        from
            DCM_PROJECT_{{db}}.RAW.ORDER_HEADER dest
        where
            dest.ORDER_ID = src.ORDER_ID
    );

    -- Insert new order details
    insert into
        DCM_PROJECT_{{db}}.RAW.ORDER_DETAIL (ORDER_ID, MENU_ITEM_ID, QUANTITY)
    select
        ORDER_ID, MENU_ITEM_ID, QUANTITY
    from
        DCM_PROJECT_{{db}}.RAW.DAILY_ORDERS_INCOMING;

    -- Clean up the landing table for the next run
    truncate table DCM_PROJECT_{{db}}.RAW.DAILY_ORDERS_INCOMING;

    -- Remove the processed files from the stage to prevent re-loading
    remove @DCM_PROJECT_{{db}}.RAW.TASTY_BYTES_ORDERS_STAGE pattern='.*.csv';
end;
