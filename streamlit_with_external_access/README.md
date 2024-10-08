# Streamlit application with external access

This is a simple example of a Streamlit application that requires external access.

## Prerequisites
This project requires a database, API integration and secret. To created them you can execute convenience script
`snow sql -f setup.sql` or run the following SQL commands:

```sql
CREATE DATABASE IF NOT EXISTS <! database_name | to_snowflake_identifier !>;
CREATE SCHEMA IF NOT EXISTS <! database_name | to_snowflake_identifier !>.<! schema_name | to_snowflake_identifier !>;
USE SCHEMA <! database_name | to_snowflake_identifier !>.<! schema_name | to_snowflake_identifier !>;

CREATE SECRET IF NOT EXISTS <! secret_name | to_snowflake_identifier !> TYPE = GENERIC_STRING SECRET_STRING = 'very_secret_string';

CREATE OR REPLACE NETWORK RULE streamlit_example_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('docs.snowflake.com');

CREATE EXTERNAL ACCESS INTEGRATION IF NOT EXISTS <! external_access_integration_name !>
  ALLOWED_NETWORK_RULES = (streamlit_example_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (<! secret_name | to_snowflake_identifier !>)
  ENABLED = true;
```

## Deploying the streamlit application
_For more information see [deploy documentation](https://docs.snowflake.com/developer-guide/snowflake-cli/streamlit-apps/manage-apps/deploy-app)._

To deploy the Streamlit application, you should run:

```bash
snow streamlit deploy
```
