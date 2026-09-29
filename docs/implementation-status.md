# Implementation status

Updated 29 September 2026.

## Completed locally

- Responsive React and TypeScript demo journey for 390, 768, and 1440-pixel layouts, with a persistent Demo banner, keyboard focus, status labels, reduced-motion handling, print layout, and explicit human decisions.
- FastAPI demo endpoints and ReportLab PDF generation from the persisted synthetic report fixture.
- Strict Pydantic requirement, finding, evidence, decision, score, and ATS contracts.
- Deterministic Job Match, weighted evidence coverage, half-up rounding, interval merging, and ATS assessment rules.
- PDF and DOCX validation limits, stable segments, encrypted or scan rejection behavior, bounded archive expansion, and local direct-identity redaction.
- Configurable Gemini provider adapter using structured Pydantic output and versioned prompt files. Model output never supplies scores or decisions.
- Google free-tier-only configuration locked to `gemini-3.5-flash-lite`; startup rejects paid model overrides.
- Supabase SQL schema, private queue and ledgers, composite workspace references, RLS read policies, private storage, no browser report/task writes, lease claims, heartbeats, and fencing.
- Synthetic domain and API tests for the central scoring, evidence, duration, parsing, decision conflict, idempotency requirement, and PDF paths.

## Live integration blockers

- No Supabase project, user accounts, JWT issuer, or credentials were supplied, so live Auth, RLS, Storage, database functions, and two-workspace isolation have not been executed against a hosted project.
- No customer-approved Gemini account or API key was supplied. The live SDK request, regional data handling, usage reconciliation, and provider retry behavior have not been exercised with real candidate data.
- Browser automation could not be completed because the environment browser provider failed to initialize. The responsive CSS, production build, and local HTTP serving were verified, but the full Playwright journey remains to be run.
- The live API persistence services and worker dispatch loop remain integration seams around the included domain, adapter, and SQL contracts; the credential-free demo is functional, but this is not production-ready.

## Verification run

- `npm run build`: passed with Vite 8.3.1; 1,615 modules transformed.
- `npm audit --audit-level=low`: passed with zero known vulnerabilities after upgrading Vite and Vitest.
- `.venv/bin/pytest -q`: 25 tests passed in 4.59 seconds; two dependency deprecation warnings only.
- Local frontend request: HTTP 200 from `http://127.0.0.1:5173/`.
- Local API readiness: returned `ready`, `demo`, and `synthetic-demo`.
- Local report endpoint: HTTP 200 with `application/pdf`.
- Generated ReportLab sample: rendered and visually inspected; score table, findings, typography, and page margins were clean with no clipping or overlap.

## Deliberate deviations

- The project is not deployed because the brief explicitly says not to deploy without separate authorization.
- Demo state is process-local and synthetic by design. Live mode refuses missing configuration and never substitutes demo output.
- The frontend uses shadcn-style accessible primitives implemented in the application stylesheet rather than importing the shadcn CLI catalog; this avoids adding an unnecessary generator to the empty Vite repository.
