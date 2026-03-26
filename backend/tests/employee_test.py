from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    # Login as admin (or user) to get token
    response = client.post("/login", data={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def create_employee(client, employee_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/employees/employee", json=employee_data, headers=headers)
    assert response.status_code == 200
    yield employee_data
    # Cleanup after test
    client.delete(f"/employees/employee/{employee_data['employeeID']}", headers=headers) 

def test_get_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_employee(client, employee_data):
    response = client.post("/employees/employee", json=employee_data)
    assert response.status_code == 200
    # adjust according to your route output
    assert response.json()["employeeID"] == employee_data["employeeID"]

    get_response = client.get("/employees")
    assert any(emp["employeeID"] == employee_data["employeeID"] for emp in get_response.json())

    client.delete(f"/employees/employee/{employee_data['employeeID']}")

def test_update_employee(client, create_employee):
    updated_data = create_employee.copy()
    updated_data["name"] = "Updated Name"
    response = client.put(f"/employees/employee/{create_employee['employeeID']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_employee(client, employee_data):
    client.post("/employees/employee", json=employee_data)
    response = client.delete(f"/employees/employee/{employee_data['employeeID']}")
    assert response.status_code == 200
    assert response.json().get("message") == "Employee removed successfully"

    assert client.get(f"/employees/employee/{employee_data['employeeID']}").status_code == 404


def test_get_employee_by_id(client, create_employee):
    emp_id = create_employee["employeeID"]
    response = client.get(f"/employees/employee/{emp_id}")
    assert response.status_code == 200
    assert response.json()["employeeID"] == emp_id

def test_get_employee_by_department(client, create_employee):
    department = create_employee["department"]
    response = client.get(f"/employees/department/{department}")
    assert response.status_code == 200
    assert any(emp["employeeID"] == create_employee["employeeID"] for emp in response.json())
