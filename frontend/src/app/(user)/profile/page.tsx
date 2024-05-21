'use client'

import useSWR from 'swr'
import { fetcher } from '@/app/fetcher'

export default function Profile() {
  const { data: user } = useSWR('/auth/users/me', fetcher)

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-1/3 text-center text-black">
        <h1 className="text-2xl font-bold mb-4">Hi, {user?.username}!</h1>
        <p className="mb-4">Your account details:</p>
        <ul className="mb-4">
          <li>Username: {user?.username}</li>
          <li>Email: {user?.email}</li>
        </ul>
      </div>
    </div>
  )
}
