import pytest
import os, sys
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.app.main1 import app
from fastapi.testclient import TestClient

client = TestClient(app)

def make_test_employee():
    eid = f"TEST-{uuid.uuid4().hex[:8]}"
    return {
        "employeeID": eid,
        "name": "John Doe",
        "email": f"{eid}@example.com",
        "department": "Engineering",
        "position": "Software Engineer",
        "status": "active",
        "createdAt": "2026-03-24T12:00:00Z",
    }

#Test case for the GET /employees endpoint to list all employees
def test_get_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    #Check if the response contains at least one employee
    assert any(emp["name"] == "John Doe" for emp in response.json())

# Test case for the GET /employees/department/{department} endpoint
def test_get_employee_by_department():
    response = client.get("/employees/department/Finance")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(emp["department"] == "Finance" for emp in response.json())

# Test case for the GET /employees/employee/{employeeID} endpoint
def test_get_employee_by_id():
    employees = client.get("/employees").json()
    assert employees, "Need at least one employee in DB"
    emp_id = employees[0]["employeeID"]

    response = client.get(f"/employees/employee/{emp_id}")
    assert response.status_code == 200
    obj = response.json()
    assert obj["employeeID"] == emp_id


# Test case for the PUT /employees/employee/{employeeID} endpoint
def test_update_employee():
    emp = make_test_employee()
    client.post("/employees/employee", json=emp)
    emp["name"] = "John Updated"
    response = client.put(f"/employees/employee/{emp['employeeID']}", json=emp)
    assert response.status_code == 200
    assert response.json()["name"] == "John Updated"
    client.delete(f"/employees/employee/{emp['employeeID']}")

def test_delete_employee():
    emp = make_test_employee()
    client.post("/employees/employee", json=emp)
    response = client.delete(f"/employees/employee/{emp['employeeID']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee removed successfully"
    assert client.get(f"/employees/employee/{emp['employeeID']}").status_code == 404