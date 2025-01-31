import toml, subprocess
from typing import Any


def export_dependencies():
    with open("pyproject.toml") as f:
        pyproject = toml.load(f)
    project: dict[str, Any] = pyproject.get("project", {})
    dependencies: list[str] = project.get("dependencies", [])
    with open("requirements.txt", "w") as f:
        for item in dependencies:
            name, version = item.split(" ")
            limit = version.split(",")[0].lstrip("(")
            f.write(f"{name}{limit}\n")


def stage_requirements():
    subprocess.run(["git", "add", "requirements.txt"])


if __name__ == "__main__":
    export_dependencies()
    stage_requirements()
