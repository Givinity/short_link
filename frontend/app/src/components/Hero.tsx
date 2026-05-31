import { useState } from 'react'
import { LinkIcon, Zap, Check, Copy, CheckCheck } from 'lucide-react'
import { getUrlValidationError } from '../lib/validateUrl'

interface ShortenResult {
  shortLink: string
  originalUrl: string
}

export default function Hero() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ShortenResult | null>(null)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  async function handleShorten() {
    const trimmed = url.trim()
    const validationError = getUrlValidationError(url)
    if (validationError) {
      setError(validationError)
      setResult(null)
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const params = new URLSearchParams({ url: trimmed })
      const res = await fetch(`/api/v1/shorten?${params}`, { method: 'POST' })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        const detail = data?.detail
        const message =
          typeof detail === 'string'
            ? detail
            : Array.isArray(detail) && detail[0]?.msg
              ? detail[0].msg
              : `Error ${res.status}`
        throw new Error(message)
      }
      const data = await res.json()
      setResult({ shortLink: data.task_short_link, originalUrl: trimmed })
      setError('')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  async function handleCopy() {
    if (!result) return
    await navigator.clipboard.writeText(`${window.location.origin}/${result.shortLink}`)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const shortUrl = result
    ? `${window.location.origin}/${result.shortLink}`
    : 'example.com/x8kQ2p'

  const originalUrl = result
    ? result.originalUrl
    : 'https://example.com/very/long/url/that/needs/shortening'

  return (
    <section className="flex flex-col items-center gap-8 px-5 py-10 md:px-8 md:py-12 lg:px-16 lg:py-20 lg:gap-10">
      {/* Hero content */}
      <div className="flex flex-col items-center gap-5 w-full lg:gap-6 lg:max-w-[800px]">
        {/* Eyebrow badge */}
        <div className="flex items-center gap-2 bg-surface-secondary rounded-full px-4 py-1.5">
          <div className="w-2 h-2 rounded-full bg-green-dot" />
          <span className="text-[13px] text-fg-secondary">Free & Fast URL Shortener</span>
        </div>

        {/* Headline */}
        <h1 className="text-[36px] font-extrabold leading-[1.1] text-center text-fg-primary m-0 md:text-[48px] lg:text-[64px]">
          Make Every Link
          <br />
          Short & Powerful
        </h1>

        {/* Subtitle */}
        <p className="text-base text-fg-secondary text-center leading-relaxed md:text-lg lg:max-w-[600px]">
          Transform long, ugly URLs into clean, trackable short links.
          {' '}Analyze clicks, manage campaigns, and boost your brand.
        </p>
      </div>

      {/* URL input row */}
      <div className="flex flex-col gap-2 w-full md:flex-row md:gap-3 lg:max-w-[720px]">
        <div
          className={`flex items-center gap-3 flex-1 bg-surface-secondary border rounded-design-xl px-5 py-4 ${error ? 'border-red-400/60' : 'border-divider'}`}
        >
          <LinkIcon size={20} className="text-fg-muted shrink-0" />
          <input
            type="url"
            value={url}
            aria-invalid={error ? true : undefined}
            onChange={e => {
              setUrl(e.target.value)
              if (error) setError('')
            }}
            onKeyDown={e => e.key === 'Enter' && handleShorten()}
            placeholder="Paste your long URL here..."
            className="flex-1 bg-transparent text-base text-fg-primary placeholder:text-fg-muted outline-none min-w-0"
          />
        </div>
        <button
          onClick={handleShorten}
          disabled={loading || !url.trim()}
          className="flex items-center justify-center gap-2 bg-accent text-fg-inverse font-semibold text-base px-8 py-4 rounded-design-xl hover:opacity-90 transition-opacity disabled:opacity-50 shrink-0"
        >
          <Zap size={18} />
          {loading ? 'Shortening…' : 'Shorten'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <p className="text-sm text-red-400 -mt-4">{error}</p>
      )}

      {/* Result / Placeholder card */}
      <div
        className={`flex items-center justify-between w-full gap-4 bg-surface-secondary border border-[#22C55E33] rounded-design-xl px-5 py-4 lg:max-w-[720px] flex-col md:flex-row ${!result ? 'opacity-40 pointer-events-none select-none' : ''}`}
      >
        <div className="flex items-center gap-3 min-w-0 w-full md:w-auto">
          <div className="w-7 h-7 rounded-full bg-[#22C55E22] flex items-center justify-center shrink-0">
            <Check size={14} className="text-green-dot" />
          </div>
          <div className="flex flex-col gap-1 min-w-0">
            <span className="font-mono font-semibold text-base text-accent truncate">
              {shortUrl}
            </span>
            <span className="text-xs text-fg-muted truncate">
              {originalUrl}
            </span>
          </div>
        </div>
        <button
          onClick={result ? handleCopy : undefined}
          className="flex items-center gap-1.5 bg-divider text-fg-secondary text-[13px] font-medium px-4 py-2 rounded-design-lg hover:bg-[#3f3f46] transition-colors shrink-0 self-end md:self-auto"
        >
          {copied ? <CheckCheck size={14} className="text-green-dot" /> : <Copy size={14} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
    </section>
  )
}
