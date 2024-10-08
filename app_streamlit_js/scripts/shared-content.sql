-- An example script to share your data with consumer --

-- Scenario: You want to create an application package which is able to access some data that resides in a different database in your account.
-- Let this database be called past_add_transactions, with a schema called core, and a table in the schema called transactions.

-- To share past_add_transactions.core.transactions with your application package, we recommend carrying out the following steps:
-- 1. Create a view over the table past_add_transactions.core.transactions that can be shared with the application package, such as past_add_transactions.core.transactions_v;
-- 2. Grant reference_usage on database past_add_transactions to share in application package;
-- 3. Grant usage on schema past_add_transactions.core to share in the application package;
-- 4. Grant select/any required privilege on the view past_add_transactions.core.transactions_v to share in application package;

-- For more information, refer to https://docs.snowflake.com/en/developer-guide/native-apps/preparing-data-content
