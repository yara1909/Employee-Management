import os
import uuid
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
import pytest
from jose import jwt
from app.main import app
from utils.utils import SECRET_KEY, ALGORITHM

TEST_MONGODB_URL = os.getenv("TEST_MONGODB_URL", "mongodb://localhost:27017")
TEST_DB_NAME = "fastapi_auth_test_db"

# =========================================================
# Simple sync fixtures (no async needed for TestClient)
# =========================================================
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_user_payload():
    unique_id = uuid.uuid4().hex[:8]
    return {
        "username": f"normaluser_{unique_id}",
        "email": f"normaluser_{unique_id}@example.com",
        "password": "StrongPass123!",
        "role": "user",
    }

@pytest.fixture
def valid_admin_payload():
    unique_id = uuid.uuid4().hex[:8]
    return {
        "username": f"normaluser_{unique_id}",
        "email": f"normaluser_{unique_id}@example.com",
        "password": "StrongPass123!",
        "role": "admin",
    }

@pytest.fixture
def registered_user(client, valid_user_payload):
    response = client.post("/auth/users/register", json=valid_user_payload)
    assert response.status_code in (200, 201), response.text
    return valid_user_payload

@pytest.fixture
def registered_admin(client, valid_admin_payload):
    response = client.post("/auth/users/register", json=valid_admin_payload)
    assert response.status_code in (200, 201), response.text
    return valid_admin_payload

@pytest.fixture
def user_token(client, registered_user):
    response = client.post(
        "/auth/users/login",
        json={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    return data["access_token"]

@pytest.fixture
def admin_token(client, registered_admin):
    response = client.post(
        "/auth/users/login",
        json={
            "username": registered_admin["username"],
            "password": registered_admin["password"],
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    return data["access_token"]

@pytest.fixture
def expired_token():
    payload = {
        "sub": "normaluser",
        "role": "user",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def malformed_token():
    return "this.is.not.a.valid.jwt"

# =========================================================
# Tests (uncomment as needed)
# =========================================================
def test_register_user_success(client, valid_user_payload):
    response = client.post("/auth/users/register", json=valid_user_payload)
    assert response.status_code in (200, 201), response.text

    data = response.json()
    assert data["message"] == "User registered successfully"
    assert "password" not in data
    assert "hashed_password" not in data

def test_login_success_returns_jwt(client, registered_user):
    response = client.post(
        "/auth/users/login",
        json={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    # Ensure token exists
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20  # basic sanity check

    # Optional: verify token structure by decoding
    decoded = jwt.decode(
        data["access_token"],
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    # Check payload contents
    assert decoded["username"] == registered_user["username"]
    assert decoded["role"] == registered_user["role"]


# def test_protected_route_with_valid_token_succeeds(client, user_token):
#     response = client.get(
#         "/auth/users/protected",  # adjust if your route is different
#         headers={"Authorization": f"Bearer {user_token}"}
#     )

#     assert response.status_code == 200, response.text

#     data = response.json()

#     # Flexible assertion depending on your response
#     assert isinstance(data, dict)

    # Optional (if your route returns user info)
    # assert "username" in data or "message" in data

# def test_protected_route_without_token_returns_401(client):
#     response = client.get("/auth/me")
#     assert response.status_code == 401

def test_admin_route_with_admin_role_succeeds(client, admin_token):
    response = client.get(
        "/auth/users/admin-dashboard",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200, response.text

    data = response.json()

    # Basic validation
    assert isinstance(data, dict)


def test_admin_route_with_user_role_returns_403(client, user_token):
    response = client.get(
        "/auth/users/admin-dashboard",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403, response.text

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "You do not have permission to perform this action"

# def test_protected_route_with_expired_token_returns_401(client, expired_token):
#     response = client.get(
#         "/auth/me",
#         headers={"Authorization": f"Bearer {expired_token}"},
#     )
#     assert response.status_code == 401

# def test_protected_route_with_malformed_token_returns_401(client, malformed_token):
#     response = client.get(
#         "/auth/me",
#         headers={"Authorization": f"Bearer {malformed_token}"},
#     )
#     assert response.status_code == 401