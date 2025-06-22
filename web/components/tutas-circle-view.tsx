"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Student {
  name: string
  whatsapp: string
}

interface StudyGroup {
  id: string
  courseName: string
  subtopic: string
  tutor: {
    name: string
    whatsapp: string
  }
  students: Student[]
  schedule: string
  learningMode: string
  maxStudents: number
}

const TutasCircleView = () => {
  const [studyGroups, setStudyGroups] = useState<StudyGroup[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    fetchStudyGroups()
  }, [])

  const fetchStudyGroups = async () => {
    setLoading(true)
    setError("")
    try {
      const response = await fetch("http://localhost:5000/tutas-circle")

      if (response.ok) {
        const data = await response.json()
        setStudyGroups(data.study_groups || [])
      } else {
        setError("Failed to fetch data from server")
      }
    } catch (error) {
      console.error("Error fetching study groups:", error)
      setError("Error connecting to server. Please check if the Flask backend is running.")
    }
    setLoading(false)
  }

  if (loading) {
    return (
      <Card className="bg-black border-gray-700">
        <CardContent className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
          <div className="text-gray-300">Loading study groups...</div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="bg-black border-gray-700">
        <CardContent className="text-center py-8">
          <div className="text-red-400 mb-4">⚠️ {error}</div>
          <Button onClick={fetchStudyGroups} className="btn-secondary">
            Try Again
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-white">Active Study Groups ({studyGroups.length})</h2>
        <Button onClick={fetchStudyGroups} className="btn-secondary">
          🔄 Refresh Groups
        </Button>
      </div>

      {studyGroups.length === 0 ? (
        <Card className="bg-black border-gray-700">
          <CardContent className="text-center py-12">
            <div className="text-gray-400 text-lg">No study groups available yet</div>
            <p className="text-gray-500 mt-2">
              Groups will appear here once students register for Tutas Circle and are grouped by the system.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {studyGroups.map((group) => (
            <Card key={group.id} className="bg-black border-gray-700">
              <CardHeader>
                <CardTitle className="text-lg text-white">{group.courseName}</CardTitle>
                <p className="text-gray-400 text-sm">{group.subtopic}</p>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Tutor Section */}
                <div className="border-b border-gray-700 pb-3">
                  <h4 className="font-semibold text-white mb-2">👨‍🏫 Tutor</h4>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">{group.tutor.name}</span>
                    <a
                      href={`https://wa.me/${group.tutor.whatsapp.replace(/[^0-9]/g, "")}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="whatsapp-btn"
                    >
                      WhatsApp
                    </a>
                  </div>
                </div>

                {/* Students Section */}
                <div>
                  <h4 className="font-semibold text-white mb-2">
                    👥 Students ({group.students.length}/{group.maxStudents})
                  </h4>
                  <div className="space-y-2">
                    {group.students.map((student, index) => (
                      <div key={index} className="flex items-center justify-between text-sm">
                        <span className="text-gray-300">{student.name}</span>
                        <a
                          href={`https://wa.me/${student.whatsapp.replace(/[^0-9]/g, "")}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="contact-btn"
                        >
                          WhatsApp
                        </a>
                      </div>
                    ))}
                    {/* Show available slots */}
                    {Array.from({ length: group.maxStudents - group.students.length }).map((_, index) => (
                      <div key={`slot-${index}`} className="text-sm text-gray-500 italic">
                        📍 Available slot
                      </div>
                    ))}
                  </div>
                </div>

                {/* Group Details */}
                <div className="pt-3 border-t border-gray-700 space-y-2 text-sm">
                  <div>
                    <span className="text-gray-400">📅 Schedule: </span>
                    <span className="text-gray-300">{group.schedule}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">💻 Mode: </span>
                    <span className="text-gray-300">{group.learningMode}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default TutasCircleView
