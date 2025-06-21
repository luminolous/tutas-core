import RegistrationForm from "@/components/registration-form"

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4 text-white">Welcome to Tutas</h1>
        <p className="text-gray-300 text-lg">
          Register as a student or tutor to get matched for personalized learning sessions
        </p>
      </div>
      <RegistrationForm />
    </div>
  )
}
