from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
from app.routes.auth import get_current_user
from app.schemas.user_schema import UserResponse
from app.crud.task_crud import TaskCRUD
from app.services.permission_service import PermissionService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/task-summary")
def get_employee_task_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    PermissionService.check_employer_permission(current_user)
    
    summary = TaskCRUD.get_employee_task_summary(db)
    
    task_summary = []
    for item in summary:
        task_summary.append({
            "employee_id": item[0],
            "total_tasks": item[1],
            "completed_tasks": item[2]
        })
    
    return task_summary
