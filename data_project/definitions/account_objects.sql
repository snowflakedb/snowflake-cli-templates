-- ROLES:
define role TABLE_MANAGER
    comment = 'This role is allowed to manage tables.';

define role TASK_MANAGER
    comment = 'This role is allowed to manage tasks.';

define role WAREHOUSE_MANAGER
    comment = 'This role is allowed to manage warehouses.';

-- WAREHOUSES:
define warehouse PARENT_TASK_WH warehouse_size='large';

define warehouse CHILD_TASK_WH warehouse_size='small';

-- TAGS:
define tag VISIBILITY
    allowed_values 'private', 'public';
