"""
Implementation of SecretManager, presenting an example of running SQL queries in Snowflake
and how to use internal plugin config.
"""

from snowflake.cli.api.plugins.plugin_config import PluginConfigProvider
from snowflake.cli.api.sql_execution import SqlExecutionMixin
from snowflake.connector.cursor import SnowflakeCursor
from enum import Enum
from click import ClickException
from snowflake.cli.api.identifiers import FQN
from typing import Optional


class SecretType(str, Enum):
    """Supported secret types."""

    PASSWORD = "password"
    GENERIC_STRING = "generic_string"
    SYMMETRIC_KEY = "symmetric_key"

    @classmethod
    def all(cls):
        return list(x.value for x in cls)

    @classmethod
    def of_string(cls, value):
        try:
            return cls(value)
        except ValueError:
            raise ClickException(
                f"Invalid secret type: `{value}`. Supported secret types: {', '.join(cls.all())}"
            )


class SecretManager(SqlExecutionMixin):
    def __init__(self):
        super().__init__()
        # reading config from [cli.plugins.example-plugin.config] section
        config_provider = PluginConfigProvider()
        self.config = config_provider.get_config("example-plugin")

    def _execute_query(self, query: str) -> SnowflakeCursor:
        print_query = self.config.internal_config.get("print_queries", False)
        if print_query:
            print(query)
        return self.execute_query(query)

    def create(
        self,
        secret_type: SecretType,
        fqn: FQN,
        replace: bool,
        if_not_exists: bool,
        username: Optional[str] = None,
        password: Optional[str] = None,
        value: Optional[str] = None,
    ):
        replace_str = "OR REPLACE " if replace else ""
        if_not_exists_str = "IF NOT EXISTS " if if_not_exists else ""
        query = (
            f"CREATE {replace_str}SECRET {if_not_exists_str}{fqn.sql_identifier} "
            f"TYPE = '{secret_type.upper()}' "
        )

        if secret_type == SecretType.SYMMETRIC_KEY:
            query += "ALGORITHM = GENERIC"
        if secret_type == SecretType.PASSWORD:
            query += f"USERNAME = '{username}' PASSWORD = '{password}'"
        if secret_type == SecretType.GENERIC_STRING:
            query += f"SECRET_STRING = '{value}'"

        return self._execute_query(query)

    def show(self, like: Optional[str]) -> SnowflakeCursor:
        query = "SHOW SECRETS"
        if like:
            query += f" LIKE '{like}'"
        return self._execute_query(query)

    def drop(self, fqn: FQN) -> SnowflakeCursor:
        query = f"DROP SECRET {fqn.sql_identifier}"
        return self._execute_query(query)

    def describe(self, fqn: FQN) -> SnowflakeCursor:
        query = f"DESCRIBE SECRET {fqn.sql_identifier}"
        return self._execute_query(query)
