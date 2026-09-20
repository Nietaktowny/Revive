import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ApiError } from '../api/client'
import { useAuth } from '../features/auth/useAuth'
import { LoginForm } from '../features/auth/LoginForm'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(email: string, password: string) {
    setError(null)
    try {
      await login(email, password)
      navigate('/dashboard', { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Login failed')
    }
  }

  return (
    <section id="center">
      <h1>Log in</h1>
      {error && <p className="form-error">{error}</p>}
      <LoginForm onSubmit={handleSubmit} />
      <p>
        No account? <Link to="/register">Register</Link>
      </p>
    </section>
  )
}
