import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from snowflake.cli.__about__ import VERSION
import pytest
from contextlib import contextmanager

if VERSION < "2.8.0":
    pytest.skip("This test requires CLI >= 2.8.0", allow_module_level=True)


@pytest.fixture()
def initialize_project():
    @contextmanager
    def _initialize_project(template_name):
        with TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "project"
            output = subprocess.check_output(
                [
                    "snow",
                    "init",
                    str(project_dir),
                    "--template",
                    template_name,
                    "--no-interactive",
                ],
                encoding="utf-8",
            )
            assert "Initialized the new project in" in output

            old_cwd = os.getcwd()
            os.chdir(project_dir)
            yield project_dir
            os.chdir(old_cwd)

    return _initialize_project


def test_snowpark_examples_functions_work_locally(initialize_project):
    with initialize_project("example_snowpark") as snowpark_project:
        output = subprocess.check_output(
            ["python", str(snowpark_project / "app" / "functions.py"), "FooBar"],
            encoding="utf-8",
        )
        assert output.strip() == "Hello FooBar!"

        output = subprocess.check_output(
            ["python", str(snowpark_project / "app" / "procedures.py"), "BazBar"],
            encoding="utf-8",
        )
        assert output.strip() == "Hello BazBar!"


def test_example_snowpark_yml_is_correct(initialize_project):
    with initialize_project("example_snowpark") as snowpark_project:
        output = subprocess.check_output(
            ["snow", "snowpark", "build"],
            encoding="utf-8",
        )
        assert "Build done." in output


def test_example_streamlit_yml_is_correct(initialize_project):
    with initialize_project("example_streamlit") as streamlit_project:
        result = subprocess.run(
            ["snow", "streamlit", "deploy"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert not "During evaluation of " in result.stdout + result.stderr
