"""
This file contains implementation of "secret" command group containing three commands (create, list and drop).

It presents you usage examples of snowflake.cli.api commands utils.
"""

from typing import Optional

import typer
from click import ClickException
from snowflake.cli.api.commands.flags import (
    IdentifierType,
    IfNotExistsOption,
    ReplaceOption,
    like_option,
)
from snowflake.cli.api.commands.snow_typer import SnowTyperFactory
from snowflake.cli.api.identifiers import FQN
from snowflake.cli.api.output.types import (
    CommandResult,
    QueryResult,
    SingleQueryResult,
)

from snowflake_cli_example_plugin.manager import SecretManager, SecretType

app = SnowTyperFactory(
    name="secret",  # name of the command group - commands will be available as "snow object secret X"
    help="(plugin) Manage secrets in Snowflake.",
)

NameArgument = typer.Argument(
    help="Name of the secret.",
    show_default=False,
    click_type=IdentifierType(),
)


@app.command(
    "list",
    requires_connection=True,
)
def list_(
    like: str = like_option(
        help_example='`list --like "my%"` lists all secrets that begin with “my”'
    ),
    **options,
):
    """Lists all available secrets."""
    sm = SecretManager()
    return QueryResult(sm.show(like=like))


@app.command(requires_connection=True)
def drop(name: FQN = NameArgument, **options):
    """Drops secret."""
    sm = SecretManager()
    return SingleQueryResult(sm.drop(fqn=name))


@app.command(requires_connection=True)
def describe(name: FQN = NameArgument, **options):
    """Describes secret."""
    sm = SecretManager()
    return SingleQueryResult(sm.describe(fqn=name))


@app.command(requires_connection=True)
def create(
    secret_type: str = typer.Argument(
        help=f"Secret type. Should be one of {', '.join(SecretType.all())}",
        show_default=False,
    ),
    name: FQN = NameArgument,
    # '_' at the end of the name as 'user' and 'password' are connection arguments
    username_: Optional[str] = typer.Option(
        None, "--secret-username", help="Username for secret of type 'password'"
    ),
    password_: Optional[str] = typer.Option(
        None, "--secret-password", help="Password for secret of type 'password'"
    ),
    value: Optional[str] = typer.Option(
        None, "--value", help="Value for secret of type 'generic_string'"
    ),
    # replace_option and if_not_exists option automatically throw an error if used together
    if_not_exists: bool = IfNotExistsOption(),
    replace: bool = ReplaceOption(),
    **options,
) -> CommandResult:
    """
    Creates a secret object in Snowflake.
    """
    # validate flags
    _type = SecretType.of_string(secret_type.lower())
    if _type == SecretType.PASSWORD and (not username_ or not password_):
        raise ClickException(
            "Both `--secret-username` and `--secret-password` must be provided for secret of type `password`."
        )
    if _type == SecretType.GENERIC_STRING and not value:
        raise ClickException(
            "`--value` must be provided for secret of type `generic_string`."
        )

    sm = SecretManager()
    return SingleQueryResult(
        sm.create(
            secret_type=_type,
            fqn=name,
            if_not_exists=if_not_exists,
            replace=replace,
            username=username_,
            password=password_,
            value=value,
        )
    )
