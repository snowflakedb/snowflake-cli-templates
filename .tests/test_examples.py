import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from snowflake.cli.__about__ import VERSION

if VERSION < "2.8.0":
    pytest.skip("This test requires CLI >= 2.8.0", allow_module_level=True)

_REPO_ROOT = Path(__file__).parent.parent


def _snow() -> str:
    candidate = Path(sys.executable).with_name("snow")
    if candidate.exists():
        return str(candidate)
    found = shutil.which("snow")
    if not found:
        raise FileNotFoundError("snow CLI executable not found")
    return found


def _skip_if_cli_below(minimum: str) -> None:
    from packaging.version import Version

    if Version(VERSION) < Version(minimum):
        pytest.skip(f"This test requires CLI >= {minimum}")


@pytest.fixture()
def initialize_project():
    @contextmanager
    def _initialize_project(template_name, extra_args=None):
        with TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "project"
            cmd = [
                _snow(),
                "init",
                str(project_dir),
                "--template",
                template_name,
                "--no-interactive",
                "--template-source",
                str(_REPO_ROOT),
            ]
            if extra_args:
                cmd.extend(extra_args)
            output = subprocess.check_output(cmd, encoding="utf-8")
            assert "Initialized the new project in" in output

            old_cwd = os.getcwd()
            os.chdir(project_dir)
            try:
                yield project_dir
            finally:
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
        result = subprocess.run(
            [
                _snow(),
                "snowpark",
                "build",
                "--ignore-anaconda",
                "--allow-shared-libraries",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert result.returncode == 0, result.stderr
        assert "Build done." in result.stdout


def test_example_streamlit_yml_is_correct(initialize_project):
    with initialize_project("example_streamlit") as streamlit_project:
        result = subprocess.run(
            [_snow(), "streamlit", "deploy"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert not "During evaluation of " in result.stdout + result.stderr


def _init_fails_as_invalid_identifier(template_name, extra_args):
    with TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "project"
        cmd = [
            _snow(),
            "init",
            str(project_dir),
            "--template",
            template_name,
            "--no-interactive",
            "--template-source",
            str(_REPO_ROOT),
            *extra_args,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8"
        )
        assert result.returncode != 0, result.stdout + result.stderr
        blob = " ".join((result.stdout + result.stderr).split())
        assert "cannot be converted to valid Snowflake identifier" in blob


def _streamlit_base_args(**overrides):
    values = {
        "database_name": "MY_DB",
        "schema_name": "PUBLIC",
        "warehouse_name": "COMPUTE_WH",
        "stage_name": "dev_deployment",
        "secret_name": "streamlit_secret",
        "external_access_integration_name": "streamlit_external_access_integration",
    }
    values.update(overrides)
    extra = []
    for key, value in values.items():
        extra.extend(["-D", f"{key}={value}"])
    return extra


def _dcm_base_args(**overrides):
    values = {
        "account_identifier": "myorg-myacct",
        "project_owner": "PROJECT_ADMIN",
        "db_name": "MY_DB",
        "schema_name": "PUBLIC",
        "project_name": "DCM_PROJECT",
    }
    values.update(overrides)
    extra = []
    for key, value in values.items():
        extra.extend(["-D", f"{key}={value}"])
    return extra


def test_dcm_manifest_renders_valid_yaml_for_plain_and_quoted_identifiers(
    initialize_project,
):
    _skip_if_cli_below("3.16.0")
    import yaml

    with initialize_project("dcm_project", extra_args=_dcm_base_args()) as project:
        parsed = yaml.safe_load((project / "manifest.yml").read_text(encoding="utf-8"))
        target = parsed["targets"]["DCM_DEV"]
        assert parsed["default_target"] == "DCM_DEV"
        assert list(parsed["targets"]) == ["DCM_DEV"]
        assert target["account_identifier"] == "myorg-myacct"
        assert target["project_name"] == "MY_DB.PUBLIC.DCM_PROJECT_DEV"
        assert target["project_owner"] == "PROJECT_ADMIN"
        assert parsed["templating"]["defaults"]["project_owner_role"] == "PROJECT_ADMIN"

    quoted_args = _dcm_base_args(
        project_owner='"My Role"',
        project_name='"My Project"',
    )
    with initialize_project("dcm_project", extra_args=quoted_args) as project:
        rendered = (project / "manifest.yml").read_text(encoding="utf-8")
        assert '""My Role""' not in rendered
        assert '""My Project""' not in rendered
        parsed = yaml.safe_load(rendered)
        target = parsed["targets"]["DCM_DEV"]
        assert target["account_identifier"] == "myorg-myacct"
        assert target["project_owner"] == '"My Role"'
        assert target["project_name"] == 'MY_DB.PUBLIC."My Project_DEV"'
        assert parsed["templating"]["defaults"]["project_owner_role"] == '"My Role"'


def test_dcm_manifest_yaml_encodes_multiline_account_locator(initialize_project):
    _skip_if_cli_below("3.16.0")
    import yaml

    extra_args = _dcm_base_args(
        account_identifier=(
            "myorg-myacct\ndefault_target: OTHER\ntargets:\n  OTHER:\n"
            "    account_identifier: myorg-myacct\n    project_name: EXISTING.PUBLIC.PROJ\n"
            "extra: |"
        )
    )
    with initialize_project("dcm_project", extra_args=extra_args) as project:
        parsed = yaml.safe_load((project / "manifest.yml").read_text(encoding="utf-8"))
        assert parsed["default_target"] == "DCM_DEV"
        assert list(parsed["targets"]) == ["DCM_DEV"]
        assert "OTHER" not in parsed
        assert "extra" not in parsed
        assert parsed["targets"]["DCM_DEV"]["project_name"] == "MY_DB.PUBLIC.DCM_PROJECT_DEV"
        assert isinstance(parsed["targets"]["DCM_DEV"]["account_identifier"], str)


def test_dcm_project_name_yaml_encodes_sibling_keys(initialize_project):
    _skip_if_cli_below("3.16.0")
    extra_args = _dcm_base_args(
        project_name=(
            "DCM_PROJECT\ndefault_target: OTHER\ntargets:\n  OTHER:\n"
            "    project_name: EXISTING.PUBLIC.PROJ\nextra: |"
        )
    )
    _init_fails_as_invalid_identifier("dcm_project", extra_args)


def test_dcm_rejects_project_name_that_is_not_an_identifier(initialize_project):
    _skip_if_cli_below("3.16.0")
    extra_args = _dcm_base_args(project_name="7days")
    _init_fails_as_invalid_identifier("dcm_project", extra_args)


def test_streamlit_external_access_yml_does_not_double_quote_identifiers(
    initialize_project,
):
    _skip_if_cli_below("3.0.0")
    import yaml

    extra_args = [
        "-D",
        "database_name=MY_DB",
        "-D",
        "schema_name=PUBLIC",
        "-D",
        'warehouse_name="My Warehouse"',
        "-D",
        "stage_name=dev_deployment",
        "-D",
        "secret_name=streamlit_secret",
        "-D",
        'external_access_integration_name="My Integration"',
    ]
    with initialize_project(
        "streamlit_with_external_access", extra_args=extra_args
    ) as project:
        rendered = (project / "snowflake.yml").read_text(encoding="utf-8")
        assert '""My Warehouse""' not in rendered
        assert '""My Integration""' not in rendered
        parsed = yaml.safe_load(rendered)
        assert parsed["entities"]["dashboard"]["query_warehouse"] == '"My Warehouse"'
        assert parsed["mixins"]["external_access"]["external_access_integrations"] == [
            '"My Integration"'
        ]
        setup_sql = (project / "setup.sql").read_text(encoding="utf-8")
        assert 'CREATE EXTERNAL ACCESS INTEGRATION IF NOT EXISTS "My Integration"' in setup_sql


def test_streamlit_yml_yaml_encodes_warehouse_sibling_keys(initialize_project):
    _skip_if_cli_below("3.0.0")
    _init_fails_as_invalid_identifier(
        "streamlit_with_external_access",
        _streamlit_base_args(
            warehouse_name="WH\nsecond line"
        ),
    )


def test_streamlit_quoted_integration_name_stays_one_yaml_string(initialize_project):
    _skip_if_cli_below("3.0.0")
    import yaml

    extra_args = _streamlit_base_args(
        external_access_integration_name='"My Integration; note"'
    )
    with initialize_project(
        "streamlit_with_external_access", extra_args=extra_args
    ) as project:
        parsed = yaml.safe_load((project / "snowflake.yml").read_text(encoding="utf-8"))
        names = parsed["mixins"]["external_access"]["external_access_integrations"]
        assert names == ['"My Integration; note"']
        assert names[0].startswith('"') and names[0].endswith('"')


def test_streamlit_quoted_newline_warehouse_stays_one_scalar(initialize_project):
    _skip_if_cli_below("3.0.0")
    import yaml

    extra_args = _streamlit_base_args(warehouse_name='"WH\nline two"')
    with initialize_project(
        "streamlit_with_external_access", extra_args=extra_args
    ) as project:
        parsed = yaml.safe_load((project / "snowflake.yml").read_text(encoding="utf-8"))
        assert parsed["entities"]["dashboard"]["query_warehouse"] == '"WH\nline two"'
        assert list(parsed["entities"]) == ["dashboard"]


def test_streamlit_quoted_newline_stage_does_not_replace_entities(initialize_project):
    _skip_if_cli_below("3.0.0")
    import yaml

    extra_args = _streamlit_base_args(
        stage_name='"stage\nline two"'
    )
    with initialize_project(
        "streamlit_with_external_access", extra_args=extra_args
    ) as project:
        parsed = yaml.safe_load((project / "snowflake.yml").read_text(encoding="utf-8"))
        rendered = (project / "snowflake.yml").read_text(encoding="utf-8")
        assert "<% ctx.env.stage_name %>" in rendered
        assert parsed["entities"]["dashboard"]["identifier"]["name"] == "dashboard"
        assert list(parsed["entities"]) == ["dashboard"]
        assert parsed["env"]["stage_name"].startswith('"stage')


def test_snowpark_yml_encodes_integration_name(initialize_project):
    _skip_if_cli_below("3.0.0")
    import yaml

    extra_args = [
        "-D",
        "database_name=MY_DB",
        "-D",
        "schema_name=PUBLIC",
        "-D",
        "stage_name=dev_deployment",
        "-D",
        "secret_name=snowpark_secret",
        "-D",
        'external_access_integration_name="My Integration"',
    ]
    with initialize_project(
        "snowpark_with_external_access", extra_args=extra_args
    ) as project:
        parsed = yaml.safe_load((project / "snowflake.yml").read_text(encoding="utf-8"))
        assert parsed["mixins"]["external_access"]["external_access_integrations"] == [
            '"My Integration"'
        ]
        setup_sql = (project / "setup.sql").read_text(encoding="utf-8")
        assert 'CREATE EXTERNAL ACCESS INTEGRATION IF NOT EXISTS "My Integration"' in setup_sql
