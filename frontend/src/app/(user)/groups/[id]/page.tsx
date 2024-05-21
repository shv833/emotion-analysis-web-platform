'use client'

import React, { useState, useEffect } from 'react'
import { fetcher } from '@/app/fetcher'
import GroupDetail from '@/components/GroupDetail'
interface User {
  id: number
  avatar: string
  username: string
  first_name: string
  last_name: string
}

interface GroupStudent {
  id: number
  student: User
  is_active: boolean
}

interface Group {
  id: number
  title: string
  date_started: string
  course: string
  teacher: User
  supervisor: User
  description: string
  students: GroupStudent[]
}
type Props = {
  params: { id: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

const GroupDetailPage = ({ params }: Props) => {
  const [group, setGroup] = useState<Group | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadGroup = async () => {
      try {
        const data = await fetcher(`/groups/groups/${params.id}/`)

        setGroup(data)
      } catch (err) {
        setError('Failed to load group details')
      } finally {
        setLoading(false)
      }
    }

    loadGroup()
  }, [params.id])

  if (loading) {
    return <p>Loading...</p>
  }

  if (error) {
    return <p>{error}</p>
  }

  if (!group) {
    return <p>Group not found</p>
  }

  return <GroupDetail group={group} />
}

export default GroupDetailPage
