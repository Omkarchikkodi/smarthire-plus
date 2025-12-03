export default function Sidebar() {
  return (
    <div className="w-64 bg-white h-screen shadow p-4">
      <h2 className="font-semibold mb-4">Menu</h2>
      <ul className="space-y-2">
        <li className="cursor-pointer hover:text-blue-600">Dashboard</li>
        <li className="cursor-pointer hover:text-blue-600">Recommendations</li>
      </ul>
    </div>
  );
}
