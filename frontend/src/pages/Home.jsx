import { useNavigate } from 'react-router-dom'
import LogoutButton from '../components/Logout'

export default function Home() {
  const role = localStorage.getItem('role')
  const navigate = useNavigate()

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #2563eb 0%, #1e293b 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'Inter, sans-serif',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '500px',
          background: 'white',
          padding: '32px',
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, color: '#2563eb', letterSpacing: '1px' }}>
            Dashboard
          </h1>
          <LogoutButton />
        </div>
        <p style={{ color: '#374151', marginBottom: 24 }}>
          Welcome back! Manage your employees and view your role below.
        </p>
        <div style={{ marginBottom: 24 }}>
          <div style={{
            background: '#f1f5f9',
            borderRadius: '10px',
            padding: '18px',
            marginBottom: 12,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <span style={{ fontWeight: 600, color: '#374151' }}>Your Role:</span>
            <span style={{
              background: '#2563eb',
              color: 'white',
              borderRadius: '8px',
              padding: '8px 20px',
              fontWeight: 700,
              fontSize: '1.1rem'
            }}>
              {role || 'Unknown'}
            </span>
          </div>
        </div>
        <button
          onClick={() => navigate('/employees')}
          style={{
            width: '100%',
            backgroundColor: '#22c55e',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            padding: '12px 0',
            fontWeight: 600,
            fontSize: '1rem',
            cursor: 'pointer',
            marginTop: 8,
            transition: 'background 0.2s',
          }}
        >
          View Employees
        </button>
      </div>
    </div>
  )
}