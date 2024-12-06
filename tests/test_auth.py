import pytest
from app.models.user import RoleEnum

def test_user_creation(db, employer_user, employee_user):
    assert employer_user.role == RoleEnum.EMPLOYER
    assert employee_user.role == RoleEnum.EMPLOYEE
    assert employer_user.username == "employer_test"
    assert employee_user.username == "employee_test"

def test_login_success(client, employer_user):
    response = client.post(
        "/login", 
        json={
            "username": "employer_test", 
            "password": "employer_password"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure(client):
    response = client.post(
        "/login", 
        json={
            "username": "nonexistent", 
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401