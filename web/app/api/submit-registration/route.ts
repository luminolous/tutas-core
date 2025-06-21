import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.json()

    // Google Sheets configuration
    const SPREADSHEET_ID = process.env.GOOGLE_SPREADSHEET_ID || "your-spreadsheet-id"
    const SHEET_NAME = "Input"
    const API_KEY = process.env.GOOGLE_SHEETS_API_KEY || "your-api-key"

    // Prepare data for Google Sheets
    const rowData = [
      formData.timestamp,
      formData.fullName,
      formData.whatsappNumber,
      formData.status,
      formData.courseName,
      formData.topicSubtopic,
      formData.preferredDate,
      formData.preferredTime,
      formData.flexibleSchedule,
      formData.learningStyle,
      formData.learningMode,
      formData.matchingType,
      "", // Status Proses - left empty by default
    ]

    // In a real implementation, you would use Google Sheets API
    // For now, we'll simulate the API call
    console.log("Submitting to Google Sheets:", {
      spreadsheetId: SPREADSHEET_ID,
      range: `${SHEET_NAME}!A:M`,
      values: [rowData],
    })

    // Simulate Google Sheets API call
    // const response = await fetch(
    //   `https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${SHEET_NAME}!A:M:append?valueInputOption=RAW&key=${API_KEY}`,
    //   {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({
    //       values: [rowData]
    //     })
    //   }
    // )

    // Simulate successful response
    await new Promise((resolve) => setTimeout(resolve, 1000))

    return NextResponse.json({
      success: true,
      message: "Registration submitted successfully to Google Sheets",
    })
  } catch (error) {
    console.error("Error submitting to Google Sheets:", error)
    return NextResponse.json({ success: false, message: "Error submitting registration" }, { status: 500 })
  }
}
