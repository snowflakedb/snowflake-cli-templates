define database {{ example_db_name }};

define schema {{ example_db_name }}.sch1 COMMENT = 'some comment';

define table {{ example_db_name }}.sch1.tab1 ( {{ example_column_name }} integer, col_2 varchar);

define stage  {{ example_db_name }}.sch1.stg1 COMMENT = 'another comment';
