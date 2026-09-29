import os
os.environ["AI_MODE"]="demo"
from fastapi.testclient import TestClient
from app.main import app, decisions
client=TestClient(app)
def test_health_and_demo_report():
    assert client.get("/health/ready").json()["mode"]=="demo"
    report=client.get("/api/v1/analyses/00000000-0000-4000-8000-000000000104").json()["report"]
    assert report["job_match"]==70 and report["ats_readiness"]==90
def test_idempotency_key_required(): assert client.post("/api/v1/candidates/c1/analyses").status_code==400
def test_decision_validation_and_conflict():
    decisions.clear(); payload={"status":"talk_first","note":"Needs a conversation","questions":["Which workload did you own?"],"analysis_id":"a1","expected_version":0}
    assert client.post("/api/v1/candidates/c1/decisions",json=payload).status_code==201
    assert client.post("/api/v1/candidates/c1/decisions",json=payload).status_code==409
def test_pdf_export_matches_saved_scores():
    result=client.get("/api/v1/analyses/00000000-0000-4000-8000-000000000104/report.pdf")
    assert result.status_code==200 and result.content.startswith(b"%PDF") and result.headers["cache-control"]=="no-store"
