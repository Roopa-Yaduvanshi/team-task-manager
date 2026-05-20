"""
Pydantic schemas for request/response validation.
Separate from SQLAlchemy models — keeps API layer clean.
"""

from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field

from app.models import UserRole, TaskStatus


# ---------- Auth schemas ----------

class UserSignup(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    role: UserRole = UserRole.member


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ---------- Project schemas ----------

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_by: int
    creator_name: Optional[str] = None
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------- Task schemas ----------

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None
    project_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None
    project_id: Optional[int] = None


class TaskStatusUpdate(BaseModel):
    """Members only update status."""
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: Optional[date]
    assigned_to: Optional[int]
    project_id: int
    created_at: Optional[datetime]
    assignee_name: Optional[str] = None
    project_title: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Dashboard schemas ----------

class DashboardStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int


class MessageResponse(BaseModel):
    message: str
