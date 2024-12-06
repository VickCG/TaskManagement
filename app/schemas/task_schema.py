from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.enums.task_status import TaskStatusEnum


class TaskBase(BaseModel):
    title: str = Field(..., example="Fix login bug")
    description: Optional[str] = Field(None, example="Resolve the issue with login not working for certain users.")
    assignee_id: Optional[int] = Field(None, example=1)
    due_date: Optional[datetime] = Field(None, example="2024-12-31T23:59:59")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Fix logout bug")
    description: Optional[str] = Field(None, example="Resolve the issue with logout.")
    assignee_id: Optional[int] = Field(None, example=2)
    due_date: Optional[datetime] = Field(None, example="2025-01-15T23:59:59")
    status: Optional[TaskStatusEnum] = Field(None, example=TaskStatusEnum.COMPLETED)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    assignee_id: Optional[int]
    due_date: Optional[datetime]
    status: TaskStatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskSummary(BaseModel):
    assignee_id: int
    total_tasks: int
    completed_tasks: int
