from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from typing import Callable
from functools import wraps
from app.services.task_service import TaskService
from app.models.user import RoleEnum


class PermissionMiddleware:
    @staticmethod
    def check_role(user, required_role: RoleEnum):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Requires {required_role} role."
            )

    @staticmethod
    def check_employer_permission(user):
        PermissionMiddleware.check_role(user, RoleEnum.employer)

    @staticmethod
    def check_employee_permission(user):
        PermissionMiddleware.check_role(user, RoleEnum.employee)


def permission_required(required_role: RoleEnum):
    def decorator(route_handler: Callable):
        @wraps(route_handler)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request") or (args[0] if args else None)

            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object missing"
                )

            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            PermissionMiddleware.check_role(user, required_role)

            return await route_handler(*args, **kwargs)

        return wrapper

    return decorator


def owner_or_assignee_required():
    """Decorator to ensure the user is the owner or assignee of a task."""
    def decorator(route_handler: Callable):
        @wraps(route_handler)
        async def wrapper(task_id: int, *args, **kwargs):
            db: Session = kwargs.get("db") or (args[0] if args else None)
            current_user = kwargs.get("current_user") or (args[1] if args else None)

            if not db or not current_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session or current user is missing."
                )

            task = TaskService.get_task_by_id(db, task_id)

            if current_user.role == RoleEnum.EMPLOYEE and task.assignee_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied. You are not authorized to access this task."
                )

            kwargs["task"] = task
            return await route_handler(task_id, *args, **kwargs)

        return wrapper
    
    return decorator
