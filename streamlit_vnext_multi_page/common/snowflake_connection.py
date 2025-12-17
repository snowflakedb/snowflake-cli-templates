from typing import Any, Sequence

import pandas as pd
import streamlit as st
from snowflake.snowpark import Session

# This is the duration for which query results are cached (= 1 hour).
# You can set it to None to disable caching.
CACHE_TTL = "1h"


def get_connection() -> st.connections.SnowflakeConnection:
    """Return a Snowflake connection."""
    return st.connection("snowflake")


def get_session() -> Session:
    """Return a cached Snowpark Session."""
    if "_snowflake_session" not in st.session_state:
        st.session_state._snowflake_session = get_connection().session()
    return st.session_state._snowflake_session


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def run_query(sql: str, params: Sequence[Any] | None = None) -> pd.DataFrame:
    """Execute SQL and return a Pandas DataFrame.

    Parameters
    ----------
    sql: str
        The SQL statement with optional "?" placeholders.
    params: Sequence[Any] | None
        Positional parameters to bind to placeholders.
    """
    session = get_session()
    return session.sql(sql, params=params).to_pandas()


SAMPLE_DATAFRAME_SQL = """
SELECT
    CURRENT_TIMESTAMP() as timestamp,
    ARRAY_CONSTRUCT(
        0,
        25,
        2,
        6,
        10,
        15,
        6,
        1,
        5
    ) as chart_data,
    .3 as progress,
    CASE
        WHEN RANDOM() < 0.33 THEN 'Low'
        WHEN RANDOM() < 0.66 THEN 'Medium'
        ELSE 'High'
    END as status
"""
