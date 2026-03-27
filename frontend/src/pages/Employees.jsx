import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Employees() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const role = localStorage.getItem('role')

  useEffect(() => {
    const token = localStorage.getItem('token')
    axios.get('http://localhost:8000/employees/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => {
        setEmployees(res.data)
        setLoading(false)
      })
      .catch(err => {
        setError('Failed to fetch employees')
        setLoading(false)
      })
  }, [])

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
          maxWidth: '700px',
          background: 'white',
          padding: '32px',
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, color: '#2563eb', letterSpacing: '1px' }}>
            Employees
          </h1>
          <button
            onClick={() => navigate('/home')}
            style={{
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              padding: '8px 20px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Home
          </button>
        </div>
        {role === 'admin' && (
          <button
            onClick={() => navigate('/add-employee')}
            style={{
              backgroundColor: '#22c55e',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              padding: '8px 20px',
              fontWeight: 600,
              marginBottom: 20,
              cursor: 'pointer',
            }}
          >
            Add Employee
          </button>
        )}
        {loading && <p style={{ color: '#2563eb' }}>Loading...</p>}
        {error && <p style={{ color: '#dc2626' }}>{error}</p>}
        {!loading && !error && (
          <div style={{ width: '100%', overflowX: 'auto', marginTop: 20 }}>
          <table
              style={{
              width: '100%',
              borderCollapse: 'collapse',
              tableLayout: 'auto',
              }}
          >
            
            <thead>
              <tr>
                <th style={{ textAlign: 'center', padding: '12px', color: '#374151' }}>Employee ID</th>
                <th style={{ textAlign: 'center', padding: '12px', color: '#374151' }}>Name</th>
                <th style={{ textAlign: 'center', padding: '12px', color: '#374151' }}>Email</th>
                <th style={{ textAlign: 'center', padding: '12px', color: '#374151' }}>Position</th>
                <th style={{ textAlign: 'center', padding: '12px', color: '#374151' }}>Department</th>
                <th style={{ textAlign: 'center', padding: '12px', color: '#374151' }}>Status</th>
                {role === 'admin' && <th style={{ padding: '12px' }}>Actions</th>}
              </tr>
            </thead>
            <tbody>
              {employees.length === 0 && (
                <tr>
                  <td colSpan={role === 'admin' ? 7 : 6} style={{ textAlign: 'center', color: '#6b7280', padding: '16px' }}>
                    No employees found.
                  </td>
                </tr>
              )}
              {employees.map((emp, idx) => (
                <tr key={emp.id || emp._id || idx} style={{ background: idx % 2 === 0 ? '#f1f5f9' : 'white' }}>
                  <td style={{ padding: '12px' }}>{emp.name}</td>
                  <td style={{ padding: '12px' }}>{emp.name}</td>
                  <td style={{ padding: '12px' }}>{emp.email}</td>
                  <td style={{ padding: '12px' }}>{emp.position }</td>
                  <td style={{ padding: '12px' }}>{emp.department }</td>
                  <td style={{ padding: '12px' }}>{emp.status }</td>
                  {role === 'admin' && (
                    <td style={{ padding: '12px' }}>
                      <button
                        style={{
                          backgroundColor: '#f59e42',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          padding: '6px 12px',
                          marginRight: 8,
                          cursor: 'pointer',
                        }}
                        onClick={() => navigate('/edit-employee')}
                      >
                        Edit
                      </button>
                      <button
                        style={{
                          backgroundColor: '#dc2626',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          padding: '6px 12px',
                          cursor: 'pointer',
                        }}
                        onClick={() => navigate('/delete-employee')}
                      >
                        Delete
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        )}
      </div>
    </div>
  )
}