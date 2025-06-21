import TutasCircleView from "@/components/tutas-circle-view"

export default function TutasCirclePage() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4 text-white">Tutas Circle</h1>
        <p className="text-gray-300 text-lg">Active study groups with up to 5 students and 1 tutor</p>
      </div>
      <TutasCircleView />
    </div>
  )
}
