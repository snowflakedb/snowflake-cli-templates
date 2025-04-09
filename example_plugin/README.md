# Example Snowflake CLI plugin

This is a simple plugin adding basic management commands for [secret objects](https://docs.snowflake.com/en/user-guide/api-authentication#managing-secrets):
```
snow object secret create
snow object secret list
snow object secret describe
snow object secret drop
```
It also serves as a boilerplate for developing your own plugin.

## Installation and usage

To install and use the plugin you simply need to install it in the same python environment
Snowflake CLI is installed in. For example, if the CLI was installed via pip, call
```
pip install ./<! project_dir_name !>
```
You can verify that the plugin is installed by running
```
snow plugin list

+--------------------------+
| plugin name    | enabled |
|----------------+---------|
| example-plugin | False   |
+--------------------------+
```
Each plugin needs to be separately enabled. To enable the plugin, call
```
snow plugin enable example-plugin

Plugin example-plugin successfully enabled.
```

After that, you should see `secret` command in `snow object` command group:
```
snow object --help

...
+- Commands -------------------------------------------------------------------------+
| create     Create an object of a given type. Check documentation for the list of   |
|            supported objects and parameters.                                       |
| describe   Provides description of an object of given type.                        |
| drop       Drops Snowflake object of given name and type.                          |
| list       Lists all available Snowflake objects of given type.                    |
| secret     (plugin) Manage secrets in Snowflake.                                   |
+------------------------------------------------------------------------------------+
```

To uninstall the plugin, uninstall its package using the same package manager used for installation:
```
pip uninstall <! plugin_package_name !>
```

### Config

The plugin has an example configuration containing single boolean argument `print_queries`.
You can modify it in `config.toml`:
```toml
[cli.plugins.example-plugin.config]
print_queries = true
```

## Development from a boilerplate

This plugin consists of 5 files:
```
- pyproject.toml
- src/snowflake_cli_example_plugin/
    - __init__.py
    - commands.py
    - manager.py
    - plugin_spec.py
```

### pyproject.toml
It is a configuration file for python package installers. Each plugin need to be defined as entrypoint
in `"snowflake.cli.plugin.command"` namespace to be detected by CLI. Entrypoint's name defined here is treated
by the CLI as a plugin name for various contexts (reading config, enabling plugin etc.). The entrypoint need to point
to the module with `plugin_spec` implementation.
```toml
[project.entry-points."snowflake.cli.plugin.command"]
<! plugin_name !> = "snowflake_cli_example_plugin.plugin_spec"
```

### plugin_spec.py
This file contains a function returning `snowflake.cli.api.plugins.command.CommandSpec` instance, which defines
what commands are registered by the plugin.

```python
@plugin_hook_impl
def command_spec():
    return CommandSpec(
        parent_command_path=CommandPath(["object"]),
        command_type=CommandType.COMMAND_GROUP,
        typer_instance=commands.app.create_instance(),
    )
```

| argument            | description                                            |
|---------------------|--------------------------------------------------------|
| parent_command_path | command path to which the new command will be appended |
| command type        | `SINGLE_COMMAND` or `COMMAND_GROUP`                    |
| typer_instance      | instance of the command implementation                 |


### commands.py and manager.py

These files contain an example implementation of the command group, showing usage examples of
`snowflake.cli.api` command utils, and example communication with Snowflake using `SQL` interface.
Feel free to use it, or replace it with another method of communicating with Snowflake
(for example Snowflake Python API).
`manager.py` file also shows a basic example of using custom config for your plugin.
