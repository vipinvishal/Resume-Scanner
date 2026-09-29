import { useEffect, useRef, useState } from 'react'
import { motion, useReducedMotion, useScroll, useTransform } from 'motion/react'
import { ArrowRight, CheckCircle2, FileCheck2, Quote, Scale, ShieldCheck, UserCheck } from 'lucide-react'
import { StatusBadge } from '../components/StatusBadge'

const EASE = [0.16, 1, 0.3, 1] as const
const SPRING = { type: 'spring', stiffness: 400, damping: 28 } as const

function useReveal() {
  const reduce = useReducedMotion()
  return (delay = 0) => ({
    initial: reduce ? false : { opacity: 0, y: 22 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true, amount: 0.35 },
    transition: { duration: 0.6, delay, ease: EASE },
  })
}

function useTap() {
  const reduce = useReducedMotion()
  return reduce ? {} : { whileHover: { scale: 1.03, y: -1 }, whileTap: { scale: 0.97 }, transition: SPRING }
}

export function Landing({ onEnter }: { onEnter: () => void }) {
  return (
    <div className="landing">
      <LandingNav onEnter={onEnter} />
      <Hero onEnter={onEnter} />
      <PrinciplesStrip />
      <HowItWorks />
      <EvidenceShowcase />
      <ScoresDuo />
      <FinalCta onEnter={onEnter} />
      <LandingFooter onEnter={onEnter} />
    </div>
  )
}

function LandingNav({ onEnter }: { onEnter: () => void }) {
  const tap = useTap()
  return (
    <header className="land-nav">
      <div className="land-container land-nav-row">
        <div className="land-brand"><span className="brand-mark"><FileCheck2 size={18} /></span><span>Northstar</span></div>
        <nav className="land-links">
          <a href="#how-it-works">How it works</a>
          <a href="#evidence">Evidence</a>
          <a href="#scoring">Scoring</a>
        </nav>
        <motion.button className="primary" onClick={onEnter} {...tap}>Start a review<ArrowRight size={16} /></motion.button>
      </div>
    </header>
  )
}

