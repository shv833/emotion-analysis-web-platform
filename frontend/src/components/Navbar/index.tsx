import Link from 'next/link'
import Logout from '../Logout'

const Navbar = () => {
  return (
    <header className="bg-gray-800 text-white">
      <nav className="container mx-auto p-4 flex justify-between items-center">
        <div className="flex space-x-4">
          <Link href="/main" className="hover:text-gray-400">
            Main
          </Link>
          <Link href="/groups" className="hover:text-gray-400">
            Groups
          </Link>
          <Link href="/courses" className="hover:text-gray-400">
            Courses
          </Link>
          <Link href="/profile" className="hover:text-gray-400">
            Profile
          </Link>
        </div>
        <Logout />
      </nav>
    </header>
  )
}

export default Navbar
