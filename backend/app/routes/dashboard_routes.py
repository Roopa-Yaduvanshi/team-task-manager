"""
Dashboard route: task statistics.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Task, UserRole, TaskStatus
from app.schemas import DashboardStats
from app.dependencies import get_current_user
from app.utils import is_task_overdue

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return task counts for the dashboard.
    Admin sees all tasks; member sees only assigned tasks.
    """
    query = db.query(Task)

    if current_user.role == UserRole.member:
        query = query.filter(Task.assigned_to == current_user.id)

    tasks = query.all()

    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == TaskStatus.completed)
    pending = sum(
        1
        for t in tasks
        if t.status in (TaskStatus.pending, TaskStatus.in_progress)
    )
    overdue = sum(1 for t in tasks if is_task_overdue(t))

    return DashboardStats(
        total_tasks=total,
        completed_tasks=completed,
        pending_tasks=pending,
        overdue_tasks=overdue,
    )
