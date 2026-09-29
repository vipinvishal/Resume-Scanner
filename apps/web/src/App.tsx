import { useEffect, useState } from 'react'
import { BriefcaseBusiness, CheckCircle2, ChevronRight, CircleHelp, Download, FileCheck2, LayoutDashboard, LockKeyhole, Plus, Search, Settings, ShieldCheck, Upload, X, XCircle } from 'lucide-react'
import { StatusBadge } from './components/StatusBadge'
import { Landing } from './pages/Landing'
import type { Status } from './lib/demo'

type Page = 'landing' | 'dashboard' | 'job' | 'upload' | 'progress' | 'report' | 'settings'
type Finding = { requirement_id:string; requirement:string; category:string; status:Status; reason:string; quote?:string|null; source?:string|null }
type CategoryContribution = { category:string; base_weight:number; criterion_count:number; credit:string; contribution:string }
type AtsCheckItem = { name:string; weight:number; result:'pass'|'fail'|'unassessed'; observed:string }
type LiveReport = { job_match:number|null; evidence_coverage:number|null; ats_readiness:number|null; coverage_notice:boolean; findings:Finding[]; questions:string[]; redaction_warnings:string[]; category_contributions:CategoryContribution[]; ats_checks:AtsCheckItem[] }
const API_BASE=import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'
const STAGE_MESSAGES=['Reading your document locally and removing direct identifiers…','Sending redacted job and resume text to the configured AI model…','Validating quotes, coverage, and scores…']

export default function App(){
 const [page,setPage]=useState<Page>('landing'); const [jdText,setJdText]=useState(''); const [resume,setResume]=useState<File|null>(null); const [report,setReport]=useState<LiveReport|null>(null); const [stage,setStage]=useState(''); const [error,setError]=useState(''); const [drawer,setDrawer]=useState<Finding|null>(null); const [decision,setDecision]=useState(''); const [saved,setSaved]=useState(false)
 const title=({landing:'',dashboard:'Overview',job:'New job',upload:'Add candidate',progress:'Analysis progress',report:'Candidate report',settings:'Workspace settings'} as Record<Page,string>)[page]
 const goto=(next:Page)=>{setPage(next);window.scrollTo({top:0,behavior:'smooth'})}
 const chooseDecision=(value:string)=>{setDecision(value);setSaved(false)}
 const analyze=async()=>{
  if(!resume||jdText.trim().length<50)return
  setError(''); setSaved(false); setDecision(''); goto('progress'); setStage(STAGE_MESSAGES[0])
  const timers=[setTimeout(()=>setStage(STAGE_MESSAGES[1]),900),setTimeout(()=>setStage(STAGE_MESSAGES[2]),2600)]
  const form=new FormData(); form.append('resume',resume); form.append('jd_text',jdText)
  try{
   const response=await fetch(`${API_BASE}/live-analysis`,{method:'POST',body:form})
   const payload=await response.json()
   if(!response.ok)throw new Error(typeof payload.detail==='string'?payload.detail:'Analysis could not be completed.')
   setReport(payload.report); goto('report')
  }catch(cause){
   setError(cause instanceof Error?cause.message:'Analysis could not be completed.'); goto('upload')
  }finally{
   timers.forEach(clearTimeout)
  }
 }
 if(page==='landing')return <Landing onEnter={()=>goto('dashboard')}/>
 return <div className="app-shell"><aside className="sidebar" aria-label="Primary navigation"><div className="brand"><span className="brand-mark"><FileCheck2 size={20}/></span><span>Northstar</span></div><div className="workspace"><div className="avatar">AS</div><div><strong>Acme Systems</strong><span>Local review workspace</span></div></div><nav><button className={page==='dashboard'?'active':''} onClick={()=>goto('dashboard')}><LayoutDashboard size={19}/>Dashboard</button><button onClick={()=>goto('settings')}><Settings size={19}/>Workspace settings</button></nav><div className="privacy-note"><ShieldCheck size={18}/><div><strong>Transient local review</strong><span>Files are not stored. Redacted text is sent to the AI model only when you analyze.</span></div></div></aside><main><div className="live-banner"><ShieldCheck size={15}/> Live analysis · Redacted resume text only · Human decisions remain yours</div><header><button className="mobile-brand" onClick={()=>goto('dashboard')}><FileCheck2 size={20}/> Northstar</button><div><span className="eyebrow">Resume review</span><h1>{title}</h1></div><div className="header-actions"><button className="icon-btn" aria-label="Help"><CircleHelp size={20}/></button><button className="primary" onClick={()=>goto('job')}><Plus size={18}/> New job</button></div></header>{page==='dashboard'&&<Dashboard goto={goto} report={report}/>} {page==='job'&&<JobSetup goto={goto} jdText={jdText} setJdText={setJdText}/>} {page==='upload'&&<UploadPage goto={goto} file={resume} setFile={setResume} error={error} clearError={()=>setError('')} onAnalyze={analyze}/>} {page==='progress'&&<Progress stage={stage}/>} {page==='report'&&<Report report={report} goto={goto} decision={decision} setDecision={chooseDecision} saved={saved} onSave={()=>setSaved(true)} setDrawer={setDrawer}/>} {page==='settings'&&<SettingsPage/>}</main>{drawer&&<EvidenceDrawer finding={drawer} close={()=>setDrawer(null)}/>}</div>
}

