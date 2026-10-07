from backend.app.schemas.risk import (
    Evidence,
    ProjectAnalysisResponse,
    RiskAnalysis,
)


def test_risk_analysis_schema():
    response = ProjectAnalysisResponse(
        project_id="PRJ-001",
        project_name="Palm Jumeirah Luxury Villa",
        overall_risk="HIGH",
        risks=[
            RiskAnalysis(
                title="Marble specification mismatch",
                severity="HIGH",
                cause="Client changed the marble finish.",
                evidence=[
                    Evidence(
                        document_id="DOC-001",
                        document_title="Client Coordination Meeting",
                        quote="The client requested a change to the marble finish.",
                    )
                ],
                affected_tasks=["T-002", "T-003", "T-004", "T-005"],
                downstream_impact=[
                    "BOQ may require revision",
                    "Supplier quotation may need revision",
                    "Material delivery could be delayed"
                ],
                recommended_actions=[
                    "Confirm revised specification",
                    "Update BOQ",
                    "Request revised supplier quotation"
                ],
            )
        ],
    )

    assert response.project_id == "PRJ-001"
    assert response.overall_risk == "HIGH"
    assert len(response.risks) == 1
    assert response.risks[0].evidence[0].verified is False