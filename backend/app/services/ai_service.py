from openai import OpenAI

from backend.app.core.config import OPENAI_API_KEY
from backend.app.schemas.project import Project
from backend.app.schemas.risk import ProjectAnalysisResponse
from backend.app.services.dependency_service import DependencyService


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

    def analyze_project(
        self,
        project: Project,
    ) -> ProjectAnalysisResponse:
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
  missing follow-up, or information that may affect downstream work.
- Connect document evidence to the project's task dependencies.

Classify tasks into:

1. root_cause_tasks:
   Tasks directly associated with the origin of the issue.

2. affected_tasks:
   Tasks currently requiring action, validation, correction,
   or review because of the identified issue.

Do NOT determine downstream_tasks yourself.
The application will calculate downstream tasks deterministically
from the project's dependency graph.

- Do not put every related task into affected_tasks.
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
            raise RuntimeError(
                "AI returned no structured project analysis."
            )

        analysis = response.output_parsed

        dependency_service = DependencyService(project)

        for risk in analysis.risks:
            normalized_root_tasks: list[str] = []
            normalized_affected_tasks: list[str] = []

            # Resolve root-cause task references.
            for task_reference in risk.root_cause_tasks:
                task_id = dependency_service.normalize_task_id(
                    task_reference
                )

                if task_id and task_id not in normalized_root_tasks:
                    normalized_root_tasks.append(task_id)

            # Resolve affected task references.
            for task_reference in risk.affected_tasks:
                task_id = dependency_service.normalize_task_id(
                    task_reference
                )

                if task_id and task_id not in normalized_affected_tasks:
                    normalized_affected_tasks.append(task_id)

            risk.root_cause_tasks = normalized_root_tasks
            risk.affected_tasks = [
                task_id
                for task_id in normalized_affected_tasks
                if task_id not in set(normalized_root_tasks)
            ]

            # Calculate downstream tasks from the affected tasks.
            downstream_candidates: set[str] = set()

            for task_id in risk.affected_tasks:
                downstream_candidates.update(
                    dependency_service.get_all_downstream_tasks(
                        task_id
                    )
                )

            risk.downstream_tasks = [
                task_id
                for task_id in downstream_candidates
                if task_id not in set(risk.root_cause_tasks)
                and task_id not in set(risk.affected_tasks)
            ]

        # Independently verify every AI-provided evidence quote.
        for risk in analysis.risks:
            for evidence in risk.evidence:
                source_document = next(
                    (
                        document
                        for document in project.documents
                        if document.document_id
                        == evidence.document_id
                    ),
                    None,
                )

                if source_document is None:
                    evidence.verified = False
                    continue

                evidence.verified = (
                    evidence.quote in source_document.content
                )

        return analysis