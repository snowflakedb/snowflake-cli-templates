import pytest
import subprocess
import yaml

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from snowflake.cli.api.project.schemas.template import Template


_REPO_ROOT = Path(__file__).parent.parent


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


def _gen_input_values(template_root: Path) -> List[str]:
    metadata = _read_template_metadata(template_root)
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
            process_input = "\n".join(_gen_input_values(template_root))
            # reasonable 60s timeout
            snow.communicate(input=process_input.encode(), timeout=60)
        except subprocess.TimeoutExpired:
            raise AssertionError("Timeout expired")
        assert snow.returncode == 0, f"Rendering finished with {snow.returncode}"
