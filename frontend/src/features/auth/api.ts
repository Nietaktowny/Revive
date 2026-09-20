import { request, setToken } from '../../api/client'

export interface User {
  id: number
  email: string
  username: string
  first_name: string | null
  last_name: string | null
  is_active: boolean
}

export async function login(email: string, password: string): Promise<void> {
  const form = new URLSearchParams({ username: email, password })
  const { access_token } = await request<{ access_token: string; token_type: string }>(
    "/login",
    { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: form }
  )
  setToken(access_token)
}

export async function logout(): Promise<void> {
  try {
    await request("/logout", { method: "POST" })
  } finally {
    setToken(null)
  }
}

export function currentUser(): Promise<User> {
  return request<User>("/current_user", { method: "POST" })
}

export function registerUser(email: string, password: string, firstName: string, lastName: string): Promise<{ status: string }> {
  const params = new URLSearchParams({ email, password, first_name: firstName, last_name: lastName })
  return request(`/add_user?${params}`, { method: "POST" })
}
