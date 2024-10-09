CREATE DATABASE IF NOT EXISTS <! database_name | to_snowflake_identifier !>;
CREATE SCHEMA IF NOT EXISTS <! database_name | to_snowflake_identifier !>.<! schema_name | to_snowflake_identifier !>;
USE SCHEMA <! database_name | to_snowflake_identifier !>.<! schema_name | to_snowflake_identifier !>;

CREATE SECRET IF NOT EXISTS <! secret_name | to_snowflake_identifier !> TYPE = GENERIC_STRING SECRET_STRING = 'very_secret_string';

CREATE OR REPLACE NETWORK RULE snowpark_example_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('docs.snowflake.com');

CREATE EXTERNAL ACCESS INTEGRATION IF NOT EXISTS <! external_access_integration_name !>
  ALLOWED_NETWORK_RULES = (snowpark_example_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (<! secret_name | to_snowflake_identifier !>)
  ENABLED = true;
