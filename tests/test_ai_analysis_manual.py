from backend.app.services.ai_service import AIService
from backend.app.services.project_service import ProjectService


project_service = ProjectService()
ai_service = AIService()

project = project_service.load_project("PRJ-001")

analysis = ai_service.analyze_project(project)

print("\n==============================")
print("PROJECT INTELLIGENCE ANALYSIS")
print("==============================")

print(f"\nProject: {analysis.project_name}")
print(f"Overall Risk: {analysis.overall_risk}")

print(f"\nNumber of Risks: {len(analysis.risks)}")

for index, risk in enumerate(analysis.risks, start=1):
    print(f"\n--- Risk {index} ---")
    print(f"Title: {risk.title}")
    print(f"Severity: {risk.severity}")
    print(f"Cause: {risk.cause}")

    print("\nEvidence:")

    for evidence in risk.evidence:
        print(f"  Document: {evidence.document_title}")
        print(f"  Quote: {evidence.quote}")
        print(f"  Verified: {evidence.verified}")

    print("\nAffected Tasks:")

    for task in risk.affected_tasks:
        print(f"  - {task}")

    print("\nDownstream Impact:")

    for impact in risk.downstream_impact:
        print(f"  - {impact}")

    print("\nRecommended Actions:")

    for action in risk.recommended_actions:
        print(f"  - {action}")