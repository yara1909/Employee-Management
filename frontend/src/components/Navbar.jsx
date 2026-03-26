import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const role = localStorage.getItem('role')

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-xl font-bold text-blue-600">EMS</h1>
      </div>

      <div className="flex items-center gap-4">
        <Link to="/" className="text-gray-700 hover:text-blue-600">
          Home
        </Link>
        <Link to="/employees" className="text-gray-700 hover:text-blue-600">
          Employees
        </Link>
        {role === 'admin' && (
          <Link to="/employees/add" className="text-gray-700 hover:text-blue-600">
            Add Employee
          </Link>
        )}
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
        >
          Logout
        </button>
      </div>
    </nav>
  )
}