import streamlit as st
from common.snowflake_connection import (
    run_query,
    SAMPLE_DATAFRAME_SQL,
)
from common.ui import APP_NAME, APP_LOGO

st.logo(
    APP_LOGO,
    size="large",
)

f"""
# {APP_NAME}

Welcome to the home page of my app!

Let's collect data from Snowflake and display it in a dataframe.
"""

df = run_query(SAMPLE_DATAFRAME_SQL)


st.dataframe(
    df,
    column_config={
        "TIMESTAMP": st.column_config.DatetimeColumn(
            "Timestamp", format="DD/MM/YY HH:mm"
        ),
        "IMAGE_URL": st.column_config.ImageColumn("Image"),
        "CHART_DATA": st.column_config.LineChartColumn("Chart Data"),
        "PROGRESS": st.column_config.ProgressColumn(
            "Progress", min_value=0, max_value=1
        ),
        "STATUS": st.column_config.SelectboxColumn(
            "Status", options=["Low", "Medium", "High"]
        ),
    },
    hide_index=True,
)


"""
Cool, right? You can discover the SQL query by expanding the code block below.
"""

st.expander("View SQL query", expanded=False, icon=":material/code:").code(
    SAMPLE_DATAFRAME_SQL
)

"""
Now, time to use your own data and build your beautiful data app, **enjoy!** :material/celebration:
"""
