from fastapi import HTTPException, status
from app.models.user import RoleEnum

class PermissionService:
    @staticmethod
    def check_employer_permission(user):
        if user.role != RoleEnum.EMPLOYER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only employers can perform this action"
            )

    @staticmethod
    def check_employee_permission(user):
        if user.role != RoleEnum.EMPLOYEE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only employees can perform this action"
            )

    @staticmethod
    def check_task_permission(current_user_id: int, task_assignee_id: int, user_role: RoleEnum):
        if user_role == RoleEnum.EMPLOYEE and current_user_id != task_assignee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to modify this task"
            )
