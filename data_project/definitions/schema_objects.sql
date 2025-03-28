-- TABLES:
define table {{ base_db_name }}_{{ env }}.TABLES.SOURCE_TABLE
    (num_value int, timestamp timestamp_ntz default current_timestamp())
    with tag (VISIBILITY = 'private')
    max_data_extension_time_in_days = 8
    data_retention_time_in_days = 1
    enable_schema_evolution = false
    change_tracking = false
    comment = 'This is the table that is powered by the data from outside.';

define table {{ base_db_name }}_{{ env }}.TABLES.TARGET_TABLE
    (a int, timestamp timestamp_ntz default current_timestamp())
    with tag (VISIBILITY = 'private')
    change_tracking = true
    comment = 'This is the table that is powered by the data from {{ base_db_name }}_{{ env }}.tables.source_table.';

-- VIEWS:
define view {{ base_db_name }}_{{ env }}.VIEWS.RESULTS
    with tag (VISIBILITY = 'public')
    comment = 'This view returns only values divisible by 3.'
    as
       select (num_value, timestamp) from {{ base_db_name }}_{{ env }}.TABLES.SOURCE_TABLE
            where 1=1
                and mod(num_value, 3) = 0;

-- TASKS:
define task {{ base_db_name }}_{{ env }}.TASKS.DATA_GENERATOR
    with tag (VISIBILITY = 'private')
    warehouse = CHILD_TASK_WH
    finalize = {{ base_db_name }}_{{ env }}.TASKS.DATA_PROCESSOR
    AS
        insert into {{ base_db_name }}_{{ env }}.TABLES.SOURCE_TABLE (num_value)
            values ((select count(*) from {{ base_db_name }}_{{ env }}.TABLES.SOURCE_TABLE));

define task {{ base_db_name }}_{{ env }}.TASKS.DATA_PROCESSOR
    with tag (VISIBILITY = 'private')
    warehouse = PARENT_TASK_WH
    schedule = '1 MINUTE'
    AS
        insert into {{ base_db_name }}_{{ env }}.TABLES.TARGET_TABLE (num_value)
            select (num_value) FROM {{ base_db_name }}_{{ env }}.TABLES.SOURCE_TABLE;
