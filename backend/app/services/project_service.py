import json
from pathlib import Path

from backend.app.schemas.project import Project


class ProjectService:
    """Handles loading and validating project information."""

    def load_project(self, project_id: str) -> Project:
        projects_path = (
            Path(__file__).resolve().parents[3]
            / "data"
            / "projects"
        )

        project_files = projects_path.glob("*.json")

        for project_file in project_files:
            with project_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if data.get("project_id") != project_id:
                continue

            return Project.model_validate(data)

        raise ValueError(f"Project not found: {project_id}")