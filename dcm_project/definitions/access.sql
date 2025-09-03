define warehouse DCM_PROJECT_WH_{{db}}
with
    warehouse_size = '{{wh_size}}'
    auto_suspend = 5
    comment = 'For Quickstart Demo of DCM Projects PrPr'
;

define role DCM_PROJECT_{{role}}_READ;
grant role DCM_PROJECT_{{role}}_READ to user JSOMMERFELD;   -- replace with your user


grant USAGE on database DCM_PROJECT_{{db}}         to role DCM_PROJECT_{{role}}_READ;

grant usage on schema DCM_PROJECT_{{db}}.RAW       to role DCM_PROJECT_{{role}}_READ;
grant usage on schema DCM_PROJECT_{{db}}.ANALYTICS to role DCM_PROJECT_{{role}}_READ;
grant usage on schema DCM_PROJECT_{{db}}.SERVE     to role DCM_PROJECT_{{role}}_READ;
grant usage on warehouse DCM_PROJECT_WH_{{db}}     to role DCM_PROJECT_{{role}}_READ;


grant select on all tables in database DCM_PROJECT_{{db}}    to role DCM_PROJECT_{{role}}_READ;

--grant SELECT on ALL dynamic tables in database DCM_PROJECT_{{db}}    to role DCM_PROJECT_{{role}}_READ;
-- //awaiting bug fix to roll out

grant select on all views in database DCM_PROJECT_{{db}}    to role DCM_PROJECT_{{role}}_READ;
