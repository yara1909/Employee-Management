from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.controller.Employee_controller import fetch_all_employees, create_employee, edit_employee, find_employee_by_id, find_employees_by_department, remove_employee
from app.schemas.Employee_schema import Employee, EmployeeCreate, UpdateEmployee
import datetime
from utils.utils import require_roles

router = APIRouter()
#GET endpoint to list all employees
@router.get("/", response_model=List[Employee], status_code=200, dependencies=[Depends(require_roles(["admin", "user"]))])
def get_employees():
    try:
        return fetch_all_employees()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/employee", response_model=EmployeeCreate, status_code=200, dependencies=[Depends(require_roles(["admin"]))])
def add_employee(employee: EmployeeCreate):
    #Here you would add logic to save the employee to the database
    #For now we will just return the employee data with a success message
    employee.createdAt = datetime.datetime.now()
    try:
        return create_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/employee/{employeeID}", response_model=UpdateEmployee , status_code=200, dependencies=[Depends(require_roles(["admin"]))])
def update_employee(employeeID: str, employee: UpdateEmployee):
    employee.createdAt = datetime.datetime.now()
    try:
        return edit_employee(employeeID, employee)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/employee/{employeeID}", status_code=200, dependencies=[Depends(require_roles(["admin"]))])
def delete_employee(employeeID: str):
    try:
        return remove_employee(employeeID)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/employee/{employeeID}", status_code=200, dependencies=[Depends(require_roles(["admin"]))])
def get_employee(employeeID: str):
    #add logic to retrieve the employee from the database using the employeeID
    try:
        return find_employee_by_id(employeeID)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

                    
@router.get("/department/{department}", response_model=List[Employee], status_code=200, dependencies=[Depends(require_roles(["admin"]))])
def get_employees_by_department(department: str):
    #add logic to retrieve employees from the database based on the department
    try:
        return find_employees_by_department(department)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

