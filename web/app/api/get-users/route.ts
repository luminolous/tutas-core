import { NextResponse } from "next/server"

// Mock data - in real implementation, this would come from Google Sheets
const mockUsers = [
  {
    id: "1",
    fullName: "Alice Johnson",
    status: "Student" as const,
    subject: "Mathematics",
    subtopic: "Calculus and derivatives",
    preferredDate: "2024-01-15",
    preferredTime: "14:00",
    learningMode: ["Online", "Two-way discussion"],
    matchingType: "One-on-One",
    whatsappNumber: "+1234567890",
  },
  {
    id: "2",
    fullName: "Dr. Smith",
    status: "Tutor" as const,
    subject: "Mathematics",
    subtopic: "Advanced calculus and mathematical analysis",
    preferredDate: "2024-01-15",
    preferredTime: "15:00",
    learningMode: ["Online", "Offline"],
    matchingType: "One-on-One",
    whatsappNumber: "+1234567891",
  },
  {
    id: "3",
    fullName: "Bob Wilson",
    status: "Student" as const,
    subject: "Physics",
    subtopic: "Quantum mechanics basics",
    preferredDate: "2024-01-16",
    preferredTime: "10:00",
    learningMode: ["Online"],
    matchingType: "Tutas Circle",
    whatsappNumber: "+1234567892",
  },
  {
    id: "4",
    fullName: "Prof. Davis",
    status: "Tutor" as const,
    subject: "Physics",
    subtopic: "Quantum physics and modern physics concepts",
    preferredDate: "2024-01-16",
    preferredTime: "11:00",
    learningMode: ["Online", "Visual & Conceptual"],
    matchingType: "Tutas Circle",
    whatsappNumber: "+1234567893",
  },
]

export async function GET() {
  try {
    // In real implementation, fetch from Google Sheets API
    // const response = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values/${range}?key=${apiKey}`)

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    return NextResponse.json({ users: mockUsers })
  } catch (error) {
    console.error("Error fetching users:", error)
    return NextResponse.json({ error: "Failed to fetch users" }, { status: 500 })
  }
}
