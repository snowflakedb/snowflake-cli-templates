-- loop through lists
{% for team in teams %}
    {% set team = team | upper %}

    define schema DCM_DEMO_1{{env_suffix}}.{{team}}
        comment = 'using JINJA FILTER for upper';

    -- Run the macro to create all roles and grants for this schema
{{ create_team_roles(team) }}

    define table DCM_DEMO_1{{env_suffix}}.{{team}}.PRODUCTS(
        ITEM_NAME varchar,
        ITEM_ID varchar,
        ITEM_CATEGORY array
    );

    -- define conditions
{% if team == 'HR' %}
        define table DCM_DEMO_1{{env_suffix}}.{{team}}.EMPLOYEES(
            NAME varchar,
            ID int
        )
        comment = 'This table is only created in HR'
        ;
{% endif %}
{% endfor %}


-- ### check the jinja_demo file in the PLAN output to see the rendered jinja
