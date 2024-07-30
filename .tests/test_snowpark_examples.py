import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def test_snowpark_examples_functions_work_locally():
    with TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "snowpark"
        output = subprocess.check_output(
            [
                "snow",
                "init",
                str(project_dir),
                "--template",
                "example_snowpark",
                "--no-interactive",
            ],
            encoding="utf-8",
        )
        assert "Initialized the new project in" in output

        output = subprocess.check_output(
            ["python", str(project_dir / "app" / "functions.py"), "FooBar"],
            encoding="utf-8",
        )
        assert output.strip() == "Hello FooBar!"

        output = subprocess.check_output(
            ["python", str(project_dir / "app" / "procedures.py"), "BazBar"],
            encoding="utf-8",
        )
        assert output.strip() == "Hello BazBar!"
