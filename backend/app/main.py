from fastapi import FastAPI, HTTPException

from backend.app.services.ai_service import AIService
from backend.app.services.project_service import ProjectService


app = FastAPI(
    title="Designex AI Studio",
    description="AI intelligence layer for Designex project, visual and content workflows.",
    version="0.2.0",
)


project_service = ProjectService()
ai_service = AIService()


@app.get("/")
def root():
    return {
        "name": "Designex AI Studio",
        "status": "running",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/projects/{project_id}/analysis")
def analyze_project(project_id: str):
    try:
        project = project_service.load_project(project_id)
        analysis = ai_service.analyze_project(project)

        return analysis.model_dump(mode="json")

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Project not found: {project_id}",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Project analysis failed: {str(exc)}",
        )