# DCM Project template

## Introduction

You can use this template as a starter project for a Snowflake DCM Project.

DCM Projects enable declarative infrastructure management, presenting a less error-prone paradigm
that integrates better with Git than imperative approaches. Through automated change detection, DCM
Projects keep the Snowflake environment synchronized with the definition files from different supported
sources (SnowGIT repositories, Workspaces, Stages). DCM Projects automatically create new objects,
modify existing objects, and delete objects that are no longer needed, which supports CI/CD best
practices when working with Snowflake environments.

## Directory Structure

```
  <project_name> (7)
        ├── sources
        │   ├── definitions (2)
        │   │   ├────── examples.sql (4)
        │   │   ├────── jinja_demo.sql (5)
        │   │   └────── [...]
        │   └── macros (3)
        │       ├────── grants_macro.sql (6)
        │       └────── [...]
        └── manifest.yml (1)
```

1. [manifest.yml][manifest] - is the file that defines:
   * `templating` - the settings for Jinja templating:
      * `defaults` specifying the default values for template variables. They can be provided here as a series of key-value entries (dictionary), mapping the template variable name to its value. e.g. `example_db_name: "db_default"`.
      * `configurations` that group template variables and override their defaults. Configurations can be specified here as a series of key-value entries (dictionary), where the key is a case-insensitive configuration name, and the value is a series of key-value entries, mapping the template variable name to its value. Each configuration contains a set of key-value pairs, e.g. `example_db_name: "db_dev"`.
   * `targets` - targets specifying targeted account, project object names, templating config
      * `project_name` - the name of the DCM Project to use in Snowflake. It can be either a simple name or a fully qualified name, including the database and schema names. If the fully qualified project name is provided, its database and schema take precedence over the configured connection.
      * `templating_config` - the templating configuration name to use. It should refer to a configuration name specified in the `templating.configurations` section.
      * `account_identifier` - the account identifier to use
2. `definitions` - is the directory for all .sql files containing project entity definitions. You can use an arbitrarily nested directory structure.
3. `macros` - is the directory for all .sql files containing project macros. You can use an arbitrarily nested directory structure.
4. [examples.sql][examples.sql] - this is the file that contains some example definitions of project entities. You define particular entities with a `DEFINE` keyword which behaves similar to `CREATE OR ALTER`, e.g. `DEFINE DATABASE d1 COMMENT = 'some comment'`. Removing a `DEFINE` statement results in the entity being dropped.
5. [jinja_demo.sql][jinja_demo.sql] - this is the file that contains some example definitions focusing on demoing some Jinja capabilities, like using loops and macros
6. [grants_macro.sql][grants_macro.sql] - this is the file that contains a sample Jinja macro granting privileges
6. `<project_name>` - is the repository project folder.

### How to organize the definition files structure

Once you initialize a project from the template, you create the definitions that will set up your
account. The template doesn't impose any file structure of definition files, but keep in mind that you
don't need to keep all definition statements in a single file. You can organize the code in multiple
files divided into different directories, such as single object type per file. The following
example uses a more complex file structure:

```
<repo-project-folder>
      ├── sources
      │   ├── definitions
      │   │   ├────── wh_db_roles.sql
      │   │   ├────── load
      │   │   ├────── transform
      │   │   └────── serve
      │   │           ├────── dashboard_views.sql
      │   │           ├────── annual_agg.sql
      │   │           └────── team_metrics.sql
      │   └── macros
      │       ├────── grants.sql
      │       └────── users.sql
      └── manifest.yml
```

## Working on DCM Projects with Snowflake CLI

### 1. Initialize a DCM Project from the template

To initialize a new DCM Project from this template, execute the following command and provide the
data required in the command prompts. This command creates a new directory with DCM Project files.
Replace `<project_dir_name>` with the desired name for the project directory.

```bash
snow init <project_dir_name> --template dcm_project
```

example usage:

```bash
snow init my_project --template dcm_project
```

The `init` command does not create any Snowflake object. It only bootstraps the local project.

### 2. Define entities in `.sql` files

In this step, you define the entities you want the DCM Project to manage. You can define these entities in the prepared `sources/definitions/*.sql` files, but you can also create your own .sql files in the `sources/definitions` folder or any subfolder.

An example content of the definition file:
```sql
DEFINE ROLE role1;
DEFINE DATABASE ROLE role2;

DEFINE DATABASE db1;
DEFINE DATABASE db2;

DEFINE SCHEMA db1.sch1;
DEFINE SCHEMA db2.sch2;

DEFINE TABLE db1.sch1.tb1 (col_1 integer, col_2 varchar);
DEFINE TABLE db2.sch2.tb2 (col_3 integer, col_4 varchar);
```

### 3. Create the DCM Project

After entity definitions included in definition files are ready to be applied to your infrastructure,
you must create a DCM Project in Snowflake. You can perform this operation by executing the command below:

```bash
snow dcm create
```

The DCM Project will be created in the current session's database and schema or in those specified in the flags of the `snow` command.
If the fully qualified project name is provided, its database and schema take precedence.

### 4. DCM Plan

After creating a new DCM Project, you can validate what changes will be applied to your Snowflake
account with this command. It will perform all the same validations and consistency checks
like a regular `snow dcm deploy`, but will not persist any changes to your Snowflake account objects.

```bash
snow dcm plan
```

### 5. Deploy DCM Project

In order to apply changes to your Snowflake account, you need to deploy the current definition the DCM Project. It is recommended to first run `snow dcm plan` and review the changeset. If it looks good, you can deploy the changes
with the following command:

```bash
snow dcm deploy
```

[manifest]: ./manifest.yml
[examples.sql]: ./sources/definitions/examples.sql
[jinja_demo.sql]: ./sources/definitions/jinja_demo.sql
[grants_macro.sql]: ./sources/macros/grants_macro.sql
[template]: ./template.yml
[workspaces_docs]: https://docs.snowflake.com/en/user-guide/ui-snowsight/workspaces
[stages_docs]: https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage
[snowgit_docs]: https://docs.snowflake.com/en/developer-guide/git/git-overview
