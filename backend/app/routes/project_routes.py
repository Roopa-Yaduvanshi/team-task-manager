"""
Project routes: list and create projects (admin only for create).
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import User, Project
from app.schemas import ProjectCreate, ProjectResponse
from app.dependencies import get_current_user, require_admin
from app.utils import project_to_response

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=List[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all projects (both admin and member can view)."""
    projects = (
        db.query(Project)
        .options(joinedload(Project.creator))
        .order_by(Project.created_at.desc())
        .all()
    )
    return [project_to_response(p) for p in projects]


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Create a new project (admin only)."""
    project = Project(
        title=project_data.title,
        description=project_data.description,
        created_by=admin.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    project = (
        db.query(Project)
        .options(joinedload(Project.creator))
        .filter(Project.id == project.id)
        .first()
    )
    return project_to_response(project)
