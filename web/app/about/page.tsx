import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function AboutPage() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-6 text-white">About Tutas</h1>
        <p className="text-gray-300 text-xl max-w-3xl mx-auto leading-relaxed">
          Connecting students and tutors for personalized learning experiences through innovative matching technology
        </p>
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {/* What is Tutas */}
        <Card className="bg-black border-gray-700 hover:border-gray-600 transition-all duration-300">
          <CardHeader>
            <CardTitle className="text-xl text-white flex items-center">
              <span className="text-2xl mr-3">🎓</span>
              What is Tutas?
            </CardTitle>
          </CardHeader>
          <CardContent className="text-gray-300 space-y-4">
            <p className="text-white">
              Tutas is a modern tutoring platform that bridges the gap between students seeking knowledge and qualified
              tutors ready to share their expertise.
            </p>
            <p className="text-white">
              Our platform facilitates both one-on-one tutoring sessions and collaborative group learning through our
              innovative "Tutas Circle" feature.
            </p>
            <p className="text-white">
              We believe that quality education should be accessible, personalized, and tailored to each learner's
              unique needs and schedule.
            </p>
          </CardContent>
        </Card>

        {/* How It Works */}
        <Card className="bg-black border-gray-700 hover:border-gray-600 transition-all duration-300">
          <CardHeader>
            <CardTitle className="text-xl text-white flex items-center">
              <span className="text-2xl mr-3">⚙️</span>
              How It Works
            </CardTitle>
          </CardHeader>
          <CardContent className="text-gray-300 space-y-4">
            <div className="space-y-3">
              <div className="flex items-start">
                <span className="bg-white text-black rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">
                  1
                </span>
                <p className="text-white">Register with your learning preferences and schedule</p>
              </div>
              <div className="flex items-start">
                <span className="bg-white text-black rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">
                  2
                </span>
                <p className="text-white">Our algorithm matches you with compatible partners</p>
              </div>
              <div className="flex items-start">
                <span className="bg-white text-black rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">
                  3
                </span>
                <p className="text-white">Connect via WhatsApp to coordinate sessions</p>
              </div>
              <div className="flex items-start">
                <span className="bg-white text-black rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">
                  4
                </span>
                <p className="text-white">Start your personalized learning journey!</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Matching Algorithm */}
        <Card className="bg-black border-gray-700 hover:border-gray-600 transition-all duration-300">
          <CardHeader>
            <CardTitle className="text-xl text-white flex items-center">
              <span className="text-2xl mr-3">🧠</span>
              Smart Matching
            </CardTitle>
          </CardHeader>
          <CardContent className="text-gray-300 space-y-3">
            <p className="text-white mb-3">Our intelligent algorithm considers:</p>
            <ul className="space-y-2">
              <li className="flex items-center text-white">
                <span className="text-green-400 mr-2">✓</span>
                Subject expertise and learning needs
              </li>
              <li className="flex items-center text-white">
                <span className="text-green-400 mr-2">✓</span>
                Preferred study times and flexibility
              </li>
              <li className="flex items-center text-white">
                <span className="text-green-400 mr-2">✓</span>
                Learning modes (online, offline, chat)
              </li>
              <li className="flex items-center text-white">
                <span className="text-green-400 mr-2">✓</span>
                Learning styles and teaching preferences
              </li>
              <li className="flex items-center text-white">
                <span className="text-green-400 mr-2">✓</span>
                Matching type preference (1-on-1 or group)
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Learning Options */}
      <div className="grid gap-8 md:grid-cols-2">
        <Card className="bg-black border-gray-700 hover:border-gray-600 transition-all duration-300">
          <CardHeader>
            <CardTitle className="text-xl text-white flex items-center">
              <span className="text-2xl mr-3">👤</span>
              One-on-One Tutoring
            </CardTitle>
          </CardHeader>
          <CardContent className="text-gray-300 space-y-4">
            <p className="text-white">Personalized sessions between one student and one tutor, perfect for:</p>
            <ul className="space-y-2">
              <li className="flex items-center text-white">
                <span className="text-blue-400 mr-2">•</span>
                Focused learning and addressing specific weaknesses
              </li>
              <li className="flex items-center text-white">
                <span className="text-blue-400 mr-2">•</span>
                Customized pace and learning approach
              </li>
              <li className="flex items-center text-white">
                <span className="text-blue-400 mr-2">•</span>
                Intensive exam preparation
              </li>
              <li className="flex items-center text-white">
                <span className="text-blue-400 mr-2">•</span>
                Building confidence in challenging subjects
              </li>
            </ul>
          </CardContent>
        </Card>

        <Card className="bg-black border-gray-700 hover:border-gray-600 transition-all duration-300">
          <CardHeader>
            <CardTitle className="text-xl text-white flex items-center">
              <span className="text-2xl mr-3">👥</span>
              Tutas Circle
            </CardTitle>
          </CardHeader>
          <CardContent className="text-gray-300 space-y-4">
            <p className="text-white">Small group sessions with up to 5 students and 1 tutor, ideal for:</p>
            <ul className="space-y-2">
              <li className="flex items-center text-white">
                <span className="text-purple-400 mr-2">•</span>
                Collaborative learning and peer interaction
              </li>
              <li className="flex items-center text-white">
                <span className="text-purple-400 mr-2">•</span>
                Cost-effective quality education
              </li>
              <li className="flex items-center text-white">
                <span className="text-purple-400 mr-2">•</span>
                Group discussions and problem-solving
              </li>
              <li className="flex items-center text-white">
                <span className="text-purple-400 mr-2">•</span>
                Building study communities
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Who Can Join */}
      <Card className="bg-black border-gray-700 hover:border-gray-600 transition-all duration-300">
        <CardHeader>
          <CardTitle className="text-2xl text-white text-center flex items-center justify-center">
            <span className="text-3xl mr-3">🌟</span>
            Who Can Join Tutas?
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="text-center">
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-semibold text-white mb-3">Students</h3>
              <ul className="text-gray-300 space-y-2">
                <li className="text-white">School and university students</li>
                <li className="text-white">Adult learners acquiring new skills</li>
                <li className="text-white">Professionals seeking career development</li>
                <li className="text-white">Anyone passionate about learning</li>
              </ul>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold text-white mb-3">Tutors</h3>
              <ul className="text-gray-300 space-y-2">
                <li className="text-white">Qualified educators and teachers</li>
                <li className="text-white">Subject matter experts</li>
                <li className="text-white">Graduate students with expertise</li>
                <li className="text-white">Professionals with teaching experience</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Contact Information */}
      <Card className="bg-black border-gray-700 hover:border-gray-600 transition-all duration-300">
        <CardHeader>
          <CardTitle className="text-2xl text-white text-center flex items-center justify-center">
            <span className="text-3xl mr-3">📞</span>
            Get in Touch
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-3 text-center">
            <div>
              <div className="text-3xl mb-3">📧</div>
              <h4 className="font-semibold text-white mb-2">Email Support</h4>
              <p className="text-gray-300">tutasits@gmail.com</p>
            </div>
            <div>
              <div className="text-3xl mb-3">📱</div>
              <h4 className="font-semibold text-white mb-2">WhatsApp</h4>
              <p className="text-gray-300">+62 819 3762 2696</p>
              <a
                href="https://wa.me/6281937622696"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-2 whatsapp-btn"
              >
                Chat with us
              </a>
            </div>
            <div>
              <div className="text-3xl mb-3">🕒</div>
              <h4 className="font-semibold text-white mb-2">Support Hours</h4>
              <p className="text-gray-300">24/7 Everyday</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Call to Action */}
      <div className="text-center py-12">
        <h2 className="text-3xl font-bold text-white mb-6">Ready to Start Learning?</h2>
        <p className="text-gray-300 text-lg mb-8 max-w-2xl mx-auto">
          Join thousands of students and tutors who have already discovered the power of personalized learning with
          Tutas.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/">
            <Button className="btn-primary text-lg px-8 py-3">Register Now</Button>
          </Link>
          <Link href="/available">
            <Button className="btn-secondary text-lg px-8 py-3">Browse Tutors and Students Matched</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