function Hero({ onEnter }: { onEnter: () => void }) {
  const reduce = useReducedMotion()
  const tap = useTap()
  const sectionRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: sectionRef, offset: ['start start', 'end start'] })
  const frameY = useTransform(scrollYProgress, [0, 1], [0, reduce ? 0 : -50])
  const frameRotate = useTransform(scrollYProgress, [0, 1], [0, reduce ? 0 : 2.5])
  return (
    <section className="land-hero" ref={sectionRef}>
      <div className="land-hero-glow" aria-hidden="true" />
      <div className="land-container land-hero-grid">
        <motion.div
          className="land-hero-copy"
          initial={reduce ? false : { opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: EASE }}
        >
          <h1>Job Match scores, backed by exact quotes.</h1>
          <p>Paste a job description, upload one resume, and get a deterministic match score where every finding cites its exact source.</p>
          <div className="land-hero-actions">
            <motion.button className="primary" onClick={onEnter} {...tap}>Start a review<ArrowRight size={16} /></motion.button>
            <motion.a className="secondary" href="#how-it-works" {...tap}>See how it works</motion.a>
          </div>
        </motion.div>
        <motion.div
          className="hero-frame"
          style={{ y: frameY, rotate: frameRotate }}
          initial={reduce ? false : { opacity: 0, y: 26, scale: 0.97 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.15, ease: EASE }}
        >
          <div className="hero-frame-shine" aria-hidden="true" />
          <div className="hero-frame-bar"><span /><span /><span /></div>
          <div className="hero-frame-body">
            <div className="hero-frame-rings">
              <MiniRing value={82} color="#4f46e5" label="Job Match" />
              <MiniRing value={94} color="#f59e0b" label="ATS Readiness" delay={0.15} />
            </div>
            <div className="hero-frame-finding">
              <StatusBadge status="MET" />
              <div>
                <strong>Hands-on AWS experience</strong>
                <p><q>Designed and operated multi-account AWS environments using Terraform.</q></p>
                <span>Resume, Experience, paragraph 2</span>
              </div>
            </div>
            <div className="hero-frame-finding is-muted">
              <StatusBadge status="NOT_EVIDENCED" />
              <div>
                <strong>Own production Kubernetes workloads</strong>
                <p>The resume does not establish Kubernetes production ownership.</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

function useCountUp(target: number, active: boolean, duration = 1100) {
  const [value, setValue] = useState(0)
  const reduce = useReducedMotion()
  useEffect(() => {
    if (!active) return
    if (reduce) { setValue(target); return }
    let raf = 0
    let start: number | null = null
    const tick = (ts: number) => {
      if (start === null) start = ts
      const t = Math.min((ts - start) / duration, 1)
      const eased = 1 - Math.pow(1 - t, 3)
      setValue(Math.round(target * eased))
      if (t < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [active, target, duration, reduce])
  return value
}

function MiniRing({ value, color, label, size = 76, delay = 0 }: { value: number; color: string; label: string; size?: number; delay?: number }) {
  const reduce = useReducedMotion()
  const [inView, setInView] = useState(false)
  const big = size >= 132
  const radius = big ? 52 : 30
  const viewBox = big ? 132 : 76
  const circumference = 2 * Math.PI * radius
  const displayed = useCountUp(value, inView)
  return (
    <div className={`mini-ring-block${big ? ' big' : ''}`}>
      <div className="mini-ring" style={{ width: size, height: size }}>
        <svg viewBox={`0 0 ${viewBox} ${viewBox}`} aria-hidden="true">
          <circle cx={viewBox / 2} cy={viewBox / 2} r={radius} className="mini-ring-track" />
          <motion.circle
            cx={viewBox / 2}
            cy={viewBox / 2}
            r={radius}
            className="mini-ring-fill"
            style={{ stroke: color, strokeDasharray: circumference }}
            initial={{ strokeDashoffset: circumference }}
            whileInView={{ strokeDashoffset: circumference * (1 - value / 100) }}
            viewport={{ once: true, amount: 0.6 }}
            onViewportEnter={() => setInView(true)}
            transition={reduce ? { duration: 0 } : { duration: 1.1, ease: EASE, delay: 0.2 + delay }}
          />
        </svg>
        <div className="mini-ring-value"><strong>{displayed}</strong></div>
      </div>
      <span className="mini-ring-label">{label}</span>
    </div>
  )
}

function PrinciplesStrip() {
  const reveal = useReveal()
  const items = [
    { icon: Scale, label: 'Deterministic scoring' },
    { icon: Quote, label: 'Exact-quote evidence' },
    { icon: ShieldCheck, label: 'Identity-hidden review' },
    { icon: UserCheck, label: 'Human makes the call' },
  ]
  return (
    <section className="land-principles">
      <div className="land-container principles-row">
        {items.map((item, index) => (
          <motion.div className="principle" key={item.label} {...reveal(index * 0.06)}>
            <item.icon size={18} />
            <span>{item.label}</span>
          </motion.div>
        ))}
      </div>
    </section>
  )
}

function HowItWorks() {
  const reveal = useReveal()
  const steps = [
    { title: 'Paste the job description', body: 'The model extracts only explicit, job-related requirements, nothing implied.' },
    { title: 'Upload one resume', body: 'Direct identifiers are redacted locally before anything reaches the model.' },
    { title: 'Read the evidence', body: 'Every finding links back to the line in the resume that supports it.' },
  ]
  return (
    <section className="land-section" id="how-it-works">
      <div className="land-container">
        <h2>How a review runs</h2>
        <div className="timeline">
          <div className="timeline-track">
            {steps.map((step, index) => (
              <div className="timeline-track-item" key={step.title}>
                <motion.span className="timeline-index" {...reveal(index * 0.12)}>{index + 1}</motion.span>
                {index < steps.length - 1 && <span className="timeline-connector" />}
              </div>
            ))}
          </div>
          <div className="timeline-labels">
            {steps.map((step, index) => (
              <motion.div className="timeline-label" key={step.title} {...reveal(index * 0.12 + 0.08)}>
                <strong>{step.title}</strong>
                <p>{step.body}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

function EvidenceShowcase() {
  const reveal = useReveal()
  return (
    <section className="land-section land-section-narrow" id="evidence">
      <div className="land-container">
        <h2>Not evidenced means exactly that.</h2>
        <p className="land-lede">When a resume does not establish a claim, the report says so directly instead of guessing or penalizing silently.</p>
        <div className="evidence-card">
          <motion.div className="evidence-row" {...reveal(0)}>
            <span className="evidence-label">Requirement</span>
            <strong>4+ years in cloud engineering</strong>
          </motion.div>
          <motion.div className="evidence-row" {...reveal(0.12)}>
            <span className="evidence-label">Finding</span>
            <StatusBadge status="PARTIAL" />
          </motion.div>
          <motion.div className="evidence-quote" {...reveal(0.24)}>
            <Quote size={16} />
            <p><q>Cloud Engineer, Mar 2023 to Present</q></p>
            <span>Resume, Experience, paragraph 1</span>
          </motion.div>
          <motion.p className="evidence-reason" {...reveal(0.36)}>
            Grounded month-level intervals establish 38 months. Earlier duration is unclear, so the finding stays partial instead of guessing.
          </motion.p>
        </div>
      </div>
    </section>
  )
}

function ScoresDuo() {
  const reveal = useReveal()
  return (
    <section className="land-section land-section-center" id="scoring">
      <div className="land-container">
        <h2>Two scores, never blended.</h2>
        <p className="land-lede">ATS Readiness checks formatting only. Job Match checks the job only. Neither one changes the other, and neither makes the hiring decision.</p>
        <div className="duo-grid">
          <motion.div className="duo-card" {...reveal(0)}>
            <MiniRing value={82} color="#4f46e5" label="Job Match" size={132} />
            <p>Deterministic match to this job's requirements only.</p>
          </motion.div>
          <motion.div className="duo-card" {...reveal(0.12)}>
            <MiniRing value={94} color="#f59e0b" label="ATS Readiness" size={132} />
            <p>Document formatting only. It never touches Job Match.</p>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

function FinalCta({ onEnter }: { onEnter: () => void }) {
  const reveal = useReveal()
  const tap = useTap()
  return (
    <section className="land-cta-banner">
      <div className="land-cta-glow" aria-hidden="true" />
      <motion.div className="land-container land-cta-inner" {...reveal(0)}>
        <CheckCircle2 size={26} />
        <h2>Run an evidence-based review now.</h2>
        <p>It works against your own AI provider key, locally. No account, and nothing is stored after the review closes.</p>
        <motion.button className="primary" onClick={onEnter} {...tap}>Start a review<ArrowRight size={16} /></motion.button>
      </motion.div>
    </section>
  )
}

function LandingFooter({ onEnter }: { onEnter: () => void }) {
  const tap = useTap()
  return (
    <footer className="land-footer">
      <div className="land-container land-footer-row">
        <div className="land-brand"><span className="brand-mark"><FileCheck2 size={18} /></span><span>Northstar</span></div>
        <p>A local, evidence-based resume review tool.</p>
        <motion.button className="secondary" onClick={onEnter} {...tap}>Start a review</motion.button>
      </div>
      <div className="land-container">
        <small>This build runs entirely on your machine, using the AI provider you configure. It does not run as a hosted service.</small>
      </div>
    </footer>
  )
}
