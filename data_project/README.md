# Data Project template

## Introduction

This template can be used as a starting point for a Snowflake Data Project.

Data Projects enable declarative infrastructure management, presenting a less error-prone paradigm
that integrates better with Git than imperative approaches. Through automated change detection, Data
Projects keep the Snowflake environment in-sync with the definitions files in version management.
New objects will be created, existing objects modified, and no longer needed objects deleted.
This enables the use of CI/CD best practices when working with Snowflake environments.

## Directory Structure

```
<project_name>
      ├── definitions (2)
      │   ├────── main.sql (3)
      │   └────── [...]
      ├── manifest.yml (1)
      ├── snowflake.yml (4)
      └── template.yml (5)
```

1. [manifest.yml][manifest] - this is the file where you can:
    * specify what files should be included in the version creation process. In the `include_definitions` list you can:
      * include a specific file by passing its relative path to the root of the project, e.g. `definitions/main.sql`
      * include all files from a specific directory, e.g. `definitions/.*`
    * specify values for template variables. Definition files (templates) are rendered as Jinja2 variables during the project execution process. Variable values are defined in the `template_variables` list, e.g. `example_db_name: "db1"`
2. `definitions` - this is the default directory as defined in the [manifest.yml][manifest] for all `.sql` files containing project entity definitions. You are free to use an arbitrarily nested directory structure.
3. [main.sql][main.sql] - this is the file that contains some example definitions of project entities. You define particular entities with a `DEFINE` keyword which behaves similar to `CREATE OR ALTER`, e.g. `DEFINE DATABASE d1 COMMENT = 'some comment'`. Removing a `DEFINE` statement results in the entity being dropped. You can also replace [main.sql][main.sql] or create more `.sql` files to organise the code better.
4. [snowflake.yml][snowflake] - this is the file required by the `Snowflake CLI`. The most important keys are:
    * `identifier` - specifies the name of `PROJECT` entity managed in Snowflake.
    * `stage` - specifies the name of `STAGE` entity that stores project files in Snowflake.
    * `main_file` - the path to the projects' manifest file.
    * `artifacts` - the list of files and directories that make up the Snowflake Data Project. The Snowflake CLI will upload them to the stage when creating new project versions.
5. [template.yml][template] - this file is used by the `Snowflake CLI` to generate a new project from this template.

### How to organize definition files structure

Once you initialize a project from the template, it's time to create definitions that will set up your
account. The template doesn't impose any file structure of definition files, but keep in mind that you
don't need to keep all definition statements in a single file. It's possible to organize the code in
multiple files divided into different directories, e.g. single file per single object type. An example,
more complex files structure is shown below

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

In order to include these files in new project versions it's also required to modify `snowflake.yaml`:

```yaml
definition_version: 2
entities:
  my_project:
    type: project
    identifier: "my_project"
    stage: "my_project_stage"
    main_file: manifest.yml
    artifacts:
      - definitions/objects.sql
      - definitions/schema_definition.sql
      - definitions/sadf/**
      - manifest.yml
```

It's also  required to include all files from the `definitions` directory in the `manifest.yaml` file:

```yaml
manifest_version: 1.0

include_definitions:
  - definitions/.*
```

## Working on Data Projects with Snowflake CLI

### 1. Initialize Data Project from the template

In order to initialize a new Data Project from this template execute the command below and provide data required in command prompts. This command will create a new directory with Data Project files. Please fill `<project_dir_name>` with where you want the project directory to be created.

```bash
snow init <project_dir_name> --template data_project
```

example usage:

```bash
snow init MY_PROJECT --template data_project
```

### 2. Define entities in `.sql` files

In this step you need to define entities that will be managed by the project. You can define these
entities in the prepared [definitions/main.sql][main.sql] file, but you can also create your own files. If you
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

### 3. Create Project

Once the entity definitions included in definition files are ready to be applied to your infrastructure,
it's required to create a `PROJECT` entity with a new `VERSION` from your local files. You can perform this
operation by executing the command below:

```bash
snow project create-version
```

This command will create a new `STAGE` if it doesn't already exist or use an existing one as a target
of local files deployment, from which, the new `VERSION` will be created. The `STAGE` and the `PROJECT`
will be created in the current sessions' database and schema or in these, which are specified in the
flags of `snow` command. Name of the `PROJECT` is specified in the [snowflake.yml][snowflake] file under the `identifier`
key and `STAGE` name is specified under the `stage` key.

You can also use this command for adding new versions, not only the initial one.

### 4. Project dry-run [optional]

After creating a new PROJECT version, you can validate what changes will be applied to your Snowflake
account with this command. This command will perform all the same validations and consistency checks
like a regular `snow project execute`, but will not persist any changes to your Snowflake objects.

```bash
snow project dry-run <project_name> --version <version_name>
```

example usage:

```bash
snow project dry-run <! name | to_snowflake_identifier !> --version latest
```

### 5. Execute Project

In order to apply changes to your Snowflake account you need to execute the particular version of
the PROJECT. It is recommended to first perform a dry-run with the changes.You can do this with the
following command:

```bash
snow project execute <project_name> --version <version_name>
```

example usage:

```bash
snow project execute <! name | to_snowflake_identifier !> --version latest
```

### 6. Add Project version

If you have already prepared project files for a new PROJECT VERSION in one of your Snowflake STAGEs,
and you want to create this VERSION, you can use the command below:

```bash
snow project add-version <project_name> --from <stage_path>
```

example usage:

```bash
snow project add-version <! name | to_snowflake_identifier !> --from @<! stage | to_snowflake_identifier !>
```

[manifest]: ./manifest.yml
[snowflake]: ./snowflake.yml
[main.sql]: ./definitions/main.sql
[template]: ./template.yml
