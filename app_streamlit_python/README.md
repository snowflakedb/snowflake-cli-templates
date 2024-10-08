## Introduction

This is an example template for a Snowflake Native App project which demonstrates the use of Python extension code and adding Streamlit code. This template is meant to guide developers towards a possible project structure on the basis of functionality, as well as to indicate the contents of some common and useful files.

Since this template contains Python files only, you do not need to perform any additional steps to build the source code. You can directly go to the next section. However, if there were any source code that needed to be built, you must manually perform the build steps here before proceeding to the next section.

Similarly, you can also use your own build steps for any other languages supported by Snowflake that you wish to write your code in. For more information on supported languages, visit [docs](https://docs.snowflake.com/en/developer-guide/stored-procedures-vs-udfs#label-sp-udf-languages).

## Run the app
Create or update an application package in your Snowflake account, upload application artifacts to a stage in the application package, and create or update an application object in the same account based on the uploaded artifacts.
```
snow app run
```

For more information, please refer to the Snowflake Documentation on installing and using Snowflake CLI to create a Snowflake Native App.
# Directory Structure
## `/app`
This directory holds your Snowflake Native App files.

### `/app/README.md`
Exposed to the account installing the application with details on what it does and how to use it.

### `/app/manifest.yml`
Defines properties required by the application package. Find more details at the [Manifest Documentation.](https://docs.snowflake.com/en/developer-guide/native-apps/creating-manifest)

### `/app/setup_script.sql`
Contains SQL statements that are run when a consumer installs or upgrades a Snowflake Native App in their account.

## `/scripts`
You can add any additional scripts such as `.sql` and `.jinja` files here. One common use case for such a script is to add shared content from external databases to your application package. This allows you to refer to the external database in the setup script that runs when a Snowflake Native App is installed.
_Note: See the note at the end of `snowflake.yml` if you decide to use the scripts. _


## `/src`
This directory contains code organization by functionality, such as one distinct module for Streamlit related code, and another module for "number add" functionality, which is used an example in this template.
```
/src
   |-module-add
   |          |-main
   |          |    |-python
   |          |           |-add.py
   |          |
   |          |-test
   |               |-python
   |                      |-add_test.py
   |
   |-module-ui
   |         |-src
   |             |-ui.py
   |             |-environment.yml
   |         |-test
   |              |-test_ui.py
```

## `snowflake.yml`
Snowflake CLI uses the `snowflake.yml` file  to discover your project's code and interact with Snowflake using all relevant privileges and grants.

For more information, please refer to the Snowflake Documentation on installing and using Snowflake CLI to create a Snowflake Native App.
<!! if snowflake_cli_version < "3.0.0" !!>
### Adding a snowflake.local.yml file
Though your project directory already comes with a `snowflake.yml` file, an individual developer can choose to customize the behavior of the Snowflake CLI by providing local overrides to `snowflake.yml`, such as a new role to test out your own application package. This is where you can use `snowflake.local.yml`, which is not a version-controlled file.

For more information, please refer to the Snowflake Documentation on installing and using Snowflake CLI to create a Snowflake Native App.
<!! endif !!>

## Unit tests
To set up and run unit tests, please follow the steps below.

### Set up testing conda environment (First Time setup)

Go to the project's root directory where you can find `local_test_env.yml` and run the following command once to set up a conda environment with the correct packages. Please note that the version of test packages may differ from the version of packages in Snowflake, so you will need to be careful with any differences in behavior.

```
conda env create --file local_test_env.yml
```

This will create a conda environment with the name `streamlit-python-testing`.

### Run unit tests
To run unit tests, follow these steps:

#### Activate conda environment
You will need to activate this conda environment once per command line session:
```
conda activate streamlit-python-testing
```
To deactivate and use your current command line session for other tasks, run the following:
```
conda deactivate
```
#### Run Pytest
To run the example tests provided, execute the following command from the project's root:
```
pytest
```
Note that there is a pytest.ini file specifying the location of the source code that we are testing.
