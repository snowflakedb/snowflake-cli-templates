define stage DCM_PROJECT_{{db}}.RAW.TASTY_BYTES_ORDERS_STAGE
    comment = 'Internal stage for daily incoming Tasty Bytes order files (CSV)';


define table DCM_PROJECT_{{db}}.RAW.DAILY_ORDERS_INCOMING (
    ORDER_ID number,
    CUSTOMER_ID number,
    TRUCK_ID number,
    ORDER_TS TIMESTAMP_NTZ,
    MENU_ITEM_ID number,
    QUANTITY number
)
change_tracking = true
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
        type = 'CSV',
        field_delimiter = ',',
        skip_header = 1,
        null_if = ('NULL', 'null'),
        empty_field_as_null = true,
        field_optionally_enclosed_by = '"'
    )
    on_error = 'CONTINUE';

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
