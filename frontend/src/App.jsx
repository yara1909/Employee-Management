import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'

function Home() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold">Home Page</h1>
      <p className="mt-2 text-gray-600">You are logged in.</p>
    </div>
  )
}

export default function App() {
  console.log('App component rendered')
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<Home />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}