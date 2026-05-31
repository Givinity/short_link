import { BarChart3, Shield, Globe } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

interface Feature {
  icon: LucideIcon
  title: string
  description: string
}

const features: Feature[] = [
  {
    icon: BarChart3,
    title: 'Link Analytics',
    description: 'Track clicks, geographic data, referrers, and devices in real-time.',
  },
  {
    icon: Shield,
    title: 'Custom Aliases',
    description: 'Create branded short links with custom aliases that reflect your brand.',
  },
  {
    icon: Globe,
    title: 'QR Codes',
    description: 'Generate QR codes for any short link instantly. Perfect for print and offline.',
  },
]

export default function Features() {
  return (
    <section id="features" className="flex flex-col items-center gap-8 px-5 py-10 md:px-8 md:py-12 lg:gap-12 lg:px-16 lg:py-16">
      <div className="flex flex-col items-center gap-3">
        <h2 className="text-2xl font-bold text-fg-primary text-center m-0 md:text-[28px] lg:text-[36px]">
          Everything You Need
        </h2>
        <p className="text-base text-fg-secondary text-center">
          Powerful features to help you manage and track your links
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full">
        {features.map(({ icon: Icon, title, description }) => (
          <div
            key={title}
            className="flex flex-col gap-5 bg-surface-secondary rounded-design-2xl p-8"
          >
            <div className="w-12 h-12 rounded-design-xl bg-[#A855F722] flex items-center justify-center">
              <Icon size={24} className="text-accent" />
            </div>
            <h3 className="text-xl font-semibold text-fg-primary m-0">{title}</h3>
            <p className="text-sm text-fg-secondary leading-relaxed m-0">{description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