function Dashboard({goto,report}:{goto:(page:Page)=>void;report:LiveReport|null}){return <div className="page dashboard"><section className="intro"><div><h2>Start an evidence-based review</h2><p>Paste the actual job description, select one resume, then inspect only validated evidence.</p></div><button className="primary" onClick={()=>goto('job')}><Plus size={18}/> New analysis</button></section>{report?<section className="activity-card"><div className="section-head"><div><h2>Latest live report</h2><p>Generated from your last submitted JD and resume.</p></div></div><button className="candidate-row" onClick={()=>goto('report')}><div className="candidate-code"><div className="avatar square">LR</div><div><strong>LOCAL-REVIEW</strong><span>Open the in-browser result</span></div></div><div className="row-score"><span><b>{report.job_match??'—'}</b> Job Match</span><span><b>{report.evidence_coverage??'—'}{report.evidence_coverage===null?'':'%'}</b> evidence</span></div><ChevronRight size={18}/></button></section>:<section className="empty-card"><BriefcaseBusiness size={30}/><h2>No report yet</h2><p>Your first live report appears after you submit a job description and resume.</p><button className="primary" onClick={()=>goto('job')}>Set up a job <ChevronRight size={17}/></button></section>}</div>}

function JobSetup({goto,jdText,setJdText}:{goto:(page:Page)=>void;jdText:string;setJdText:(value:string)=>void}){const valid=jdText.trim().length>=50;return <div className="page narrow"><section className="card"><span className="eyebrow">Live job input</span><h2>Paste the actual job description</h2><p>The AI model extracts only explicit, job-related requirements from this text — nothing is carried over from any other job.</p><div className="field"><label htmlFor="jd">Job description</label><textarea id="jd" value={jdText} onChange={event=>setJdText(event.target.value)} placeholder="Paste the complete job description here…" aria-describedby="jd-help"/><small id="jd-help">{jdText.trim().length}/60,000 characters · at least 50 are required</small></div><div className="notice"><LockKeyhole size={19}/><div><strong>Job text is treated as untrusted data</strong><p>Embedded instructions and links are ignored. Only explicit job-related requirements are extracted.</p></div></div><div className="form-actions"><button className="secondary" onClick={()=>goto('dashboard')}>Cancel</button><button className="primary" disabled={!valid} onClick={()=>goto('upload')}>Continue to resume <ChevronRight size={17}/></button></div></section></div>}

