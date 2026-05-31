import { Link } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-5 py-4 md:px-8 md:py-5 lg:px-16">
      <div className="flex items-center gap-2">
        <Link size={24} className="text-accent" />
        <span className="font-bold text-[22px] text-fg-primary font-sans">Shortly</span>
      </div>

      <div className="hidden md:flex items-center gap-6 lg:gap-8">
        <a href="#features" className="text-sm text-fg-secondary hover:text-fg-primary transition-colors">
          Features
        </a>
        <a href="#" className="text-sm text-fg-secondary hover:text-fg-primary transition-colors">
          Pricing
        </a>
        <a href="#" className="text-sm text-fg-secondary hover:text-fg-primary transition-colors">
          API
        </a>
        <button className="bg-accent text-fg-inverse text-sm font-semibold px-6 py-2.5 rounded-full hover:opacity-90 transition-opacity">
          Sign Up
        </button>
      </div>

      <button className="md:hidden bg-accent text-fg-inverse text-sm font-semibold px-5 py-2.5 rounded-full hover:opacity-90 transition-opacity">
        Sign Up
      </button>
    </nav>
  )
}
