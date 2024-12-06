from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base
from app.enums.task_status import TaskStatusEnum
from datetime import datetime, timezone


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.PENDING)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    due_date = Column(DateTime)
    
    assignee_id = Column(Integer, ForeignKey('users.id'))
    assignee = relationship("User", back_populates="tasks")
