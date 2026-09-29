# Resume Screener POC

Evidence-based resume screening with separate Job Match and ATS Readiness scores, exact-source findings, identity-hidden review, and explicit recruiter decisions. The repository includes a complete synthetic demo plus the live-mode domain, provider, parser, SQL, queue, and security contracts.

## What works without credentials

The React demo provides the complete journey: dashboard, reviewed JD requirements, candidate upload guidance, redaction disclosure, real analysis stages, detailed report, evidence drawer, decision validation, history, settings, and print/PDF-friendly output. The FastAPI demo exposes the saved synthetic report, idempotent analysis response, optimistic decision conflicts, and ReportLab PDF export. Demo mode is visibly labeled and never calls an AI provider.

## Local setup

Prerequisites: Node 20+, npm 10+, Python 3.11+.

```bash
npm install
python3 -m venv .venv
source .venv/bin/activate
pip install -r apps/api/requirements-dev.txt
```

Run the frontend:

```bash
npm run dev
```

Run the API in another terminal:

```bash
source .venv/bin/activate
AI_MODE=demo uvicorn app.main:app --app-dir apps/api --reload --port 8000
```

Open `http://localhost:5173`. API documentation is at `http://localhost:8000/docs`; the OpenAPI JSON is at `/openapi.json`.

Run verification:

```bash
npm run build
source .venv/bin/activate
pytest -q
```

## Live configuration

1. Create an isolated Supabase project and apply `supabase/migrations/202609290001_initial.sql` with the Supabase CLI or SQL migration runner.
2. Provision users through Supabase Auth, then add workspace memberships. There is no public signup.
3. Copy `apps/api/.env.example` to `apps/api/.env` and provide the server-only Supabase and Gemini values. Copy `apps/web/.env.example` for public browser configuration.
4. Set `AI_MODE=live`. Startup fails if required credentials are missing; it never silently falls back to demo.
5. Start API and worker as separate supervised processes from the same backend source:

```bash
uvicorn app.main:app --app-dir apps/api --host 127.0.0.1 --port 8000
python -m app.worker.main
```

The browser must never receive `SUPABASE_SERVICE_KEY` or `GEMINI_API_KEY`. Use HTTPS and a reverse proxy for any pilot deployment. Real candidate documents require customer-approved provider data terms, region, retention, users, and budget.

## Provider configuration

The live adapter is locked to Google's free-tier `gemini-3.5-flash-lite`. Startup refuses another model ID, preventing accidental paid-model selection. Keep both configured token rates at `0` for this free-tier setup. Free-tier availability, quotas, regional access, and Google data-use terms must be confirmed in the project's AI Studio account before a real-data pilot; a free tier should not be assumed suitable for sensitive production resumes. Set `GEMINI_API_KEY` only in `apps/api/.env`, never in browser configuration or source control.

## Safety boundaries

- Job Match is deterministic and independent of ATS Readiness.
- The model cannot author scores or decisions.
- `NOT_EVIDENCED` means the resume does not establish the claim.
- Scans, encrypted PDFs, files over 5 MiB, PDFs over 20 pages, excessive DOCX expansion, and unreliable extraction are rejected.
- Identity-hidden review reduces direct identity exposure but is not guaranteed anonymization.
- Shortlist is a recruiter workflow status, not a hiring decision or offer.

See [scoring.md](docs/scoring.md), [operations.md](docs/operations.md), and [implementation-status.md](docs/implementation-status.md).
