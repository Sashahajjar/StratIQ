'use client'

import Link from 'next/link'

export default function Navigation() {

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
            <Link href="/dashboard" className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-primary tracking-tight">StratIQ</span>
            </Link>

        </div>
      </div>
    </nav>
  )
}

