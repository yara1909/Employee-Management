import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate, useLocation } from 'react-router-dom'

export function LoginForm({ navigate }) {
  const location = useLocation()
  const from = location.state?.from?.pathname || '/home'

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })

  const [errors, setErrors] = useState({
    username: '',
    password: '',
    server: '',
  })

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
    setErrors((prev) => ({
      ...prev,
      [name]: '',
      server: '',
    }))
  }

  const validateForm = () => {
    const newErrors = {
      username: '',
      password: '',
      server: '',
    }
    let isValid = true
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required'
      isValid = false
    }
    if (!formData.password.trim()) {
      newErrors.password = 'Password is required'
      isValid = false
    }
    setErrors(newErrors)
    return isValid
  }

  const handleSubmit = async (event) => {
  event.preventDefault()
  if (!validateForm()) return

  try {
    const params = new URLSearchParams()
    params.append('username', formData.username)
    params.append('password', formData.password)

    // FIX: axios.post call must be closed before using response
    const response = await axios.post(
      'http://localhost:8000/auth/users/login',
      params
    )

    console.log('Response from server:', response.data)

    const token = response?.data?.access_token || response?.data?.token
    const role = response?.data?.role

    if (token) localStorage.setItem('token', token)
    if (role) localStorage.setItem('role', role)

    console.log('Navigating to /home')
    navigate(from, { replace: true })
  } catch (error) {
    const message =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      'Login failed'
    setErrors((prev) => ({
      ...prev,
      server: message,
    }))
  }
}

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
          maxWidth: '400px',
          background: 'white',
          padding: '32px',
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
        }}
      >
        <h1
          style={{
            textAlign: 'center',
            fontSize: '2rem',
            fontWeight: 700,
            marginBottom: '24px',
            color: '#2563eb',
            letterSpacing: '1px',
          }}
        >
          Employee Management Login
        </h1>
        <form onSubmit={handleSubmit} noValidate>
          <div style={{ marginBottom: '18px' }}>
            <label
              htmlFor="username"
              style={{
                display: 'block',
                marginBottom: '6px',
                fontWeight: 500,
                color: '#374151',
              }}
            >
              Username
            </label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="Enter your username"
              value={formData.username}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '10px 12px',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                fontSize: '15px',
                boxSizing: 'border-box',
                outline: errors.username ? '2px solid #dc2626' : 'none',
              }}
            />
            {errors.username && (
              <p style={{ marginTop: '6px', fontSize: '14px', color: '#dc2626' }}>
                {errors.username}
              </p>
            )}
          </div>
          <div style={{ marginBottom: '18px' }}>
            <label
              htmlFor="password"
              style={{
                display: 'block',
                marginBottom: '6px',
                fontWeight: 500,
                color: '#374151',
              }}
            >
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '10px 12px',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                fontSize: '15px',
                boxSizing: 'border-box',
                outline: errors.password ? '2px solid #dc2626' : 'none',
              }}
            />
            {errors.password && (
              <p style={{ marginTop: '6px', fontSize: '14px', color: '#dc2626' }}>
                {errors.password}
              </p>
            )}
          </div>
          {errors.server && (
            <p style={{ marginBottom: '16px', fontSize: '14px', color: '#dc2626', textAlign: 'center' }}>
              {errors.server}
            </p>
          )}
          <button
            type="submit"
            style={{
              width: '100%',
              padding: '12px 0',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: 600,
              cursor: 'pointer',
              marginTop: '8px',
              transition: 'background 0.2s',
            }}
          >
            Login
          </button>
        </form>
      </div>
    </div>
  )
}

export default function Login() {
  const navigate = useNavigate()
  return <LoginForm navigate={navigate} />
}