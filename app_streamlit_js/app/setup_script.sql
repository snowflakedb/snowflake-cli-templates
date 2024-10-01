-- This is the setup script that runs while installing a Snowflake Native App in a consumer account.
-- For more information on how to create setup file, visit https://docs.snowflake.com/en/developer-guide/native-apps/creating-setup-script

-- A general guideline to building this script looks like:
-- 1. Create application roles
CREATE APPLICATION ROLE IF NOT EXISTS app_public;

-- 2. Create a versioned schema to hold those UDFs/Stored Procedures
CREATE OR ALTER VERSIONED SCHEMA core;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;

-- 3. Create UDFs and Stored Procedures using the JavaScript handler.
CREATE or REPLACE FUNCTION core.add(NUM1 DOUBLE, NUM2 DOUBLE)
  RETURNS DOUBLE
  LANGUAGE JAVASCRIPT
  AS 'return NUM1 + NUM2;';

-- 4. Grant appropriate privileges over these objects to your application roles.
GRANT USAGE ON FUNCTION core.add(DOUBLE, DOUBLE) TO APPLICATION ROLE app_public;

-- 5. Create a streamlit object using the code you wrote in you wrote in src/module-ui, as shown below.
-- The `from` value is derived from the stage path described in snowflake.yml
CREATE OR REPLACE STREAMLIT core.ui
     FROM '/streamlit/'
     MAIN_FILE = 'ui.py';


-- 6. Grant appropriate privileges over these objects to your application roles.
GRANT USAGE ON STREAMLIT core.ui TO APPLICATION ROLE app_public;

-- A detailed explanation can be found at https://docs.snowflake.com/en/developer-guide/native-apps/adding-streamlit
