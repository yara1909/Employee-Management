export default function Home() {
  const role = localStorage.getItem('role')

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">Dashboard</h1>
      <p className="text-gray-600 mb-6">Welcome to the Employee Management System</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700">Role</h2>
          <p className="text-2xl font-bold text-blue-600 mt-2">{role || 'Unknown'}</p>
        </div>

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700">Employees</h2>
          <p className="text-2xl font-bold text-green-600 mt-2">--</p>
        </div>

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700">Status</h2>
          <p className="text-2xl font-bold text-purple-600 mt-2">Active</p>
        </div>
      </div>
    </div>
  )
}