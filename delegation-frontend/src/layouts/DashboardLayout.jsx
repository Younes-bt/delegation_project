
import Sidebar from '../components/Sidebar/Sidebar'
import { Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar/Navbar'

function DashboardLayout() {
  return (
    <>
    <Navbar />
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
    </>
  )
}

export default DashboardLayout
