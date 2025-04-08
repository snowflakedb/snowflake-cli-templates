"""
Implementation of plugin_hook, where the new commands should be registered.
"""

from snowflake.cli.api.plugins.command import (
    CommandPath,
    CommandSpec,
    CommandType,
    plugin_hook_impl,
)
from snowflake_cli_example_plugin import commands


@plugin_hook_impl
def command_spec():
    return CommandSpec(
        # new command will be visible as "snow object COMMAND"
        parent_command_path=CommandPath(["object"]),
        # choose CommandType.SINGLE_COMMAND for a single command
        command_type=CommandType.COMMAND_GROUP,
        # link to the commands implementation
        typer_instance=commands.app.create_instance(),
    )
