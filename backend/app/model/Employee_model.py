from app.config.database import employees_collection
from app.schemas.Employee_schema import Employee, EmployeeResponse

#GET all employees from the database
def get_all_employees():
    employees = list(employees_collection.find())
    return list(employees_collection.find({}, {"_id": 0}))

#POST request to add a new employee
def add_employee(employee_data):
    return employees_collection.insert_one(employee_data)

#PUT request to update an existing employee
def update_employee(employeeID, employee_data):
    return employees_collection.update_one({"employeeID": employeeID}, {"$set": employee_data})

#DELETE request to remove an employee
def delete_employee(employeeID):
    return employees_collection.delete_one({"employeeID": employeeID})

#GET request to find an employee by ID
def get_employee_by_id(employeeID):
    return employees_collection.find_one({"employeeID": employeeID})

#GET request to find employees by department
def get_employee_by_department(department):
    return list(employees_collection.find({"department": department}))
