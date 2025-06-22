"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

const Navigation = () => {
  const pathname = usePathname()

  const navItems = [
    { href: "/", label: "Register" },
    { href: "/available", label: "Students & Tutors Matched" },
    { href: "/tutas-circle", label: "Tutas Circle" },
    { href: "/about", label: "About" },
  ]

  return (
    <nav className="bg-black border-b border-gray-700 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-2xl font-bold text-white hover:text-gray-300 transition-colors duration-200">
            Tutas
          </Link>
          <div className="flex space-x-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ease-in-out
                  transform hover:scale-105 hover:shadow-lg
                  ${
                    pathname === item.href
                      ? "bg-white text-black shadow-md"
                      : "text-gray-300 hover:text-white hover:bg-gray-800 border border-transparent hover:border-gray-600"
                  }
                `}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navigation
