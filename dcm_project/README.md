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

1. [manifest.yml][manifest] - it holds the essential configuration details of the project and allows the project folder to be identified as a DCM project. For more information, see [the manifest documentation](http://docs.snowflake.com/en/user-guide/dcm-projects/dcm-projects-files#create-a-manifest-file).
2. `definitions` - is the directory for all .sql files containing project entity definitions. You can use an arbitrarily nested directory structure.
3. `macros` - (optional) is the directory for all .sql files containing project macros. You can use an arbitrarily nested directory structure.
4. [examples.sql][examples.sql] - this is the file that contains some example definitions of project entities. You define particular entities with a `DEFINE` keyword which behaves similar to `CREATE OR ALTER`, e.g. `DEFINE DATABASE d1 COMMENT = 'some comment'`. Removing a `DEFINE` statement results in the entity being dropped.
5. [jinja_demo.sql][jinja_demo.sql] - this is the file that contains some example definitions focusing on demoing some Jinja capabilities, like using loops and macros
6. [grants_macro.sql][grants_macro.sql] - this is the file that contains a sample Jinja macro granting privileges
6. `<project_name>` - is the repository project folder.

### How to organize the definition files structure

Once you initialize a project folder from the template, you can write the object definitions and then deploy them to a specified target.
The template doesn't impose any file structure of definition files, but keep in mind that you
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
      │       └────── utils
      │               └────── date_time.sql
      └── manifest.yml
```

## Working on DCM Projects with Snowflake CLI

For detailed instructions, see [the documentation](http://docs.snowflake.com/en/user-guide/dcm-projects/dcm-projects-files)

[manifest]: ./manifest.yml
[examples.sql]: ./sources/definitions/examples.sql
[jinja_demo.sql]: ./sources/definitions/jinja_demo.sql
[grants_macro.sql]: ./sources/macros/grants_macro.sql
[template]: ./template.yml
