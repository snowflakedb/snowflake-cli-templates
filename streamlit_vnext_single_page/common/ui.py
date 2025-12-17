import yaml


def read_app_name() -> str:
    """Read the app name from the snowflake.yml file."""
    with open("snowflake.yml", "r") as f:
        config = yaml.safe_load(f)
        return list(config["entities"].keys())[0]


APP_NAME = read_app_name().title()
