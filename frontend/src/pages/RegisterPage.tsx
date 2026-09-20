import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ApiError } from '../api/client'
import { useAuth } from '../features/auth/useAuth'
import { RegisterForm } from '../features/auth/RegisterForm'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(email: string, password: string, firstName: string, lastName: string) {
    setError(null)
    try {
      await register(email, password, firstName, lastName)
      navigate('/dashboard', { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Registration failed')
    }
  }

  return (
    <section id="center">
      <h1>Register</h1>
      {error && <p className="form-error">{error}</p>}
      <RegisterForm onSubmit={handleSubmit} />
      <p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </section>
  )
}
