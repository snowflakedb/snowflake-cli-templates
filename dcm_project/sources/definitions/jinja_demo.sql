-- loop through lists
{% for team in teams %}
    {% set team_name = team.name | upper %}

    -- inject dictionary values directly into object properties
    define schema DCM_DEMO_1{{env_suffix}}.{{team_name}}
        comment = 'using JINJA dictionary values'
        data_retention_time_in_days = {{ team.data_retention_days }};

    -- Run the macro to create all roles and grants for this schema
{{ create_team_roles(team_name) }}

    define table DCM_DEMO_1{{env_suffix}}.{{team_name}}.PRODUCTS(
        ITEM_NAME varchar,
        ITEM_ID varchar,
        ITEM_CATEGORY array
    );

    -- define conditions
{% if team.add_employees | default(false) %}
        define table DCM_DEMO_1{{env_suffix}}.{{team_name}}.EMPLOYEES(
            NAME varchar,
            ID int
        )
        comment = 'This table is only created in HR'
        ;
{% endif %}
{% endfor %}


-- ### check the jinja_demo file in the PLAN output to see the rendered jinja
