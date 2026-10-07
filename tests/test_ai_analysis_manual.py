from backend.app.services.ai_service import AIService
from backend.app.services.project_service import ProjectService


def main():
    project_service = ProjectService()
    ai_service = AIService()

    project = project_service.load_project("PRJ-001")

    analysis = ai_service.analyze_project(project)

    print("\n==============================")
    print("PROJECT INTELLIGENCE ANALYSIS")
    print("==============================")

    print(f"\nProject: {analysis.project_name}")
    print(f"Overall Risk: {analysis.overall_risk}")
    print(f"Number of Risks: {len(analysis.risks)}")

    for index, risk in enumerate(analysis.risks, start=1):
        print(f"\n--- Risk {index} ---")

        print(f"Title: {risk.title}")
        print(f"Severity: {risk.severity}")

        print("\nCause:")
        print(risk.cause)

        print("\nEvidence:")

        for evidence in risk.evidence:
            print(f"  Document: {evidence.document_title}")
            print(f"  Document ID: {evidence.document_id}")
            print(f"  Quote: {evidence.quote}")
            print(f"  Verified: {evidence.verified}")

        print("\nRoot Cause Tasks:")

        for task in risk.root_cause_tasks:
            print(f"  - {task}")

        print("\nCurrently Affected Tasks:")

        for task in risk.affected_tasks:
            print(f"  - {task}")

        print("\nDownstream Tasks:")

        for task in risk.downstream_tasks:
            print(f"  - {task}")

        print("\nDownstream Impact:")

        for impact in risk.downstream_impact:
            print(f"  - {impact}")

        print("\nRecommended Actions:")

        for action in risk.recommended_actions:
            print(f"  - {action}")

    print("\n==============================")
    print("ANALYSIS COMPLETE")
    print("==============================")


if __name__ == "__main__":
    main()