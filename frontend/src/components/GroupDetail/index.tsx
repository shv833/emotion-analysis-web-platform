// components/GroupDetail.tsx
import React from 'react'
import Link from 'next/link'

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
interface GroupDetailProps {
  group: Group
}

const GroupDetail: React.FC<GroupDetailProps> = ({ group }) => {
  return (
    <div className="p-5">
      <h1 className="text-3xl font-bold mb-4">{group.title}</h1>
      <p className="text-gray-700">{group.description}</p>
      <p className="text-gray-700">Course: {group.course}</p>
      <p className="text-gray-700">
        Teacher: {group.teacher.first_name} {group.teacher.last_name}
      </p>
      <p className="text-gray-700">
        Supervisor: {group.supervisor.first_name} {group.supervisor.last_name}
      </p>
      <p className="text-gray-700">
        Date Started: {new Date(group.date_started).toLocaleDateString()}
      </p>

      <h2 className="text-2xl font-bold mt-4">Students</h2>
      <ul className="list-disc list-inside">
        {group.students.map((student: any) => (
          <li key={student.id} className="text-gray-700">
            {student.student.first_name} {student.student.last_name} (
            {student.student.username})
          </li>
        ))}
      </ul>

      <Link
        href="/groups"
        className="inline-block mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
      >
        Back to Groups
      </Link>
    </div>
  )
}

export default GroupDetail
