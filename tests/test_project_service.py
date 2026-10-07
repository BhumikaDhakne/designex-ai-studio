from backend.app.services.project_service import ProjectService


def test_load_villa_project():
    service = ProjectService()

    project = service.load_project("PRJ-001")

    assert project.project_id == "PRJ-001"
    assert project.project_name == "Palm Jumeirah Luxury Villa"
    assert len(project.tasks) == 5
    assert len(project.documents) == 2