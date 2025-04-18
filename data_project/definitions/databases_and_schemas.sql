-- SCHEMAS:
define schema {{ base_db_name }}_{{ env }}.tables
    comment = 'This schema is dedicated to tables.';

define schema {{ base_db_name }}_{{ env }}.views
    comment = 'This schema is dedicated to views.';

define schema {{ base_db_name }}_{{ env }}.tasks
    comment = 'This schema is dedicated to tasks.';

-- DATABASES:
    -- NOTE: The project is figuring out the statement execution order by itself, so you don't
    -- need to care of the statements order. The below statements will be executed before statements
    -- above that define schemas. This mechanism also applies to other entities like parent/child tasks etc.
define database {{ base_db_name }}_{{ env }}
    log_level = 'INFO'
    trace_level = 'PROPAGATE'
    data_retention_time_in_days = 1
    max_data_extension_time_in_days = 3
    comment = 'This is the base database for all objects managed by the project.';
