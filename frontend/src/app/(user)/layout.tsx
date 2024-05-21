import Navbar from '@/components/Navbar'
import React from 'react'

export default function UserLayout({ children }: any) {
  return (
    <div className="App 3sm:px-[20px] lmd:px-[20px] 2sm:px-[20px]">
      {children}
    </div>
  )
}
