import json
from pathlib import Path

from backend.app.schemas.project import Project


def test_villa_project_fixture_is_valid():
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "projects"
        / "villa_marble_change.json"
    )

    with fixture_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    project = Project.model_validate(data)

    assert project.project_id == "PRJ-001"
    assert len(project.tasks) == 5
    assert len(project.task_dependencies) == 3
    assert len(project.documents) == 2