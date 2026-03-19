-- ### jinja macro to create standard set of roles for each database
{% macro create_team_roles(team) %}

    define role {{team}}_DEVELOPER{{env_suffix}};
    define role {{team}}_USAGE{{env_suffix}};

    grant USAGE     on database DCM_DEMO_1{{env_suffix}}        to role {{team}}_USAGE{{env_suffix}};
    grant USAGE     on schema DCM_DEMO_1{{env_suffix}}.{{team}} to role {{team}}_USAGE{{env_suffix}};

    grant CREATE DYNAMIC TABLE, CREATE TABLE, CREATE VIEW on schema DCM_DEMO_1{{env_suffix}}.{{team}} to role {{team}}_DEVELOPER{{env_suffix}};

    grant role {{team}}_USAGE{{env_suffix}}     to role {{team}}_DEVELOPER{{env_suffix}};
    grant role {{team}}_DEVELOPER{{env_suffix}}     to role {{project_owner_role}};
    -- ensure that the DCM still holds all roles it transfers ownership to avoid lock-out

{% endmacro %}