function UploadPage({goto,file,setFile,error,clearError,onAnalyze}:{goto:(page:Page)=>void;file:File|null;setFile:(file:File|null)=>void;error:string;clearError:()=>void;onAnalyze:()=>void}){const select=(selected:File|undefined)=>{clearError();if(!selected)return;if(!/\.(pdf|docx)$/i.test(selected.name)){setFile(null);return}if(selected.size>5_242_880){setFile(null);return}setFile(selected)};const size=file?(file.size<1_048_576?`${Math.max(1,Math.round(file.size/1024))} KB`:`${(file.size/1024/1024).toFixed(2)} MB`):'';return <div className="page narrow"><section className="card"><span className="eyebrow">Live resume input</span><h2>Add one candidate resume</h2><p>The file is read in memory. Direct identifiers are redacted before the model request.</p><label className={`dropzone ${file?'has-file':''}`}><input type="file" accept=".pdf,.docx" onChange={event=>select(event.target.files?.[0])}/>{file?<><FileCheck2 size={34}/><strong>{file.name}</strong><span>{size} · selected and ready to analyze</span><span className="replace-file">Choose another file</span></>:<><Upload size={34}/><strong>Drop a resume here or choose a file</strong><span>PDF or DOCX · maximum 5 MiB · up to 20 PDF pages</span></>}</label><div aria-live="polite">{file&&<div className="upload-success"><FileCheck2 size={19}/><div><strong>Resume selected successfully</strong><p>Select Analyze resume to start the real review.</p></div></div>}{error&&<p className="upload-error" role="alert">{error}</p>}</div><div className="notice"><ShieldCheck size={19}/><div><strong>Before you analyze</strong><p>Redacted job and resume text will be sent to your configured AI provider. No automatic hiring decision is made.</p></div></div><div className="form-actions"><button className="secondary" onClick={()=>goto('job')}>Back</button><button className="primary" disabled={!file} onClick={onAnalyze}>Analyze resume <ChevronRight size={17}/></button></div></section></div>}

function Progress({stage}:{stage:string}){
 const activeIndex=Math.max(STAGE_MESSAGES.indexOf(stage),0)
 const fill=((activeIndex+1)/STAGE_MESSAGES.length)*100
 return <div className="page narrow"><section className="card progress-card"><div className="processing-icon spin"><FileCheck2/></div><span className="eyebrow">Live analysis</span><h2>Preparing your evidence report</h2><p>{stage || 'Starting analysis…'}</p><div className="progress-track"><i style={{width:`${fill}%`}}/></div><ol className="stages"><li className={activeIndex===0?'active':activeIndex>0?'done':''}><span>{activeIndex>0?<CheckCircle2 size={15}/>:1}</span><div><strong>Read and redact</strong><small>Local parsing, with direct identifiers removed</small></div></li><li className={activeIndex===1?'active':activeIndex>1?'done':''}><span>{activeIndex>1?<CheckCircle2 size={15}/>:2}</span><div><strong>Extract and compare</strong><small>The AI model returns requirement-level findings</small></div></li><li className={activeIndex===2?'active':''}><span>3</span><div><strong>Validate and score</strong><small>Quotes, IDs, coverage, and Job Match are checked server-side</small></div></li></ol></section></div>
}

const RING_RADIUS=42; const RING_CIRCUMFERENCE=2*Math.PI*RING_RADIUS

function useRevealed(dep:unknown){
 const [revealed,setRevealed]=useState(false)
 useEffect(()=>{setRevealed(false);const id=requestAnimationFrame(()=>setRevealed(true));return()=>cancelAnimationFrame(id)},[dep])
 return revealed
}

function useCountUp(target:number|null,duration=1000){
 const [value,setValue]=useState(0)
 useEffect(()=>{
  if(target===null){setValue(0);return}
  let raf=0; let start:number|null=null
  const tick=(ts:number)=>{
   if(start===null)start=ts
   const t=Math.min((ts-start)/duration,1); const eased=1-Math.pow(1-t,3)
   setValue(Math.round(target*eased))
   if(t<1)raf=requestAnimationFrame(tick)
  }
  raf=requestAnimationFrame(tick)
  return()=>cancelAnimationFrame(raf)
 },[target,duration])
 return value
}

