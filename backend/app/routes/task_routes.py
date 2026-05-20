"""
Task routes: CRUD with role-based permissions.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import User, Task, UserRole, Project
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, MessageResponse
from app.dependencies import get_current_user, require_admin
from app.utils import task_to_response, get_user_by_id

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admin: all tasks.
    Member: only tasks assigned to them.
    """
    query = db.query(Task).options(
        joinedload(Task.assignee),
        joinedload(Task.project),
    )

    if current_user.role == UserRole.member:
        query = query.filter(Task.assigned_to == current_user.id)

    tasks = query.order_by(Task.created_at.desc()).all()
    return [task_to_response(t) for t in tasks]


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Create and optionally assign a task (admin only)."""
    project = db.query(Project).filter(Project.id == task_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if task_data.assigned_to:
        assignee = get_user_by_id(db, task_data.assigned_to)
        if not assignee:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        due_date=task_data.due_date,
        assigned_to=task_data.assigned_to,
        project_id=task_data.project_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # Load relationships for response
    task = (
        db.query(Task)
        .options(joinedload(Task.assignee), joinedload(Task.project))
        .filter(Task.id == task.id)
        .first()
    )
    return task_to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admin: full update.
    Member: can only update status on their assigned tasks.
    """
    task = (
        db.query(Task)
        .options(joinedload(Task.assignee), joinedload(Task.project))
        .filter(Task.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role == UserRole.member:
        if task.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Not your task")
        if task_data.status is None:
            raise HTTPException(
                status_code=400,
                detail="Members can only update task status",
            )
        task.status = task_data.status
    else:
        # Admin full update
        update_data = task_data.model_dump(exclude_unset=True)
        if "project_id" in update_data:
            project = db.query(Project).filter(Project.id == update_data["project_id"]).first()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
        if "assigned_to" in update_data and update_data["assigned_to"]:
            assignee = get_user_by_id(db, update_data["assigned_to"])
            if not assignee:
                raise HTTPException(status_code=404, detail="Assigned user not found")

        for key, value in update_data.items():
            setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task_to_response(task)


@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Delete a task (admin only)."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return MessageResponse(message="Task deleted successfully")
