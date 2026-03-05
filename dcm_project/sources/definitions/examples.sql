define warehouse DCM_DEMO_1_WH{{env_suffix}}
with
    warehouse_size = '{{wh_size}}'
    auto_suspend = 300
    comment = 'For Quickstart Demo of DCM Projects PrPr'
;

define database DCM_DEMO_1{{env_suffix}}
    comment = 'This is a Quickstart Demo for DCM Projects Private Preview';

define schema DCM_DEMO_1{{env_suffix}}.ANALYTICS
    comment = 'For Task copying sample data into landing tables';

define table DCM_DEMO_1{{env_suffix}}.ANALYTICS.ALL_ITEMS(
    ITEM_NAME varchar,
    ITEM_ID varchar,
    ITEM_CATEGORY array
)
change_tracking = TRUE;

define dynamic table DCM_DEMO_1{{env_suffix}}.ANALYTICS.DRINKS
    warehouse = DCM_DEMO_1_WH{{env_suffix}}
    target_lag = '6 hours'
    initialize = 'ON_CREATE'
  as
select
    *
from
    DCM_DEMO_1{{env_suffix}}.ANALYTICS.ALL_ITEMS
where
    ARRAY_CONTAINS('DRINKS'::variant, ITEM_CATEGORY)
;

define role DCM_DEMO_1{{env_suffix}}_READ;

grant USAGE on database DCM_DEMO_1{{env_suffix}} to role DCM_DEMO_1{{env_suffix}}_READ;
grant USAGE on schema DCM_DEMO_1{{env_suffix}}.ANALYTICS to role DCM_DEMO_1{{env_suffix}}_READ;
grant SELECT on ALL tables in database DCM_DEMO_1{{env_suffix}} to role DCM_DEMO_1{{env_suffix}}_READ;
grant SELECT on dynamic table DCM_DEMO_1{{env_suffix}}.ANALYTICS.DRINKS to role DCM_DEMO_1{{env_suffix}}_READ;
