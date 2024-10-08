from __future__ import annotations

from snowflake.snowpark import Session
from common import get_secret_value, send_request


def request_procedure(session: Session) -> str:
    # Retrieve secret value
    _ = get_secret_value()

    # Send request
    return send_request()