function RingScore({label,value,suffix,note,color}:{label:string;value:number|null;suffix:string;note:string;color:string}){
 const revealed=useRevealed(value)
 const displayed=useCountUp(value)
 const fraction=value===null?0:Math.min(Math.max(value,0),100)/100
 const offset=RING_CIRCUMFERENCE*(1-(revealed?fraction:0))
 return <article className="score-card ring">
  <span>{label}</span>
  <div className="ring-wrap">
   <svg viewBox="0 0 100 100" className="ring-svg" aria-hidden="true">
    <circle cx="50" cy="50" r={RING_RADIUS} className="ring-track"/>
    {value!==null&&<circle cx="50" cy="50" r={RING_RADIUS} className="ring-fill" style={{stroke:color,strokeDasharray:RING_CIRCUMFERENCE,strokeDashoffset:offset}}/>}
   </svg>
   <div className="ring-value"><strong>{value===null?'—':displayed}</strong>{value!==null&&<b>{suffix}</b>}</div>
  </div>
  <p>{value===null?'Insufficient format assessment':note}</p>
 </article>
}

function ContributionChart({contributions}:{contributions:CategoryContribution[]}){
 const revealed=useRevealed(contributions)
 if(!contributions.length)return null
 return <section className="card contribution"><h3>Score breakdown by category</h3><p>How each requirement category contributed to the Job Match score.</p>{contributions.map(c=>{const pct=c.base_weight?Math.round((Number(c.contribution)/c.base_weight)*100):0;return <div className="bar-row" key={c.category}><span>{c.category.replaceAll('_',' ')}</span><div><i style={{width:revealed?`${pct}%`:'0%'}}/></div><b>{c.contribution}/{c.base_weight} pts</b></div>})}</section>
}

function AtsChecklist({checks}:{checks:AtsCheckItem[]}){
 if(!checks.length)return null
 return <section className="card"><h3>Document formatting checks</h3><p>ATS Readiness comes only from these format checks, never from resume content.</p><ul className="ats-list">{checks.map((c,index)=><li key={c.name} className={`ats-item ats-${c.result}`} style={{animationDelay:`${index*70}ms`}}><span className="ats-icon">{c.result==='pass'?<CheckCircle2 size={16}/>:c.result==='fail'?<XCircle size={16}/>:<CircleHelp size={16}/>}</span><div><strong>{c.name.replaceAll('_',' ')}</strong><p>{c.observed}</p></div></li>)}</ul></section>
}

