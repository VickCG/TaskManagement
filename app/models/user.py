import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class RoleEnum(enum.Enum):
    EMPLOYEE = "employee"
    EMPLOYER = "employer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), nullable=False)

    tasks = relationship("Task", back_populates="assignee")
