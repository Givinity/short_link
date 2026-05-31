import { ArrowRight } from 'lucide-react'

export default function CTA() {
  return (
    <section className="flex flex-col items-center px-5 py-10 md:px-8 md:py-12 lg:px-16 lg:py-20">
      <div
        className="flex flex-col items-center gap-6 w-full rounded-design-2xl px-6 py-10 md:px-10 md:py-12 lg:px-20 lg:py-16"
        style={{ background: 'linear-gradient(135deg, #A855F7 0%, #6D28D9 100%)' }}
      >
        <h2 className="text-2xl font-bold text-white text-center m-0 leading-tight md:text-[28px] lg:text-[36px]">
          Ready to Shorten Your Links?
        </h2>
        <p className="text-base text-[#FFFFFFCC] text-center max-w-lg">
          Join millions of users who trust Shortly for fast, reliable link shortening.
        </p>
        <button className="flex items-center gap-2 bg-white text-fg-inverse font-semibold text-base px-8 py-4 rounded-full hover:opacity-90 transition-opacity lg:px-10">
          Get Started — It's Free
          <ArrowRight size={18} />
        </button>
      </div>
    </section>
  )
}
