import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User, RoleEnum
from app.services.auth_service import AuthService
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_FILE = os.path.join(ROOT_DIR, "env/test.env")
load_dotenv(dotenv_path=ENV_FILE)

TEST_DATABASE_URL = os.getenv("DATABASE_URL")
if not TEST_DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
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
def employer_token(client):
    response = client.post(
        "/auth/login",  # Ensure the correct endpoint path
        json={
            "username": "employer_test",
            "password": "employer_password"
        }
    )
    print("Response JSON:", response.json())  # Debugging: Inspect response content
    assert response.status_code == 200, f"Login failed: {response.json()}"
    assert "access_token" in response.json(), f"Missing access_token: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def employee_token(client):
    response = client.post(
        "/login", 
        json={
            "username": "employee_test", 
            "password": "employee_password"
        }
    )
    return response.json()["access_token"]
