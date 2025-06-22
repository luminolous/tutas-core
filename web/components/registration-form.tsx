"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface FormData {
  fullName: string
  whatsappNumber: string
  status: "Student" | "Tutor" | ""
  courseName: string
  topicSubtopic: string
  preferredDate: string
  preferredTime: string
  flexibleSchedule: "Yes" | "No" | ""
  learningStyle: string
  learningMode: string[]
  matchingType: "1-on-1" | "Tutas Circle" | ""
}

const RegistrationForm = () => {
  const [formData, setFormData] = useState<FormData>({
    fullName: "",
    whatsappNumber: "",
    status: "",
    courseName: "",
    topicSubtopic: "",
    preferredDate: "",
    preferredTime: "",
    flexibleSchedule: "",
    learningStyle: "",
    learningMode: [],
    matchingType: "",
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitMessage, setSubmitMessage] = useState("")

  const learningStyles = [
    "Visual Learning",
    "Auditory Learning",
    "Kinesthetic Learning",
    "Reading/Writing Learning",
    "Interactive Discussion",
    "Problem-Based Learning",
  ]

  const learningModes = ["Online", "Offline near ITS", "Chat"]

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleCheckboxChange = (value: string) => {
    setFormData((prev) => {
      const newArray = prev.learningMode.includes(value)
        ? prev.learningMode.filter((item) => item !== value)
        : [...prev.learningMode, value]
      return { ...prev, learningMode: newArray }
    })
  }

  const handleRadioChange = (name: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      const response = await fetch("http://localhost:5000/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...formData,
          learningMode: formData.learningMode.join(", "),
          timestamp: new Date().toISOString(),
        }),
      })

      if (response.ok) {
        const result = await response.json()
        setSubmitMessage("✅ Registration submitted successfully!")
        // Reset form
        setFormData({
          fullName: "",
          whatsappNumber: "",
          status: "",
          courseName: "",
          topicSubtopic: "",
          preferredDate: "",
          preferredTime: "",
          flexibleSchedule: "",
          learningStyle: "",
          learningMode: [],
          matchingType: "",
        })
      } else {
        setSubmitMessage("❌ Error submitting registration. Please try again.")
      }
    } catch (error) {
      console.error("Error submitting registration:", error)
      setSubmitMessage("❌ Error connecting to server. Please check if the Flask backend is running.")
    }

    setIsSubmitting(false)
    setTimeout(() => setSubmitMessage(""), 5000)
  }

  return (
    <Card className="bg-black border-gray-700">
      <CardHeader>
        <CardTitle className="text-2xl text-white">Registration Form</CardTitle>
        <p className="text-gray-400">Fill out the form below to register as a student or tutor</p>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Full Name */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Full Name *</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleInputChange}
                className="input-field w-full"
                required
              />
            </div>

            {/* WhatsApp Number */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">WhatsApp Number *</label>
              <input
                type="tel"
                name="whatsappNumber"
                value={formData.whatsappNumber}
                onChange={handleInputChange}
                className="input-field w-full"
                placeholder="+62 812 3456 7890"
                required
              />
            </div>

            {/* Status */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Status *</label>
              <select
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="input-field w-full"
                required
              >
                <option value="">Select Status</option>
                <option value="Student">Student</option>
                <option value="Tutor">Tutor</option>
              </select>
            </div>

            {/* Course Name */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Course Name *</label>
              <input
                type="text"
                name="courseName"
                value={formData.courseName}
                onChange={handleInputChange}
                className="input-field w-full"
                placeholder="e.g., Mathematics, Physics, Programming"
                required
              />
            </div>

            {/* Preferred Date */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Preferred Date *</label>
              <input
                type="date"
                name="preferredDate"
                value={formData.preferredDate}
                onChange={handleInputChange}
                className="input-field w-full"
                required
              />
            </div>

            {/* Preferred Time */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Preferred Time *</label>
              <input
                type="time"
                name="preferredTime"
                value={formData.preferredTime}
                onChange={handleInputChange}
                className="input-field w-full"
                required
              />
            </div>

            {/* Learning Style */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Preferred Learning Style *</label>
              <select
                name="learningStyle"
                value={formData.learningStyle}
                onChange={handleInputChange}
                className="input-field w-full"
                required
              >
                <option value="">Select Learning Style</option>
                {learningStyles.map((style) => (
                  <option key={style} value={style}>
                    {style}
                  </option>
                ))}
              </select>
            </div>

            {/* Matching Type */}
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Matching Type *</label>
              <div className="flex space-x-4 mt-2">
                <label className="flex items-center text-white">
                  <input
                    type="radio"
                    name="matchingType"
                    value="1-on-1"
                    checked={formData.matchingType === "1-on-1"}
                    onChange={(e) => handleRadioChange("matchingType", e.target.value)}
                    className="mr-2"
                  />
                  1-on-1
                </label>
                <label className="flex items-center text-white">
                  <input
                    type="radio"
                    name="matchingType"
                    value="Tutas Circle"
                    checked={formData.matchingType === "Tutas Circle"}
                    onChange={(e) => handleRadioChange("matchingType", e.target.value)}
                    className="mr-2"
                  />
                  Tutas Circle
                </label>
              </div>
            </div>
          </div>

          {/* Topic/Subtopic */}
          <div>
            <label className="block text-sm font-medium mb-2 text-white">Topic/Subtopic *</label>
            <textarea
              name="topicSubtopic"
              value={formData.topicSubtopic}
              onChange={handleInputChange}
              className="input-field w-full h-24 resize-none"
              placeholder="Describe the specific topic or subtopic you want to learn/teach"
              required
            />
          </div>

          {/* Flexible Schedule */}
          <div>
            <label className="block text-sm font-medium mb-2 text-white">Flexible Schedule *</label>
            <div className="flex space-x-4">
              <label className="flex items-center text-white">
                <input
                  type="radio"
                  name="flexibleSchedule"
                  value="Yes"
                  checked={formData.flexibleSchedule === "Yes"}
                  onChange={(e) => handleRadioChange("flexibleSchedule", e.target.value)}
                  className="mr-2"
                />
                Yes
              </label>
              <label className="flex items-center text-white">
                <input
                  type="radio"
                  name="flexibleSchedule"
                  value="No"
                  checked={formData.flexibleSchedule === "No"}
                  onChange={(e) => handleRadioChange("flexibleSchedule", e.target.value)}
                  className="mr-2"
                />
                No
              </label>
            </div>
          </div>

          {/* Learning Mode */}
          <div>
            <label className="block text-sm font-medium mb-2 text-white">Learning Mode * (Select all that apply)</label>
            <div className="space-y-2">
              {learningModes.map((mode) => (
                <label key={mode} className="flex items-center text-white">
                  <input
                    type="checkbox"
                    checked={formData.learningMode.includes(mode)}
                    onChange={() => handleCheckboxChange(mode)}
                    className="mr-2"
                  />
                  {mode}
                </label>
              ))}
            </div>
          </div>

          <Button type="submit" disabled={isSubmitting} className="btn-primary w-full">
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-black mr-2"></div>
                Submitting...
              </>
            ) : (
              "Submit Registration"
            )}
          </Button>

          {submitMessage && (
            <div
              className={`text-center p-3 rounded ${
                submitMessage.includes("successfully") ? "bg-green-900 text-green-100" : "bg-red-900 text-red-100"
              }`}
            >
              {submitMessage}
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  )
}

export default RegistrationForm
