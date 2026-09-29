# Operations runbook

## Health and startup

Use `/health/live` for process liveness and `/health/ready` for configured-mode readiness. In live mode, do not start if Supabase or Gemini configuration is incomplete. Run the API and worker independently so API restarts do not erase queued work.

## Queue recovery

Tasks use 120-second leases, 20-second heartbeats, random fencing tokens, and `FOR UPDATE SKIP LOCKED`. An expired lease may be reclaimed. Every stage write and completion must match the current token; a stale worker cannot publish a report. Stop new claims before deployment, allow current leases to finish or expire, apply backward-compatible migrations, restart, and verify readiness.

## Provider failures and spend

Reserve the maximum configured attempt cost atomically before dispatch. Permit no more than two concurrent provider tasks and three total attempts, including a repair. Retry transient rate, network, or 5xx errors with bounded backoff. Keep timeout or crash reservations as unknown until reconciliation; do not record them as free. PDF exports make no provider call.

## Deletion and retention

Owner deletion tombstones immediately, cancels queued tasks, and enqueues cleanup. Every API and worker write rechecks the tombstone. Cleanup removes private objects and derived candidate content and leaves only an opaque deletion event. Retry storage deletion failures. Reapply the deletion ledger after any restore. Default retention is 30 days; allowed values are 7–90.

## Incident checks

Inspect queue depth, oldest task age, safe error codes, provider attempt counts, unknown reservations, evidence validation failures, and warm latency. Logs may contain request and opaque resource IDs, never resume text, prompts, contact details, object paths, provider bodies, or secrets.
