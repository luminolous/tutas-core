"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface MatchedPair {
  id: string
  tutorName: string
  studentName: string
  subject: string
  subtopic: string
  schedule: string
  learningMode: string
  tutorWhatsapp: string
  studentWhatsapp: string
}

const AvailableUsersTable = () => {
  const [matchedPairs, setMatchedPairs] = useState<MatchedPair[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [error, setError] = useState("")

  useEffect(() => {
    fetchMatchedPairs()
  }, [])

  const fetchMatchedPairs = async () => {
    setLoading(true)
    setError("")
    try {
      const response = await fetch("http://localhost:5000/available")

      if (response.ok) {
        const data = await response.json()
        setMatchedPairs(data.matched_pairs || [])
      } else {
        setError("Failed to fetch data from server")
      }
    } catch (error) {
      console.error("Error fetching matched pairs:", error)
      setError("Error connecting to server. Please check if the Flask backend is running.")
    }
    setLoading(false)
  }

  const filteredPairs = matchedPairs.filter((pair) =>
    Object.values(pair).some((value) => value.toString().toLowerCase().includes(searchTerm.toLowerCase())),
  )

  if (loading) {
    return (
      <Card className="bg-black border-gray-700">
        <CardContent className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
          <div className="text-gray-300">Loading matched pairs...</div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="bg-black border-gray-700">
        <CardContent className="text-center py-8">
          <div className="text-red-400 mb-4">⚠️ {error}</div>
          <Button onClick={fetchMatchedPairs} className="btn-secondary">
            Try Again
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Search and Refresh */}
      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <input
          type="text"
          placeholder="Search by name, subject, or topic..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input-field flex-1"
        />
        <Button onClick={fetchMatchedPairs} className="btn-secondary">
          🔄 Refresh
        </Button>
      </div>

      {/* Matched Pairs Table */}
      <Card className="bg-black border-gray-700">
        <CardHeader>
          <CardTitle className="text-xl text-white">Matched 1-on-1 Pairs ({filteredPairs.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {matchedPairs.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-gray-400 text-lg mb-2">No matched pairs available yet</div>
              <p className="text-gray-500">
                Pairs will appear here once students and tutors are matched by the system.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-white">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4">Tutor Name</th>
                    <th className="text-left py-3 px-4">Student Name</th>
                    <th className="text-left py-3 px-4">Subject</th>
                    <th className="text-left py-3 px-4">Subtopic</th>
                    <th className="text-left py-3 px-4">Schedule</th>
                    <th className="text-left py-3 px-4">Learning Mode</th>
                    <th className="text-left py-3 px-4">Contact</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPairs.map((pair) => (
                    <tr key={pair.id} className="border-b border-gray-800 hover:bg-gray-800">
                      <td className="py-3 px-4 font-medium">{pair.tutorName}</td>
                      <td className="py-3 px-4 font-medium">{pair.studentName}</td>
                      <td className="py-3 px-4">{pair.subject}</td>
                      <td className="py-3 px-4 max-w-xs truncate">{pair.subtopic}</td>
                      <td className="py-3 px-4">{pair.schedule}</td>
                      <td className="py-3 px-4">{pair.learningMode}</td>
                      <td className="py-3 px-4">
                        <div className="flex gap-2">
                          <a
                            href={`https://wa.me/${pair.tutorWhatsapp.replace(/[^0-9]/g, "")}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="whatsapp-btn"
                            title="Contact Tutor"
                          >
                            Tutor
                          </a>
                          <a
                            href={`https://wa.me/${pair.studentWhatsapp.replace(/[^0-9]/g, "")}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="contact-btn"
                            title="Contact Student"
                          >
                            Student
                          </a>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {filteredPairs.length === 0 && searchTerm && (
                <div className="text-center py-8 text-gray-400">No pairs match your search criteria.</div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default AvailableUsersTable
