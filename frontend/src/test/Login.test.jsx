import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import axios from 'axios'
import { LoginForm } from '../pages/Login'

vi.mock('axios')

describe('Login page', () => {
  let mockNavigate

  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    mockNavigate = vi.fn()
  })

  it('renders the login form correctly', () => {
    render(<LoginForm navigate={mockNavigate} />)

    expect(screen.getByLabelText(/username/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument()
  })

  it('validates required fields', async () => {
    const user = userEvent.setup()
    render(<LoginForm navigate={mockNavigate} />)

    await user.click(screen.getByRole('button', { name: /login/i }))

    expect(screen.getByText('Username is required')).toBeInTheDocument()
    expect(screen.getByText('Password is required')).toBeInTheDocument()
    expect(axios.post).not.toHaveBeenCalled()
  })

  it('displays an error message when login fails', async () => {
    const user = userEvent.setup()

    axios.post.mockRejectedValue({
      response: {
        data: {
          detail: 'Invalid credentials',
        },
      },
    })

    render(<LoginForm navigate={mockNavigate} />)

    await user.type(screen.getByLabelText(/username/i), 'test')
    await user.type(screen.getByLabelText(/password/i), 'wrongpassword')
    await user.click(screen.getByRole('button', { name: /login/i }))

    expect(await screen.findByText('Invalid credentials')).toBeInTheDocument()
    expect(localStorage.getItem('token')).toBeNull()
    expect(localStorage.getItem('role')).toBeNull()
    expect(mockNavigate).not.toHaveBeenCalled()
  })

  it('successful login calls the backend and stores JWT and role in localStorage', async () => {
    const user = userEvent.setup()

    axios.post.mockResolvedValue({
      data: {
        access_token: 'fake-jwt-token',
        role: 'admin',
      },
    })

    render(<LoginForm navigate={mockNavigate} />)

    await user.type(screen.getByLabelText(/username/i), 'test')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/auth/users/login',
        {
          username: 'test',
          password: 'password123',
        }
      )
    })

    expect(localStorage.getItem('token')).toBe('fake-jwt-token')
    expect(localStorage.getItem('role')).toBe('admin')
  })

  it('redirects to home page on successful login', async () => {
    const user = userEvent.setup()

    axios.post.mockResolvedValue({
      data: {
        access_token: 'fake-jwt-token',
        role: 'user',
      },
    })

    render(<LoginForm navigate={mockNavigate} />)

    await user.type(screen.getByLabelText(/username/i), 'user')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/')
    })
  })
})