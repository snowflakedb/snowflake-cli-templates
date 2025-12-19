# Multi-page Streamlit App Template

This template provides a foundation for building multi-page Streamlit applications that connect to Snowflake. It includes:

- A clean project structure with separate pages in `app_pages/`
- Common utilities for Snowflake connectivity and UI components in `common/`
- Sample pages demonstrating:
  - Data fetching from Snowflake
  - Data visualization
  - Material Design icons
  - Top navigation bar (configurable to sidebar)
  - App logo (use your own logo, or drop this)

## Getting Started

1. Update the app name and description in `pyproject.toml`
2. Configure your Snowflake connection details in `snowflake.yml`
3. Start building your pages in the `app_pages/` directory
4. Add new pages to the navigation list in `streamlit_app.py`
5. Create a `uv` environment using `uv sync`
6. Run the app using `uv run streamlit run streamlit_app.py`