function Report({report,goto,decision,setDecision,saved,onSave,setDrawer}:{report:LiveReport|null;goto:(page:Page)=>void;decision:string;setDecision:(value:string)=>void;saved:boolean;onSave:()=>void;setDrawer:(finding:Finding)=>void}){
 if(!report)return <div className="page narrow"><section className="empty-card"><Search size={30}/><h2>No live report available</h2><p>Start with an actual job description and a resume. Static demo scores are no longer shown here.</p><button className="primary" onClick={()=>goto('job')}>Start analysis</button></section></div>
 const groups=Object.entries(report.findings.reduce((all,finding)=>{(all[finding.category]??=[]).push(finding);return all},{} as Record<string,Finding[]>))
 let findingIndex=0
 return <div className="page report-page"><div className="report-main">
  <div className="report-heading"><div><button className="back-link" onClick={()=>goto('dashboard')}>← Back to dashboard</button><span className="eyebrow">LOCAL-REVIEW · Live analysis</span><h2>Evidence-based review</h2><p>Job Match is calculated only from validated requirement findings. ATS Readiness is separate.</p></div><button className="secondary" onClick={()=>window.print()}><Download size={17}/> Print report</button></div>
  <section className="score-grid">
   <RingScore label="Job Match" value={report.job_match} suffix="/100" note="Deterministic match to this job" color="#4f46e5"/>
   <RingScore label="Evidence coverage" value={report.evidence_coverage} suffix="%" note="Weighted criteria with evidence" color="#10b981"/>
   <RingScore label="ATS Readiness" value={report.ats_readiness} suffix="/100" note="Document formatting only" color="#f59e0b"/>
  </section>
  {report.coverage_notice&&<div className="coverage-warning"><CircleHelp size={19}/><p><strong>Clarification needed.</strong> Evidence coverage is below 60%. This does not mean the candidate lacks capability.</p></div>}
  <div className="separation-note"><ShieldCheck size={19}/><p><strong>Scores are separate.</strong> ATS Readiness never changes Job Match, and neither score makes a hiring decision.</p></div>
  <ContributionChart contributions={report.category_contributions}/>
  <AtsChecklist checks={report.ats_checks}/>
  <section className="findings-section"><div className="section-head"><div><h2>Requirement findings</h2><p>Every confirmed requirement appears once. Open a finding to inspect its source quote.</p></div></div>
   {groups.map(([category,findings])=><div className="finding-group" key={category}><h3>{category.replaceAll('_',' ')}<span>{findings.length}</span></h3>{findings.map(finding=>{const delay=findingIndex++*55;return <button className="finding" style={{animationDelay:`${delay}ms`}} key={finding.requirement_id} onClick={()=>setDrawer(finding)}><StatusBadge status={finding.status}/><div><strong>{finding.requirement}</strong><p>{finding.reason}</p>{finding.quote&&<q>{finding.quote}</q>}</div><ChevronRight size={18}/></button>})}</div>)}
  </section>
  {report.questions.length>0&&<section className="card questions"><h3>Suggested clarification questions</h3><ol>{report.questions.map(question=><li key={question}>{question}</li>)}</ol></section>}
 </div>
 <aside className="decision-panel"><span className="decision-state">Human action required</span><h3>Record a human decision</h3><p>This records only your internal next step. It does not contact the candidate.</p><fieldset><legend>Decision</legend>{['Shortlist','Talk to candidate','Reject'].map(label=><label className="radio" key={label}><input type="radio" checked={decision===label} onChange={()=>setDecision(label)}/><span>{label}</span></label>)}</fieldset><button className="primary wide" disabled={!decision} onClick={onSave}>Save local decision</button>{saved&&<div className="save-confirm"><CheckCircle2 size={16}/> Saved locally as “{decision}”.</div>}</aside>
 </div>
}

function EvidenceDrawer({finding,close}:{finding:Finding;close:()=>void}){return <div className="drawer-wrap" role="dialog" aria-modal="true" aria-label="Evidence source"><button className="drawer-scrim" onClick={close} aria-label="Close evidence"/><aside className="drawer"><div className="drawer-head"><div><span className="eyebrow">Evidence source</span><h2>{finding.requirement}</h2></div><button className="icon-btn" onClick={close}><X/></button></div><StatusBadge status={finding.status}/><p>{finding.reason}</p>{finding.quote?<div className="source-preview"><span>{finding.source}</span><p>{finding.quote}</p><small>Quote validated against redacted source text</small></div>:<div className="empty-evidence"><Search/><strong>No resume evidence cited</strong><p>Not-evidenced findings never invent a quote.</p></div>}<div className="drawer-foot"><ShieldCheck/><p>A quote confirms document provenance, not the truth of the claim.</p></div></aside></div>}
function SettingsPage(){return <div className="page narrow"><section className="card"><h2>Local live-analysis settings</h2><p>This local review tool does not persist uploaded files. It uses your configured AI provider key only when you select Analyze resume.</p><div className="notice"><LockKeyhole size={19}/><div><strong>Identity-hidden review</strong><p>Direct identifiers are redacted before provider calls. Work history can still indirectly identify someone.</p></div></div></section></div>}
