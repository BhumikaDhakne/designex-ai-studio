from datetime import date
from pydantic import BaseModel, Field


class Task(BaseModel):
    task_id: str
    title: str
    owner: str
    status: str
    deadline: date


class TaskDependency(BaseModel):
    task_id: str
    depends_on_task_id: str


class ProjectDocument(BaseModel):
    document_id: str
    document_type: str
    title: str
    doc_date: date
    content: str


class Project(BaseModel):
    project_id: str
    project_name: str
    project_type: str
    location: str
    status: str
    project_manager: str
    tasks: list[Task]
    task_dependencies: list[TaskDependency]
    documents: list[ProjectDocument]