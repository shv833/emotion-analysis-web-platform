'use client'

import React, { useState, useEffect } from 'react'
import { fetcher } from '@/app/fetcher'
import Link from 'next/link'

interface Group {
  id: number
  title: string
  description: string
}

export default function Groups() {
  const [groups, setGroups] = useState<Group[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadGroups = async () => {
      try {
        const data = await fetcher('/groups/groups/')

        setGroups(data)
      } catch (err) {
        setError('Failed to load groups')
      } finally {
        setLoading(false)
      }
    }

    loadGroups()
  }, [])

  if (loading) {
    return <p>Loading...</p>
  }

  if (error) {
    return <p>{error}</p>
  }

  return (
    <div className="p-5">
      <h2 className="text-2xl font-bold mb-4">My Groups</h2>
      {groups?.length === 0 ? (
        <p>No groups available.</p>
      ) : (
        groups.map((group: Group) => (
          <div key={group.id} className="border border-gray-300 p-4 mb-4">
            <h3 className="text-xl font-semibold">{group.title}</h3>
            <p className="text-gray-700">{group.description}</p>
            <Link
              href={`/groups/${group.id}`}
              className="inline-block mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
              passHref
            >
              View Details
            </Link>
          </div>
        ))
      )}
    </div>
  )
}
