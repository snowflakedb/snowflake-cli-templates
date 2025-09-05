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
<project_name> (4)
      ├── definitions (2)
      │   ├────── access.sql
      │   ├────── ingest.sql
      │   ├────── raw.sql (3)
      │   ├────── serve.sql
      │   └────── [...]
      └── manifest.yml (1)
```

1. [manifest.yml][manifest] - is the file that defines:
    * what files should be included in the project definition. In the `include_definitions` list, you can pass items that are Java regex patterns. The default value is `- definitions/.*`, meaning that all files in the `definitions` folder and its subfolders will be included.
    * configurations that group template variables with their default values. Configurations can be specified here as a series of key-value entries, where the key is a case-insensitive configuration name, and the value is a series of key-value entries, mapping the template variable name to its value. Each configuration contains a set of key-value pairs, e.g. `example_db_name: "db1"`.
2. `definitions` - is the default directory as defined in the [manifest.yml][manifest] for all .sql files containing project entity definitions. You can use an arbitrarily nested directory structure.
3. [raw.sql][raw.sql] - this is the file that contains some example definitions of project entities. You define particular entities with a `DEFINE` keyword which behaves similar to `CREATE OR ALTER`, e.g. `DEFINE DATABASE d1 COMMENT = 'some comment'`. Removing a `DEFINE` statement results in the entity being dropped.
4. `<project_name>` - is the repository project folder.

### How to organize definition files structure

Once you initialize a project from the template, you create the definitions that will set up your
account. The template doesn't impose any file structure of definition files, but keep in mind that you
don't need to keep all definition statements in a single file. You can organize the code in multiple
files divided into different directories, such as single object type per file. The following
example uses a more complex file structure:

```
<repo-project-folder>
      ├── definitions
      │   ├────── wh_db_roles.sql
      │   ├────── load
      │   ├────── transform
      │   └────── serve
      │           ├────── dashboard_views.sql
      │           ├────── annual_agg.sql
      │           └────── team_metrics.sql
      └── manifest.yml
```

You must include all files from the `definitions` directory in the `manifest.yaml` file:

```yaml
manifest_version: 1.0

include_definitions:
  - definitions/.*
```

## Working on DCM Projects with Snowflake CLI

### 1. Initialize a DCM Project from the template

To initialize a new DCM Project from this template, execute the following command and provide the
data required in command prompts. This command creates a new directory with DCM Project files.
Replace `<project_dir_name>` with the desired name for the project directory.

```bash
snow init <project_dir_name> --template dcm_project
```

example usage:

```bash
snow init MY_PROJECT --template dcm_project
```

### 2. Define entities in `.sql` files

In this step, you define the entities you want the DCM Project to manage. You can define these entities
in the prepared `definitions/*.sql` files, but you can also create your own files. If you
decide to add more `.sql` files, make sure that they will be included in the DCM Project execution process
by adding their paths to `include_definitions` list in the [manifest.yaml][manifest] file.

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
you must create a DCM Project. You can perform this operation by executing the command below:

```bash
snow dcm create EXAMPLE_PROJECT
```

The DCM Project will be created in the current sessions'
database and schema or in these, which are specified in the flags of `snow` command.

### 4. DCM Plan

After creating a new DCM Project, you can validate what changes will be applied to your Snowflake
account with this command. It will perform all the same validations and consistency checks
like a regular `snow dcm deploy`, but will not persist any changes to your Snowflake account objects.

```bash
snow dcm plan <project_identifier> --configuration <config_name>
```

example usage:

```bash
snow dcm plan EXAMPLE_PROJECT --configuration "PROD"
```

#### DCM Plan from prepared project files in Snowflake storage

Alternatively if you synchronize your project files with a [SNOWGIT REPOSITORY][snowgit_docs], develop
the DCM Project with [a WORKSPACE][workspaces_docs], or simply you have your project files prepared in
a [USER STAGE][stages_docs], you can specify the source storage with `--from` option, from which you
would like to use the project files for DCM Project `PLAN` commands.

```bash
snow dcm plan <project_name> --from <source_stage_name> --configuration <config_name>
```

example usage:

```bash
snow dcm plan EXAMPLE_PROJECT --from "@DB.SCH.SOURCE_STAGE/dcm_project" --configuration "PROD"
```

### 5. Deploy DCM Project

In order to apply changes to your Snowflake account you need to deploy the current definition
the DCM Project. It is recommended to first review a plan of the changes. You can deploy the changes
with the following command:

```bash
snow dcm deploy <project_name> --configuration <config_name>
```

example usage:

```bash
snow dcm deploy EXAMPLE_PROJECT --configuration "DEV"
```

#### DCM Deploy from prepared project files in Snowflake storage

Alternatively if you synchronize your project files with a [SNOWGIT REPOSITORY][snowgit_docs], develop
the DCM Project with [a WORKSPACE][workspaces_docs], or simply you have your project files prepared in
a [USER STAGE][stages_docs], you can specify the source storage with `--from` option, from which you
would like to use the project files for DCM Project `DEPLOY` command.

```bash
snow dcm deploy <project_name> --from <source_stage_name> --configuration <config_name>
```

example usage:

```bash
snow dcm deploy EXAMPLE_PROJECT --from "DB.SCH.SOURCE_STAGE/dcm_project" --configuration "PROD"
```

[manifest]: ./manifest.yml
[raw.sql]: ./definitions/raw.sql
[template]: ./template.yml
[workspaces_docs]: https://docs.snowflake.com/en/user-guide/ui-snowsight/workspaces
[stages_docs]: https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage
[snowgit_docs]: https://docs.snowflake.com/en/developer-guide/git/git-overview
