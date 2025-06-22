import { NextResponse } from "next/server"

// Mock study groups data - in real implementation, this would come from Google Sheets "Circle" tab
const mockStudyGroups = [
  {
    id: "1",
    courseName: "Mathematics",
    subtopic: "Calculus and derivatives",
    tutor: {
      name: "Dr. Smith",
      whatsapp: "+6281234567891",
    },
    students: [
      { name: "Alice Johnson", whatsapp: "+6281234567890" },
      { name: "Charlie Brown", whatsapp: "+6281234567894" },
      { name: "Diana Prince", whatsapp: "+6281234567895" },
    ],
    schedule: "Mon, Wed, Fri at 2:00 PM",
    learningMode: "Online",
    maxStudents: 5,
  },
  {
    id: "2",
    courseName: "Physics",
    subtopic: "Quantum mechanics basics",
    tutor: {
      name: "Prof. Davis",
      whatsapp: "+6281234567893",
    },
    students: [
      { name: "Bob Wilson", whatsapp: "+6281234567892" },
      { name: "Eva Martinez", whatsapp: "+6281234567896" },
      { name: "Frank Miller", whatsapp: "+6281234567897" },
      { name: "Grace Lee", whatsapp: "+6281234567898" },
    ],
    schedule: "Tue, Thu at 10:00 AM",
    learningMode: "Online, Offline near ITS",
    maxStudents: 5,
  },
  {
    id: "3",
    courseName: "Programming",
    subtopic: "Python for Data Science",
    tutor: {
      name: "Prof. Johnson",
      whatsapp: "+6281234567899",
    },
    students: [
      { name: "Henry Kim", whatsapp: "+6281234567800" },
      { name: "Ivy Chen", whatsapp: "+6281234567801" },
    ],
    schedule: "Sat at 9:00 AM",
    learningMode: "Online, Chat",
    maxStudents: 5,
  },
]

export async function GET() {
  try {
    // In real implementation, fetch from Google Sheets "Circle" tab
    // const SPREADSHEET_ID = process.env.GOOGLE_SPREADSHEET_ID
    // const SHEET_NAME = "Circle"
    // const API_KEY = process.env.GOOGLE_SHEETS_API_KEY

    // const response = await fetch(
    //   `https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${SHEET_NAME}?key=${API_KEY}`
    // )

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    return NextResponse.json({ groups: mockStudyGroups })
  } catch (error) {
    console.error("Error fetching study groups:", error)
    return NextResponse.json({ error: "Failed to fetch study groups" }, { status: 500 })
  }
}
