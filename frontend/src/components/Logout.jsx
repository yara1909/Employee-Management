import { useNavigate } from 'react-router-dom'

export default function LogoutButton() {
  const navigate = useNavigate()
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    navigate('/')
  }
  return (
    <button
      onClick={handleLogout}
      className="absolute top-6 right-8 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-semibold shadow"
    >
      Logout
    </button>
  )
}