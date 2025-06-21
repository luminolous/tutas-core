import { NextResponse } from "next/server"

// Mock data - in real implementation, this would come from Google Sheets "Output" tab
const mockAvailableUsers = [
  {
    id: "1",
    name: "Alice Johnson",
    status: "Student",
    subject: "Mathematics",
    subtopic: "Calculus and derivatives",
    schedule: "Mon, Wed 2:00 PM",
    learningMode: "Online",
    matchingType: "1-on-1",
    whatsapp: "+6281234567890",
  },
  {
    id: "2",
    name: "Dr. Smith",
    status: "Tutor",
    subject: "Mathematics",
    subtopic: "Advanced calculus and mathematical analysis",
    schedule: "Mon, Wed 3:00 PM",
    learningMode: "Online, Offline near ITS",
    matchingType: "1-on-1",
    whatsapp: "+6281234567891",
  },
  {
    id: "3",
    name: "Bob Wilson",
    status: "Student",
    subject: "Physics",
    subtopic: "Quantum mechanics basics",
    schedule: "Tue, Thu 10:00 AM",
    learningMode: "Online",
    matchingType: "1-on-1",
    whatsapp: "+6281234567892",
  },
  {
    id: "4",
    name: "Prof. Davis",
    status: "Tutor",
    subject: "Programming",
    subtopic: "Python for Data Science",
    schedule: "Fri 2:00 PM",
    learningMode: "Online, Chat",
    matchingType: "1-on-1",
    whatsapp: "+6281234567893",
  },
]

export async function GET() {
  try {
    // In real implementation, fetch from Google Sheets "Output" or "Available" tab
    // const SPREADSHEET_ID = process.env.GOOGLE_SPREADSHEET_ID
    // const SHEET_NAME = "Output"
    // const API_KEY = process.env.GOOGLE_SHEETS_API_KEY

    // const response = await fetch(
    //   `https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${SHEET_NAME}?key=${API_KEY}`
    // )

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    return NextResponse.json({ users: mockAvailableUsers })
  } catch (error) {
    console.error("Error fetching available users:", error)
    return NextResponse.json({ error: "Failed to fetch available users" }, { status: 500 })
  }
}
