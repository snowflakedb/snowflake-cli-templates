import subprocess
import sys
import yaml

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from snowflake.cli.api.project.schemas.template import Template

EXCLUDE_PATHS = [".git", ".github"]

"""
Recursively looks for all template.yml files, assuming that they are
placed in root directory of the template.
Then calls `snow init` command on every template.
Variable values are deduced from the template.yml file.
"""


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


def _exit_with_failed_render_error(template_root: Path) -> None:
    print(f"Error while rendering template: {template_root}")
    sys.exit(1)


def _render_template(template_root: Path):
    print(f"Rendering {template_root}")
    with TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        snow = subprocess.Popen(
            [
                "snow",
                "init",
                str(project_path),
                "--template-source",
                str(template_root),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        try:
            process_input = "\n".join(_gen_input_values(template_root))
            # reasonable 60s timeout
            snow.communicate(input=process_input.encode(), timeout=60)
        except subprocess.TimeoutExpired:
            print("Timed out after 60s!")
            _exit_with_failed_render_error(template_root)
        if snow.returncode:
            print(f"Rendering finished with {snow.returncode}")
            _exit_with_failed_render_error(template_root)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} PATH")
        sys.exit(1)

    root_path = Path(sys.argv[1])
    for template_yml in root_path.rglob("**/template.yml"):
        template_root = template_yml.parent
        _render_template(template_root)

    print("OK")
