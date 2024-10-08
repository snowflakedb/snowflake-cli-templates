import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).parent.parent


def iter_all_templates():
    return (
        # "str" to make tests parameters human-readable
        str(x.relative_to(_REPO_ROOT).parent)
        for x in _REPO_ROOT.rglob("**/template.yml")
    )


def template_has_cli_version_limit(template_root: Path) -> bool:
    return "minimum_cli_version" in (template_root / "template.yml").read_text()


def is_snowflake_yml_V2(template_root: Path) -> bool:
    for file in template_root.rglob("*.yml"):
        for line in file.read_text().splitlines():
            if re.match(r".*definition_version:\s+.?2.*", line):
                return True
    return False


@pytest.mark.parametrize("template_root", iter_all_templates())
def test_V2_template_has_cli_version_limit(template_root):
    template_path = _REPO_ROOT / template_root
    if not is_snowflake_yml_V2(template_path):
        pytest.skip("No snowflake.yml in definition version 2 found")

    assert template_has_cli_version_limit(
        template_path
    ), "snowflake.yml V2 is not supported in Snowflake CLI 2.X. Please add 'minimum_cli_version: 3.0.0' to template.yml"
