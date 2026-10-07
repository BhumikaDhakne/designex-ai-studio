from typing import Literal

from pydantic import BaseModel, Field


RiskSeverity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class Evidence(BaseModel):
    document_id: str
    document_title: str
    quote: str
    verified: bool = False


class RiskAnalysis(BaseModel):
    title: str
    severity: RiskSeverity
    cause: str
    evidence: list[Evidence]
    affected_tasks: list[str]
    downstream_impact: list[str]
    recommended_actions: list[str]


class ProjectAnalysisResponse(BaseModel):
    project_id: str
    project_name: str
    overall_risk: RiskSeverity
    risks: list[RiskAnalysis]