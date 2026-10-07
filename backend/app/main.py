from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.schemas.alert import TaskAlertResponse
from backend.app.schemas.content import ContentGenerationRequest
from backend.app.schemas.visual import (
    VisualGenerationRequest,
    VisualRefinementRequest,
)
from backend.app.services.ai_service import AIService
from backend.app.services.alert_service import AlertService
from backend.app.services.content_service import ContentGenerationService
from backend.app.services.project_service import ProjectService
from backend.app.services.visual_service import VisualGenerationService


app = FastAPI(
    title="Designex AI Studio",
    description=(
        "AI intelligence layer for Designex project, "
        "visual and content workflows."
    ),
    version="0.7.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


project_service = ProjectService()
ai_service = AIService()
visual_service = VisualGenerationService()
content_service = ContentGenerationService()
alert_service = AlertService()


app.mount(
    "/generated",
    StaticFiles(directory="generated"),
    name="generated",
)


@app.get("/")
def root():
    return {
        "name": "Designex AI Studio",
        "status": "running",
        "version": "0.7.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


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


@app.post("/visuals/generate")
def generate_visual(request: VisualGenerationRequest):
    try:
        result = visual_service.generate(request)

        return result.model_dump(mode="json")

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Visual generation failed: {str(exc)}",
        )


@app.post("/visuals/refine")
def refine_visual(request: VisualRefinementRequest):
    try:
        result = visual_service.refine(request)

        return result.model_dump(mode="json")

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Visual refinement failed: {str(exc)}",
        )


@app.post("/content/generate")
def generate_content(request: ContentGenerationRequest):
    try:
        result = content_service.generate(request)

        return result.model_dump(mode="json")

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Content generation failed: {str(exc)}",
        )


@app.post("/content/{generation_id}/approve")
def approve_content(generation_id: str):
    try:
        result = content_service.approve(generation_id)

        return result.model_dump(mode="json")

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Content approval failed: {str(exc)}",
        )


@app.get(
    "/projects/{project_id}/alerts",
    response_model=TaskAlertResponse,
)
def get_project_alerts(
    project_id: str,
    reference_date: date,
):
    try:
        project = project_service.load_project(project_id)

        return alert_service.generate_alerts(
            project=project,
            reference_date=reference_date,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Project not found: {project_id}",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Alert generation failed: {str(exc)}",
        )