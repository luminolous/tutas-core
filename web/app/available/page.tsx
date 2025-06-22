import AvailableUsersTable from "@/components/available-users-table"

export default function AvailablePage() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4 text-white">Students & Tutors Matched</h1>
        <p className="text-gray-300 text-lg">Browse matched 1-on-1 students and tutors</p>
      </div>
      <AvailableUsersTable />
    </div>
  )
}
