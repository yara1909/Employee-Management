from app.config.database import employees_collection
from app.model.Employee_model import get_all_employees, add_employee, update_employee, get_employee_by_department, get_employee_by_id, delete_employee
from app.schemas.Employee_schema import Employee, EmployeeResponse, EmployeeCreate, UpdateEmployee


#GET request for all employees
def fetch_all_employees():
    employees= get_all_employees()
    return [Employee(**emp) for emp in employees]

def create_employee(employee_data: EmployeeCreate):
    #check if duplicate employeeID or email exists
    existing_employees = get_all_employees()
    
    if any(emp["employeeID"] == employee_data.employeeID for emp in existing_employees):
        raise ValueError("Employee with this ID already exists")
    add_employee(employee_data.model_dump()) #convert Pydantic model to dict before inserting into database

    return Employee(**employee_data.model_dump())

def edit_employee(employee_id: str, employee_data):
    existing_employee = employees_collection.find_one({"employeeID": employee_id})

    if not existing_employee:
        raise ValueError("Employee with this ID does not exist")

    update_employee(employee_id, employee_data.model_dump())
    updated = get_employee_by_id(employee_id)

    return Employee(**updated)

def remove_employee(employee_id: str):
    existing_employee = employees_collection.find_one({"employeeID": employee_id})

    if not existing_employee:
        raise ValueError("Employee with this ID does not exist")
    delete_result = delete_employee(employee_id)
    return {
        "message": "Employee removed successfully", "deleted_count": delete_result.deleted_count}

def find_employee_by_id(employee_id: str):
    employee = get_employee_by_id(employee_id)
    
    if not employee:
        raise ValueError("Employee with this ID does not exist")
    
    employee["_id"] = str(employee["_id"])  
    return employee

def find_employees_by_department(department: str):
    employees = get_employee_by_department(department)

    if not employees:
        raise ValueError("No employees found in this department")
    
    for employee in employees:
        employee["_id"] = str(employee["_id"])  

    return employees
