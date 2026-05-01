from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")
    status: TaskStatus = Field(TaskStatus.pending, description="Task status")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Task title"
    )
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
