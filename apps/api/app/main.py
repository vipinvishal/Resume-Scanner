from contextlib import asynccontextmanager
from fastapi import FastAPI, File, Form, Header, HTTPException, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .demo_data import DEMO_ANALYSIS_ID, DEMO_REPORT
from .domain.models import DecisionInput
from .adapters.pdf_report import build_report
from .services.live_analysis import analyze_live

settings=get_settings(); decisions=[]
@asynccontextmanager
async def lifespan(app:FastAPI):
    get_settings()
    yield
app=FastAPI(title="Resume Screener API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.allowed_origins.split(",")],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

def require_demo():
    if settings.ai_mode!="demo": raise HTTPException(501,"Live persistence must be configured through Supabase")
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready","mode":settings.ai_mode,"provider":settings.model_id if settings.ai_mode=="live" else "synthetic-demo"}
@app.get("/api/v1/me")
def me():
    require_demo(); return {"user":{"id":"demo-owner","name":"Aisha Verma"},"workspaces":[{"id":"demo-workspace","name":"Acme Systems","role":"owner","identity_hidden":True,"retention_days":30}],"demo":True}
@app.get("/api/v1/dashboard")
def dashboard():
    require_demo(); return {"counts":{"total":24,"pending":6,"shortlisted":8,"talk_first":5,"rejected":5},"jobs":[{"id":"job-cloud","title":"Senior Cloud Engineer","version":2,"candidates":8}]}
@app.get("/api/v1/analyses/{analysis_id}")
def analysis(analysis_id:str):
    require_demo()
    if analysis_id!=DEMO_ANALYSIS_ID: raise HTTPException(404,"Analysis not found")
    return {"analysis_id":analysis_id,"status":"ready","stage":"Ready","report":DEMO_REPORT}
@app.post("/api/v1/candidates/{candidate_id}/analyses",status_code=202)
def create_analysis(candidate_id:str,idempotency_key:str|None=Header(default=None,alias="Idempotency-Key")):
    require_demo()
    if not idempotency_key: raise HTTPException(400,"Idempotency-Key is required")
    return {"analysis_id":DEMO_ANALYSIS_ID,"status":"ready","task_id":"demo-task","deduplicated":True}
@app.post("/api/v1/candidates/{candidate_id}/decisions",status_code=201)
def save_decision(candidate_id:str,payload:DecisionInput):
    require_demo(); current=len(decisions)
    if payload.expected_version!=current: raise HTTPException(409,detail={"code":"DECISION_CONFLICT","current_version":current})
    record=payload.model_dump()|{"candidate_id":candidate_id,"decision_version":current+1,"actor":"demo-owner"}; decisions.append(record); return record
@app.get("/api/v1/candidates/{candidate_id}/decisions")
def decision_history(candidate_id:str): require_demo(); return {"items":[d for d in decisions if d["candidate_id"]==candidate_id],"next_cursor":None}
@app.get("/api/v1/analyses/{analysis_id}/report.pdf")
def report_pdf(analysis_id:str):
    require_demo()
    if analysis_id!=DEMO_ANALYSIS_ID: raise HTTPException(404,"Analysis not found")
    return Response(build_report(DEMO_REPORT),media_type="application/pdf",headers={"Content-Disposition":"attachment; filename=CAN-1048-evidence-report.pdf","Cache-Control":"no-store"})

@app.post("/api/v1/live-analysis")
async def live_analysis(resume:UploadFile=File(...),jd_text:str=Form(...),candidate_name:str|None=Form(default=None)):
    """Transient local analysis. Source files are parsed in memory and are not persisted."""
    return await analyze_live(resume,jd_text,candidate_name,settings)
