import json
from pathlib import Path

from backend.app.schemas.project import Project


class ProjectService:
    """Handles loading and validating project information."""

    def load_project(self, project_id: str) -> Project:
        fixture_path = (
            Path(__file__).resolve().parents[3]
            / "data"
            / "projects"
            / "villa_marble_change.json"
        )

        with fixture_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        project = Project.model_validate(data)

        if project.project_id != project_id:
            raise ValueError(f"Project not found: {project_id}")

        return project