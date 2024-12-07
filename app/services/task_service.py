from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.task import Task, TaskStatusEnum
from app.schemas.task_schema import TaskCreate, TaskUpdate
from typing import List, Optional


class TaskService:
    @staticmethod
    def create_task(db: Session, task: TaskCreate):
        db_task = Task(
            title=task.title,
            description=task.description,
            assignee_id=task.assignee_id,
            due_date=task.due_date,
            status=TaskStatusEnum.PENDING
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_tasks(
        db: Session, 
        assignee_id: Optional[int] = None, 
        status: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> List[Task]:
        query = db.query(Task)
        
        # Apply filters
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        
        if status:
            query = query.filter(Task.status == TaskStatusEnum(status))
        
        # Apply sorting
        if sort_by == 'created_at':
            query = query.order_by(Task.created_at)
        elif sort_by == 'due_date':
            query = query.order_by(Task.due_date)
        elif sort_by == 'status':
            query = query.order_by(Task.status)
        
        return query.all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, task_update: TaskUpdate):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_employee_task_summary(db: Session):
        summary = db.query(
            Task.assignee_id, 
            func.count(Task.id).label('total_tasks'),
            func.count(Task.status == TaskStatusEnum.COMPLETED).label('completed_tasks')
        ).group_by(Task.assignee_id).all()
        
        return summary
