import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.config import Base
from app.models.user import User, RoleEnum
from app.models.task import Task, TaskStatusEnum
from app.services.auth_service import AuthService

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def employer_user(db):
    hashed_password = AuthService.get_password_hash("employer_password")
    employer = User(
        username="employer_test",
        email="employer@test.com",
        hashed_password=hashed_password,
        role=RoleEnum.EMPLOYER
    )
    db.add(employer)
    db.commit()
    db.refresh(employer)
    return employer

@pytest.fixture(scope="function")
def employee_user(db):
    hashed_password = AuthService.get_password_hash("employee_password")
    employee = User(
        username="employee_test",
        email="employee@test.com",
        hashed_password=hashed_password,
        role=RoleEnum.EMPLOYEE
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@pytest.fixture(scope="function")
def employer_token(client, employer_user):
    response = client.post(
        "/login", 
        json={
            "username": "employer_test", 
            "password": "employer_password"
        }
    )
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def employee_token(client, employee_user):
    response = client.post(
        "/login", 
        json={
            "username": "employee_test", 
            "password": "employee_password"
        }
    )
    return response.json()["access_token"]