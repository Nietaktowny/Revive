import { useEffect, useState, type ReactNode } from 'react'
import { getToken } from '../../api/client'
import * as authApi from './api'
import type { User } from './api'
import { AuthContext } from './context'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(() => Boolean(getToken()))

  useEffect(() => {
    if (!getToken()) {
      return
    }
    authApi
      .currentUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  async function login(email: string, password: string) {
    await authApi.login(email, password)
    setUser(await authApi.currentUser())
  }

  async function register(email: string, password: string, firstName: string, lastName: string) {
    await authApi.registerUser(email, password, firstName, lastName)
    await login(email, password)
  }

  async function logout() {
    await authApi.logout()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
