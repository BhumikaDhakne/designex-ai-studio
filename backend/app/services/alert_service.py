from datetime import date

from backend.app.schemas.alert import (
    TaskAlert,
    TaskAlertResponse,
)
from backend.app.schemas.project import Project


class AlertService:
    """Generates deterministic project task alerts."""

    STALE_DAYS = 5

    def generate_alerts(
        self,
        project: Project,
        reference_date: date,
    ) -> TaskAlertResponse:
        """Generate deadline and stale-task alerts."""

        alerts: list[TaskAlert] = []

        for task in project.tasks:
            if task.status in {
                "Completed",
                "Cancelled",
            }:
                continue

            days_until_deadline = (
                task.deadline - reference_date
            ).days

            if days_until_deadline < 0:
                alerts.append(
                    self._build_alert(
                        project=project,
                        task=task,
                        alert_type="OVERDUE",
                        severity="HIGH",
                        message=(
                            f"Task '{task.title}' is "
                            f"{abs(days_until_deadline)} "
                            "day(s) overdue."
                        ),
                        recipients=[
                            task.owner,
                            project.project_manager,
                        ],
                    )
                )

            elif days_until_deadline == 1:
                alerts.append(
                    self._build_alert(
                        project=project,
                        task=task,
                        alert_type="DUE_TOMORROW",
                        severity="HIGH",
                        message=(
                            f"Task '{task.title}' is due "
                            "tomorrow."
                        ),
                        recipients=[
                            task.owner,
                            project.project_manager,
                        ],
                    )
                )

            elif days_until_deadline == 3:
                alerts.append(
                    self._build_alert(
                        project=project,
                        task=task,
                        alert_type="DUE_SOON",
                        severity="MEDIUM",
                        message=(
                            f"Task '{task.title}' is due "
                            "in 3 days."
                        ),
                        recipients=[
                            task.owner,
                        ],
                    )
                )

        return TaskAlertResponse(
            reference_date=reference_date.isoformat(),
            total_alerts=len(alerts),
            alerts=alerts,
        )

    def _build_alert(
        self,
        project: Project,
        task,
        alert_type,
        severity,
        message,
        recipients,
    ) -> TaskAlert:
        return TaskAlert(
            task_id=task.task_id,
            task_title=task.title,
            project_id=project.project_id,
            project_name=project.project_name,
            owner=task.owner,
            project_manager=project.project_manager,
            deadline=task.deadline.isoformat(),
            alert_type=alert_type,
            severity=severity,
            message=message,
            recipients=recipients,
        )