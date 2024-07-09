import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

EXCLUDE_PATHS = [".git", ".github"]


def _yield_template_yml_files(path: Path):
    if path.name in EXCLUDE_PATHS:
        return

    if path.name == "template.yml":
        yield path
    if path.is_dir():
        for child in path.iterdir():
            yield from _yield_template_yml_files(child)


def _failed_render_error(template_root: Path) -> None:
    print(f"Error while rendering template {template_root}")
    sys.exit(1)


def _render_template(template_root: Path):
    print(f"Rendering {template_root}")
    with TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"

        # overestimate number of variables in the template
        max_number_of_variables = (
            (template_root / "template.yml").read_text().count("\n")
        )
        # 42 can be parsed by all supported types (int/float/string)
        process_input = "42\n" * max_number_of_variables

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
        # reasonable 60s timeout
        try:
            snow.communicate(input=process_input.encode(), timeout=60)
        except subprocess.TimeoutExpired:
            print("Timed out after 60s!")
            _failed_render_error(template_root)
        if snow.returncode:
            print(f"Rendering finished with {snow.returncode}")
            _failed_render_error(template_root)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} PATH")
        sys.exit(1)

    root_path = Path(sys.argv[1])
    template_yml_list: List[Path] = list(_yield_template_yml_files(root_path))
    for template_yml in template_yml_list:
        template_root = template_yml.parent
        _render_template(template_root)

    print("OK")
