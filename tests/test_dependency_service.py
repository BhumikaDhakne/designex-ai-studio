from backend.app.services.dependency_service import DependencyService
from backend.app.services.project_service import ProjectService


def test_direct_downstream_tasks():
    project = ProjectService().load_project("PRJ-001")

    dependency_service = DependencyService(project)

    result = dependency_service.get_direct_downstream_tasks("T-002")

    assert result == ["T-003"]


def test_all_downstream_tasks():
    project = ProjectService().load_project("PRJ-001")

    dependency_service = DependencyService(project)

    result = dependency_service.get_all_downstream_tasks("T-002")

    assert result == ["T-003", "T-004", "T-005"]


def test_task_with_no_downstream_tasks():
    project = ProjectService().load_project("PRJ-001")

    dependency_service = DependencyService(project)

    result = dependency_service.get_all_downstream_tasks("T-005")

    assert result == []