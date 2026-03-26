from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets

app = FastAPI()

# -----------------------------
# Simple in-memory employee data
# -----------------------------
employees = [
    {"id": 1, "name": "John Doe", "position": "Manager"},
    {"id": 2, "name": "Jane Smith", "position": "Developer"}
]

# -----------------------------
# Hardcoded users for auth
# -----------------------------
users = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": "user123",
        "role": "user"
    }
}

# Create HTTP Basic auth object
security = HTTPBasic()

# -----------------------------
# Pydantic model for employees
# -----------------------------
class Employee(BaseModel):
    id: int
    name: str
    position: str

# -----------------------------
# Authentication helper
# -----------------------------
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    user = users.get(username)

    # Check if user exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Check password safely
    correct_password = secrets.compare_digest(password, user["password"])
    correct_username = secrets.compare_digest(username, user["username"])

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user

# -----------------------------
# Admin-only helper
# -----------------------------
def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():
    return {"message": "Employee API is running"}

# Authenticated users can access
@app.get("/employees")
def get_employees(current_user: dict = Depends(get_current_user)):
    return employees

# Optional: also protect GET by ID for authenticated users
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, current_user: dict = Depends(get_current_user)):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")

# Admin only
@app.post("/employees")
def add_employee(employee: Employee, current_user: dict = Depends(get_admin_user)):
    for emp in employees:
        if emp["id"] == employee.id:
            raise HTTPException(status_code=400, detail="Employee with this ID already exists")
    employees.append(employee.dict())
    return {"message": "Employee added successfully", "employee": employee}

# Admin only
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated_employee: Employee, current_user: dict = Depends(get_admin_user)):
    for index, employee in enumerate(employees):
        if employee["id"] == employee_id:
            employees[index] = updated_employee.dict()
            return {"message": "Employee updated successfully", "employee": updated_employee}
    raise HTTPException(status_code=404, detail="Employee not found")

# Admin only
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, current_user: dict = Depends(get_admin_user)):
    for index, employee in enumerate(employees):
        if employee["id"] == employee_id:
            deleted_employee = employees.pop(index)
            return {"message": "Employee deleted successfully", "employee": deleted_employee}
    raise HTTPException(status_code=404, detail="Employee not found")