import pytest
from app.models.task import TaskStatusEnum

def test_employer_create_task(client, employer_token, db, employee_user):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {employer_token}"},
        json={
            "title": "Test Task",
            "description": "Test Description",
            "assignee_id": employee_user.id,
            "due_date": "2024-12-31T00:00:00"
        }
    )
    assert response.status_code == 200
    task_data = response.json()
    assert task_data["title"] == "Test Task"
    assert task_data["status"] == "pending"

def test_employee_cannot_create_task(client, employee_token, employee_user):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "title": "Unauthorized Task",
            "description": "Should fail",
            "assignee_id": employee_user.id,
            "due_date": "2024-12-31T00:00:00"
        }
    )
    assert response.status_code == 403

def test_employee_view_own_tasks(client, employer_token, employee_token, db, employee_user):
    create_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {employer_token}"},
        json={
            "title": "Employee Task",
            "description": "Employee's task",
            "assignee_id": employee_user.id,
            "due_date": "2024-12-31T00:00:00"
        }
    )
    
    list_response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) > 0
    assert all(task['assignee_id'] == employee_user.id for task in tasks)

def test_task_update(client, employer_token, employee_token, db, employee_user):
    create_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {employer_token}"},
        json={
            "title": "Update Task",
            "description": "Task to update",
            "assignee_id": employee_user.id,
            "due_date": "2024-12-31T00:00:00"
        }
    )
    task_id = create_response.json()['id']
    
    update_response = client.patch(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "status": "in_progress"
        }
    )
    
    assert update_response.status_code == 200
    assert update_response.json()['status'] == "in_progress"

def test_employee_cannot_update_others_task(client, employer_token, employee_token, db):
    other_employee = client.post(
        "/users/",
        json={
            "username": "other_employee",
            "email": "other@test.com",
            "password": "password123",
            "role": "employee"
        }
    )
    other_employee_id = other_employee.json()['id']
    
    create_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {employer_token}"},
        json={
            "title": "Another Employee Task",
            "description": "Task for another employee",
            "assignee_id": other_employee_id,
            "due_date": "2024-12-31T00:00:00"
        }
    )
    task_id = create_response.json()['id']
    
    update_response = client.patch(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "status": "in_progress"
        }
    )
    
    assert update_response.status_code == 403