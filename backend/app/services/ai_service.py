from openai import OpenAI

from backend.app.core.config import OPENAI_API_KEY
from backend.app.schemas.project import Project
from backend.app.schemas.risk import ProjectAnalysisResponse


class AIService:
    """Handles AI-powered project intelligence analysis."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def test_connection(self) -> str:
        response = self.client.responses.create(
            model="gpt-5.5",
            input="Respond with exactly: Designex AI connection successful.",
        )

        return response.output_text

    def analyze_project(self, project: Project) -> ProjectAnalysisResponse:
        """
        Analyze structured project data and unstructured project documents
        to identify supported project risks and downstream impact.
        """

        project_data = project.model_dump(mode="json")

        instructions = """
You are the Project Intelligence engine for Designex AI Studio.

Your job is to analyze a design/construction project by connecting:

1. Structured project information:
   - tasks
   - task deadlines
   - task statuses
   - task dependencies

2. Unstructured project information:
   - meeting minutes
   - procurement updates
   - client requests
   - site reports
   - project notes

Identify risks that are actually supported by the provided information.

IMPORTANT RULES:

- Do not invent facts.
- Do not assume a task is at risk only because it is incomplete.
- Look for contradictions, changes, dependencies, outdated information,
  missing follow-up, or information that could affect downstream work.
- Connect document evidence to affected tasks and their dependencies.
- Explain the cause of each risk.
- Explain the downstream impact.
- Recommend practical recovery actions.
- Every evidence quote MUST be copied verbatim from the source document.
- If there is no meaningful risk supported by the information,
  return an empty risks list and overall_risk = "LOW".
- Do not create a risk simply to make the analysis interesting.
- Risk severity should reflect business/project impact:
  LOW, MEDIUM, HIGH, or CRITICAL.
"""

        response = self.client.responses.parse(
            model="gpt-5.5",
            instructions=instructions,
            input=[
                {
                    "role": "user",
                    "content": (
                        "Analyze the following Designex project data.\n\n"
                        f"{project_data}"
                    ),
                }
            ],
            text_format=ProjectAnalysisResponse,
        )

        if response.output_parsed is None:
            raise RuntimeError("AI returned no structured project analysis.")

        analysis = response.output_parsed

        # Verify every AI-provided evidence quote independently.
        for risk in analysis.risks:
            for evidence in risk.evidence:
                source_document = next(
                    (
                        document
                        for document in project.documents
                        if document.document_id == evidence.document_id
                    ),
                    None,
                )

                if source_document is None:
                    evidence.verified = False
                    continue

                evidence.verified = evidence.quote in source_document.content

        return analysis