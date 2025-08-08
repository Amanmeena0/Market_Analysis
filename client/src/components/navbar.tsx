
import React from 'react'
import { ModeToggle } from './mode-toggle'
import Link from 'next/link'

function Navbar() {
  return (
    <nav className='px-8 h-20 backdrop-blur-xl border-b-2 w-full flex justify-between items-center fixed top-0 left-0 right-0 z-50'>
        <div className="container mx-auto p-4 ">
          <Link href="/" className='hover:cursor-pointer'>
            <h1 className="text-4xl font-thin ">Market Researcher</h1>
          </Link>
        </div>
        <ModeToggle />
    </nav>
  )
}

export default Navbar