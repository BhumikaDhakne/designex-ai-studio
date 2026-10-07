from backend.app.services.ai_service import AIService
from backend.app.services.project_service import ProjectService


def test_supplier_delay_detects_downstream_schedule_risk():
    project_service = ProjectService()
    ai_service = AIService()

    project = project_service.load_project("PRJ-003")

    analysis = ai_service.analyze_project(project)

    assert analysis.overall_risk in {"HIGH", "CRITICAL"}
    assert len(analysis.risks) >= 1

    risk = analysis.risks[0]

    assert "T-203" in risk.root_cause_tasks
    assert "T-204" in risk.affected_tasks
    assert "T-205" in risk.downstream_tasks

    assert all(
        evidence.verified
        for evidence in risk.evidence
    )