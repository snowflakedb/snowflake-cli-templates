import streamlit as st
from snowflake.snowpark import Session
from typing import Any, Sequence
import pandas as pd

CACHE_TTL = "1h"


def get_session() -> Session:
    """Return a Snowpark Session.

    Tries local Streamlit connection (with secrets) first. If unavailable,
    falls back to `get_active_session()` for Streamlit-in-Snowflake.
    """
    # Try local dev with Streamlit secrets
    try:
        conn = st.connection("snowflake", type="snowflake")
        return conn.session()
    except Exception:
        pass

    # Fallback: hosted Streamlit-in-Snowflake active session
    try:
        from snowflake.snowpark.context import get_active_session

        return get_active_session()
    except Exception as exc:
        raise RuntimeError("Could not obtain a Snowflake session.") from exc


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
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAADMElEQVR4nOzVwQnAIBQFQYXff81RUkQCOyDj1YOPnbXWPmeTRef+/3O/OyBjzh3CD95BfqICMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMK0CMO0TAAD//2Anhf4QtqobAAAAAElFTkSuQmCC
' as image_url,
    ARRAY_TO_STRING(ARRAY_CONSTRUCT(
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2),
        ROUND(RANDOM() * 100, 2)
    ), ',') as chart_data,
    .3 as progress,
    CASE
        WHEN RANDOM() < 0.33 THEN 'Low'
        WHEN RANDOM() < 0.66 THEN 'Medium'
        ELSE 'High'
    END as status
"""
