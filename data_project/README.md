# Data Project template

## Introduction

This is the template which can be considered as a starter of the Data Project in Snowflake. The Data
Project allows applying changes to the account infrastructure in a declarative way which make this
process more convenient comparing it to the imperative way. Data Projects detect changes which should
be applied automatically (creates, alters and drops) and take care of execution defined statements
in the correct order on its own.

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
      * attach a specific by passing its relative path from the root of the project, e.g. `definitions/main.sql`
      * attach all files from a specific dir, e.g. `definitions/.*`
    * specify values for template variables. Template are rendered and filled up with variable values during the project execution process. Variable values are defined in the `template_variables` list, e.g. `example_db_name: "db1"`
2. `definitions` - this is the directory that is initially configured in the [manifest.yml][manifest] to be a place for all `.sql` files containing project entities definitions. You can also arrange the directory/file structure by yourself.
3. [main.sql][main.sql] - this is the file that contains some example definitions of project entities. You define particular entities with a `DEFINE` keyword which behaves similar to `CREATE OR ALTER`, e.g. `DEFINE DATABASE d1 COMMENT = 'some comment'`. You can also replace [main.sql][main.sql] or create more `.sql` files to organise the code better.
4. [snowflake.yml][snowflake] - this is the file required by the `Snowflake CLI`. The most important keys are:
    * `identifier` - specifies the name of PROJECT entity managed in Snowflake.
    * `stage` - specifies the name of STAGE entity that store project files in Snowflake.
    * `main_file` - the path to the projects' manifest file.
    * `artifacts` - the list of paths to files/directories that should be used by the `Snowflake CLI` in Data Project management.
5. [template.yml][template] - this file is used by the `Snowflake CLI` to generate a new project from this template.

## Working on Data Projects with Snowflake CLI

### 1. Initialize Data Project from the template

In order to initialize a new Data Project from this template execute the command below and provide data required in command prompts. This command will create a new directory with Data Project files. Fill `<project_dir_name>` with your own name.

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

### Create Project

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

### Project dry-run [optional]

Before the real execution of the PROJECT, you can validate what changes will be applied to your infrastructure.
In purpose of this action, you can perform the dry-run execution with the command below. This command won't
persist any changes in the infrastructure.

```bash
snow project dry-run <project_name> --version <version_name>
```

example usage:

```bash
snow project dry-run MY_PROJECT --version 'VERSION$3'
```

### Execute Project

In order to apply changes to your infrastructure you need to execute the particular version of the PROJECT.
You can do this with the following command:

```bash
snow project execute <project_name> --version <version_name>
```

example usage:

```bash
snow project execute MY_PROJECT --version 'VERSION$3'
```

### Add Project version

If you have already prepared files for a new PROJECT VERSION in one of your Snowflake STAGEs, and you
want to create this VERSION, you can use the command below:

```bash
snow project add-version <project_name> --from <stage_path>
```

example usage:

```bash
snow project add-version MY_PROJECT --from @DB.SCH.MY_PROJECT_STAGE  --dbname DB --schema SCH
```

[manifest]: ./manifest.yml
[snowflake]: ./snowflake.yml
[main.sql]: ./definitions/main.sql
[template]: ./template.yml
