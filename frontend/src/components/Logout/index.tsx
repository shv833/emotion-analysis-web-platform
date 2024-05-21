'use client'
import { AuthActions } from '@/app/(auth)/utils'
import { useRouter } from 'next/navigation'
const { logout, removeTokens } = AuthActions()

const Logout = () => {
  const router = useRouter()

  const handleLogout = () => {
    logout()
      .res(() => {
        removeTokens()

        router.push('/')
      })
      .catch(() => {
        removeTokens()
        router.push('/')
      })
  }
  return (
    <div>
      <button
        onClick={handleLogout}
        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
      >
        Log out
      </button>
    </div>
  )
}

export default Logout;
