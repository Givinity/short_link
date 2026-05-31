const stats = [
  { value: '2.5M+', label: 'Links Created' },
  { value: '150M+', label: 'Clicks Tracked' },
  { value: '99.9%', label: 'Uptime' },
  { value: '50ms', label: 'Redirect Speed' },
]

export default function Stats() {
  return (
    <section className="grid grid-cols-2 gap-8 px-5 py-8 md:flex md:items-center md:justify-around md:gap-0 md:px-8 md:py-10 lg:px-16 lg:py-12">
      {stats.map((stat, i) => (
        <>
          <div key={stat.label} className="flex flex-col items-center gap-1">
            <span className="font-mono font-bold text-[28px] md:text-[32px] lg:text-[40px] text-fg-primary leading-none">
              {stat.value}
            </span>
            <span className="text-sm text-fg-muted">{stat.label}</span>
          </div>
          {i < stats.length - 1 && (
            <div key={`div-${i}`} className="hidden md:block w-px h-12 bg-divider" />
          )}
        </>
      ))}
    </section>
  )
}
