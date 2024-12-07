from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse, TaskSummaryResponse
from app.models.user import RoleEnum
from app.services.task_service import TaskService
from app.routes.auth import get_current_user
from app.middlewares.permission_middleware import permission_required, owner_or_assignee_required

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
@permission_required(RoleEnum.EMPLOYER)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TaskService.create_task(db, task, current_user.id)


@router.get("/", response_model=List[TaskResponse])
@permission_required(RoleEnum.EMPLOYER)
async def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    assignee_id: Optional[int] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
):
    if current_user.role == RoleEnum.EMPLOYEE:
        assignee_id = current_user.id

    return TaskService.get_tasks(
        db,
        assignee_id=assignee_id,
        status=status,
        sort_by=sort_by,
    )


@router.patch("/{task_id}", response_model=TaskResponse)
@permission_required(RoleEnum.EMPLOYEE)
@owner_or_assignee_required()
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    task=None
):
    return TaskService.update_task(db, task_id, task_update)


@router.get("/", response_model=List[TaskResponse])
@permission_required(RoleEnum.EMPLOYER)
async def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    assignee_id: Optional[int] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
):
    if current_user.role == RoleEnum.EMPLOYEE:
        assignee_id = current_user.id

    return TaskService.get_tasks(
        db,
        assignee_id=assignee_id,
        status=status,
        sort_by=sort_by,
    )


@router.get("/summary", response_model=List[TaskSummaryResponse])
@permission_required(RoleEnum.EMPLOYER)
async def task_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return TaskService.get_employee_task_summary(db)