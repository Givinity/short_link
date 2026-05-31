import { Link } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="flex flex-col items-center gap-4 px-5 py-6 bg-surface-secondary md:flex-row md:justify-between md:px-8 md:py-8 lg:px-16">
      <div className="flex items-center gap-2">
        <Link size={18} className="text-accent" />
        <span className="text-base font-semibold text-fg-primary">Shortly</span>
      </div>

      <span className="text-[13px] text-fg-muted">
        © 2026 Shortly. All rights reserved.
      </span>

      <div className="flex items-center gap-6">
        <a href="#" className="text-[13px] text-fg-secondary hover:text-fg-primary transition-colors">Privacy</a>
        <a href="#" className="text-[13px] text-fg-secondary hover:text-fg-primary transition-colors">Terms</a>
        <a href="#" className="text-[13px] text-fg-secondary hover:text-fg-primary transition-colors">Contact</a>
      </div>
    </footer>
  )
}
