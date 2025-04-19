import { BrowserRouter, Routes, Route } from 'react-router-dom'
import PublicLayout from './layouts/PublicLayout'
import DashboardLayout from './layouts/DashboardLayout'

import Home from './pages/home'
import Login from './pages/login'

import AdminDashboard from './pages/dashboard/AdminDashboard'
import CenterDashboard from './pages/dashboard/CenterDashboard'
import TeacherDashboard from './pages/dashboard/TeacherDashboard'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
        </Route>

        {/* Dashboard Routes */}
        <Route element={<DashboardLayout />}>
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/center/dashboard" element={<CenterDashboard />} />
          <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

