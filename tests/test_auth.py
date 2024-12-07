from app.models.user import RoleEnum


def test_user_registration(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "secure_password",
            "role": RoleEnum.EMPLOYER.value,
        },
    )
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["username"] == "new_user"
    assert json_data["email"] == "new_user@example.com"
    assert json_data["role"] == RoleEnum.EMPLOYER.value


def test_user_registration_conflict(client, employer_user):
    response = client.post(
        "/auth/register",
        json={
            "username": employer_user.username,
            "email": employer_user.email,
            "password": "secure_password",
            "role": RoleEnum.EMPLOYER.value,
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Username or email already registered"


def test_login_success(client, employer_user):
    response = client.post(
        "/auth/login",
        json={
            "username": employer_user.username,
            "password": "employer_password",
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"


def test_login_failure_missing_fields(client):
    response = client.post(
        "/auth/login",
        json={},  # Empty payload
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "username"]
    assert response.json()["detail"][0]["msg"] == "Field required"


def test_decode_jwt_token(client, employer_token):
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response.status_code == 200


def test_protected_route_without_token(client):
    response = client.get("/tasks")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
