"""
Helper functions used across routes.
"""

from datetime import date
from typing import Optional

from app.models import Task, TaskStatus, User, Project


def project_to_response(project: Project) -> dict:
    """Build project dict with creator name for display."""
    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "created_by": project.created_by,
        "creator_name": project.creator.name if project.creator else None,
        "created_at": project.created_at,
    }


def task_to_response(task: Task) -> dict:
    """Build a task dict with extra display fields for the API."""
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "due_date": task.due_date,
        "assigned_to": task.assigned_to,
        "project_id": task.project_id,
        "created_at": task.created_at,
        "assignee_name": task.assignee.name if task.assignee else None,
        "project_title": task.project.title if task.project else None,
    }


def is_task_overdue(task: Task) -> bool:
    """
    A task is overdue if it has a due date in the past
    and is not completed.
    """
    if task.due_date is None:
        return False
    if task.status == TaskStatus.completed:
        return False
    return task.due_date < date.today()


def get_user_by_id(db, user_id: int) -> Optional[User]:
    """Fetch a user by id."""
    return db.query(User).filter(User.id == user_id).first()
