import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export function LoginForm({ navigate }) {
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
      const response = await axios.post('http://localhost:8000/auth/users/login', {
        username: formData.username,
        password: formData.password,
      })

      const token = response?.data?.access_token || response?.data?.token
      const role = response?.data?.role

      if (token) localStorage.setItem('token', token)
      if (role) localStorage.setItem('role', role)

      navigate('/')
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
        backgroundColor: '#f3f4f6',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '16px',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '420px',
          backgroundColor: 'white',
          padding: '24px',
          borderRadius: '12px',
          boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
        }}
      >
        <h1
          style={{
            textAlign: 'center',
            fontSize: '28px',
            fontWeight: 'bold',
            marginBottom: '24px',
            color: '#111827',
          }}
        >
          Login
        </h1>

        <form onSubmit={handleSubmit} noValidate>
          <div style={{ marginBottom: '16px' }}>
            <label
              htmlFor="username"
              style={{
                display: 'block',
                marginBottom: '6px',
                fontSize: '14px',
                fontWeight: '500',
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
                fontSize: '14px',
                boxSizing: 'border-box',
              }}
            />
            {errors.username && (
              <p style={{ marginTop: '6px', fontSize: '14px', color: '#dc2626' }}>
                {errors.username}
              </p>
            )}
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label
              htmlFor="password"
              style={{
                display: 'block',
                marginBottom: '6px',
                fontSize: '14px',
                fontWeight: '500',
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
                fontSize: '14px',
                boxSizing: 'border-box',
              }}
            />
            {errors.password && (
              <p style={{ marginTop: '6px', fontSize: '14px', color: '#dc2626' }}>
                {errors.password}
              </p>
            )}
          </div>

          {errors.server && (
            <p style={{ marginBottom: '16px', fontSize: '14px', color: '#dc2626' }}>
              {errors.server}
            </p>
          )}

          <button
            type="submit"
            style={{
              width: '100%',
              padding: '10px 16px',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
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
  console.log('Login component rendered')
  const navigate = useNavigate()
  return <LoginForm navigate={navigate} />
}