import { useState } from 'react';

export default function AddEmployee() {
  const [employees, setEmployees] = useState([]);
const [showForm, setShowForm] = useState(false);

const [newEmployee, setNewEmployee] = useState({
  employeeID: '',
  name: '',
  email: '',
  position: '',
  department: '',
  status: '',
});

const handleInputChange = (e) => {
  const { name, value } = e.target;
  setNewEmployee((prev) => ({ ...prev, [name]: value }));
};
const handleAddEmployee = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch('http://127.0.0.1:8000/employees/employee', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newEmployee),
    });

    if (!response.ok) {
      throw new Error('Failed to add employee');
    }

    const data = await response.json();

    setEmployees((prev) => [...prev, data]);

    setNewEmployee({
      employeeID: '',
      name: '',
      email: '',
      position: '',
      department: '',
      status: '',
    });

    setShowForm(false);
  } catch (error) {
    console.error('Error adding employee:', error);
  }
};
}
