# Data Project template

## Introduction

You can use this template as a starter project for a Snowflake Data Project.

Data Projects enable declarative infrastructure management, presenting a less error-prone paradigm
that integrates better with Git than imperative approaches. Through automated change detection, Data
Projects keep the Snowflake environment synchronized with the definitions files in version management.
These projects automatically create new objects, modify existing objects, and delete objects that are
no longer needed, which supports CI/CD best practices when working with Snowflake environments.

## Directory Structure

```
<project_name> (6)
      ├── definitions (2)
      │   ├────── account_objects.sql
      │   ├────── schema_definition.sql
      │   ├────── schema_objects.sql (3)
      │   └────── [...]
      ├── manifest.yml (1)
      ├── snowflake.yml (4)
      └── template.yml (5)
```

1. [manifest.yml][manifest] - is the file that defines:
    * what files should be included in the version creation process. In the `include_definitions` list, you can pass items that are Java regex patterns. The default value is `- definitions/.*`, meaning that all files in the `definitions` folder and its subfolders will be included.
    * configurations that group template variables with their default values. Configurations can be specified here as a series of key-value entries, where the key is the case-insensitive configuration name, and the value is a series of key-value entries, mapping the template variable name to its default value. Each configuration contains a set of key-value pairs, e.g. `example_db_name: "db1"`.
2. `definitions` - is the default directory as defined in the [manifest.yml][manifest] for all .sql files containing project entity definitions. You can use an arbitrarily nested directory structure.
3. [schema_objects.sql][schema_objects.sql] - this is the file that contains some example definitions of project entities. You define particular entities with a `DEFINE` keyword which behaves similar to `CREATE OR ALTER`, e.g. `DEFINE DATABASE d1 COMMENT = 'some comment'`. Removing a `DEFINE` statement results in the entity being dropped.
4. [snowflake.yml][snowflake] - is the Snowflake CLI project definition file for the project. A Snowflake Data Project minimally requires the following parameters in the [snowflake.yml][snowflake] file:
    * `stage` - name of `STAGE` entity that stores project files in Snowflake.
    * `artifacts` - list of files and directories that make up the Snowflake Data Project. The Snowflake CLI will upload them to the stage when creating new project versions.
5. [template.yml][template] - is the name of the template file Snowflake CLI uses to generate a new project.
6. `<project_name>` - is the name of the directory that includes project Data Project artifacts.

### How to organize definition files structure

Once you initialize a project from the template, you create the definitions that will set up your
account. The template doesn't impose any file structure of definition files, but keep in mind that you
don't need to keep all definition statements in a single file. You can organize the code in multiple
files divided into different directories, such as single file per single object type. The following
example uses a more complex file structure:

```
<project_name>
      ├── definitions
      │   ├────── databases.sql
      │   ├────── schemas.sql
      │   ├────── roles.sql
      │   └────── objects
      │           ├────── tables.sql
      │           ├────── views.sql
      │           └────── tasks.sql
      ├── manifest.yml
      └── snowflake.yml
```

To include these files in new project versions, you must also modify `snowflake.yaml`, as shown:

```yaml
definition_version: 2
entities:
  example_project:
    type: project
    stage: "my_project_stage"
    artifacts:
      - definitions/databases.sql
      - definitions/schemas.sql
      - definitions/roles.sql
      - definitions/objects/*
```

You must include all files from the `definitions` directory in the `manifest.yaml` file:

```yaml
manifest_version: 1.0

include_definitions:
  - definitions/.*
```

## Working on Data Projects with Snowflake CLI

### 1. Initialize a Data Project from the template

To initialize a new Data Project from this template, execute the following command and provide the
data required in command prompts. This command creates a new directory with Data Project files.
Replace `<project_dir_name>` with the desired location for the project directory.

```bash
snow init <project_dir_name> --template data_project
```

example usage:

```bash
snow init MY_PROJECT --template data_project
```

### 2. Define entities in `.sql` files

In this step, you define the entities you want the project to manage. You can define these entities
in the prepared `definitions/*.sql` files, but you can also create your own files. If you
decide to add more `.sql` files, make sure that they will be included in the process of creating a new
project version by adding their paths to `include_definitions` list in the [manifest.yaml][manifest] file.

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

### 3. Create the Project

After entity definitions included in definition files are ready to be applied to your infrastructure,
you must create a `PROJECT` entity with a new `VERSION` from your local files. You can perform this
operation by executing the command below:

```bash
snow project create
```

This command will create a new `STAGE` if it doesn't already exist or use an existing one as a target
of local files deployment, from which, the new `VERSION` will be created. The `STAGE` and the `PROJECT`
will be created in the current sessions' database and schema or in these, which are specified in the
flags of `snow` command. Name of the `PROJECT` can be specified in the [snowflake.yml][snowflake] file under
the `identifier` key (if not specified it's taken from `entity_id`) and `STAGE` name is specified under the `stage` key.

You can also use this command for adding new versions, not only the initial one.

### 4. Project dry-run [optional]

After creating a new PROJECT version, you can validate what changes will be applied to your Snowflake
account with this command. This command will perform all the same validations and consistency checks
like a regular `snow project execute`, but will not persist any changes to your Snowflake objects.

```bash
snow project dry-run <project_identifier> --version <version_name>
```

example usage:

```bash
snow project dry-run EXAMPLE_PROJECT --version latest
```

### 5. Execute Project

In order to apply changes to your Snowflake account you need to execute the particular version of
the PROJECT. It is recommended to first perform a dry-run with the changes.You can do this with the
following command:

```bash
snow project execute <project_identifier> --version <version_name>
```

example usage:

```bash
snow project execute EXAMPLE_PROJECT --version latest
```

### 6. Add Project version

If you have already prepared project files for a new PROJECT VERSION, either locally or have it already in one of your Snowflake STAGEs,
and you want to create this VERSION, you can use the command below:

```bash
snow project add-version <entity_id> [--from <stage_path>]
```

example usage:
If `--from` argument is skipped, new VERSION will be created from local files
```bash
snow project add-version EXAMPLE_PROJECT
```

And if `--from` is provided, new PROJECT VERSION will be created from referenced stage:
```bash
snow project add-version EXAMPLE_PROJECT --from @MY_PROJECT_STAGE
```

[manifest]: ./manifest.yml
[snowflake]: ./snowflake.yml
[schema_objects.sql]: ./definitions/schema_objects.sql
[template]: ./template.yml
