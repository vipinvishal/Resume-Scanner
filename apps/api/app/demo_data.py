from datetime import datetime, timezone
from uuid import UUID

DEMO_WORKSPACE_ID="00000000-0000-4000-8000-000000000001"
DEMO_ANALYSIS_ID="00000000-0000-4000-8000-000000000104"
DEMO_FINDINGS=[
 {"requirement_id":"req-aws","requirement":"Hands-on AWS experience","category":"required_skill","status":"MET","reason":"Production infrastructure ownership is directly evidenced.","quote":"Designed and operated multi-account AWS environments using Terraform.","source":"resume-p2"},
 {"requirement_id":"req-iac","requirement":"Infrastructure as code","category":"required_skill","status":"MET","reason":"Terraform usage is explicit and applied.","quote":"Reduced provisioning time by 60% through reusable Terraform modules.","source":"resume-p3"},
 {"requirement_id":"req-exp","requirement":"4+ years in cloud engineering","category":"experience","status":"PARTIAL","reason":"Grounded intervals establish 38 months; earlier duration is unclear.","quote":"Cloud Engineer · Mar 2023 – Present","source":"resume-p1"},
 {"requirement_id":"req-k8s","requirement":"Own production Kubernetes workloads","category":"responsibility","status":"NOT_EVIDENCED","reason":"The resume does not establish Kubernetes production ownership.","quote":None,"source":None},
]
DEMO_REPORT={"schema_version":"report_v1","analysis_id":DEMO_ANALYSIS_ID,"candidate_code":"CAN-1048","job_title":"Senior Cloud Engineer","job_version":2,"job_match":70,"evidence_coverage":83,"ats_readiness":90,"coverage_notice":False,"findings":DEMO_FINDINGS,"questions":["Which production Kubernetes workloads did you personally own?"],"versions":{"parser":"parser_v1","prompt":"resume_eval_v1","model":"demo-fixture-v1","redaction":"redact_v1","schema":"report_v1","scoring":"job_match_v1","ats":"ats_readiness_v1"},"evaluation_as_of":"2026-09-29"}
