import { useAuth } from '../features/auth/useAuth'

export function DashboardPage() {
  const { user, logout } = useAuth()

  return (
    <section id="center">
      <h1>Dashboard</h1>
      <p>Welcome{user?.first_name ? `, ${user.first_name}` : ''}. This is a placeholder.</p>
      <button type="button" onClick={() => logout()}>
        Log out
      </button>
    </section>
  )
}
