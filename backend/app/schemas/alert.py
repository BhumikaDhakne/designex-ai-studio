from typing import Literal

from pydantic import BaseModel


AlertType = Literal[
    "DUE_SOON",
    "DUE_TOMORROW",
    "OVERDUE",
    "STALE",
]


class TaskAlert(BaseModel):
    task_id: str
    task_title: str
    project_id: str
    project_name: str
    owner: str
    project_manager: str
    deadline: str
    alert_type: AlertType
    severity: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
    ]
    message: str
    recipients: list[str]


class TaskAlertResponse(BaseModel):
    reference_date: str
    total_alerts: int
    alerts: list[TaskAlert]