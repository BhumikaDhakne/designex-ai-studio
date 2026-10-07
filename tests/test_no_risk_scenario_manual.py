from backend.app.services.ai_service import AIService
from backend.app.services.project_service import ProjectService


def test_no_risk_project_returns_low_risk():
    project_service = ProjectService()
    ai_service = AIService()

    project = project_service.load_project("PRJ-002")

    analysis = ai_service.analyze_project(project)

    assert analysis.overall_risk == "LOW"
    assert analysis.risks == []