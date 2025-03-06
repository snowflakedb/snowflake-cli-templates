import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import pytest
import yaml
from snowflake.cli.__about__ import VERSION
from snowflake.cli.api.project.schemas.template import Template

_REPO_ROOT = Path(__file__).parent.parent
from packaging.version import parse


def _find_all_templates():
    return (
        # "str" to make tests parameters human-readable
        str(x.relative_to(_REPO_ROOT).parent)
        for x in _REPO_ROOT.rglob("**/template.yml")
    )


def _read_template_metadata(template_root: Path) -> Template:
    with (template_root / "template.yml").open("r") as fd:
        yaml_contents = yaml.safe_load(fd) or {}
    return Template(template_root, **yaml_contents)


def _gen_input_values(metadata: Template) -> List[str]:
    result = []
    for variable in metadata.variables:
        value = {
            int: 42,
            float: 3.14,
            str: "a_string",
        }[variable.python_type]
        result.append(value)
    return result


@pytest.mark.parametrize("template_root", _find_all_templates())
def test_render_template(template_root):
    template_root = _REPO_ROOT / template_root
    metadata = _read_template_metadata(template_root)
    if metadata.minimum_cli_version and (
        parse(metadata.minimum_cli_version) > parse(VERSION)
    ):
        pytest.skip(f"Test requires CLI version >= {metadata.minimum_cli_version}")

    with TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        snow = subprocess.Popen(
            [
                "snow",
                "init",
                str(project_path),
                "--template-source",
                template_root,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        try:
            process_input = "\n".join(_gen_input_values(metadata))
            # reasonable 60s timeout
            stdout, stderr = snow.communicate(input=process_input.encode(), timeout=60)
        except subprocess.TimeoutExpired:
            raise AssertionError("Timeout expired")
        assert snow.returncode == 0, (
            f"Rendering finished with {snow.returncode}:\n"
            f"======= stdout =======\n{stdout.decode()}\n"
            f"======= stderr =======\n{stderr.decode()}"
        )


@pytest.mark.parametrize("template_root", _find_all_templates())
def test_too_low_version_error(template_root):
    template_root = _REPO_ROOT / template_root
    metadata = _read_template_metadata(template_root)
    if (not metadata.minimum_cli_version) or (
        parse(metadata.minimum_cli_version) <= parse(VERSION)
    ):
        pytest.skip("CLI version requirements fulfilled")

    with TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        result = subprocess.run(
            ["snow", "init", str(project_path), "--template-source", template_root],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert result.returncode == 1
        assert result.stdout == ""
        assert (
            f"Snowflake CLI version ({VERSION}) is too low - minimum version required by"
            in result.stderr
        )
        assert (
            f"template is {metadata.minimum_cli_version}. Please upgrade before continuing."
            in result.stderr
        )
