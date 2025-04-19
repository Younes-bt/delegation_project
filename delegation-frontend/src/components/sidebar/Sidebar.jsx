function Sidebar() {
    return (
      <aside className="w-64 bg-gray-100 p-4 min-h-screen">
        <h2 className="text-xl font-semibold mb-4">Sidebar</h2>
        <ul className="space-y-2">
          <li><a href="/admin/dashboard" className="text-blue-600 hover:underline">Dashboard</a></li>
          {/* Add more nav items here based on role */}
        </ul>
      </aside>
    )
  }
  
  export default Sidebar
  