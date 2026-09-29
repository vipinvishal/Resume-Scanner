# Scoring contract

## Job Match

`job_match_v1` uses base weights: required skills 35, relevant experience 25, responsibilities 20, preferred skills 15, and education or certifications 5. Categories with no confirmed criteria are removed and the remaining weights are normalized. Criteria within a category are equal.

Credits are `MET = 1`, `PARTIAL = 0.5`, and `NOT_EVIDENCED` or `CONTRADICTED = 0`. Partial is valid only for a duration criterion or an objective rubric confirmed before analysis. The backend rounds only the final result with decimal half-up rounding.

The LLD example contributes 26.25 + 12.50 + 20 + 7.50 across an active weight of 95. `100 × 66.25 / 95 = 69.7368`, displayed as **70**.

## Evidence coverage

Coverage uses the same category weights. Every finding except `NOT_EVIDENCED` counts as covered; it describes evidence availability, not confidence. Missing evidence remains in the denominator. Coverage below 60% requires a clarification notice and must not label the candidate unqualified.

## Duration

Month-granularity dates become half-open month intervals. Overlaps are merged before counting. `Present` resolves to the persisted analysis evaluation date. Year-only or ambiguous dates do not establish months and instead create verification questions. Total career tenure never substitutes for skill-specific duration.

## ATS Readiness

`ats_readiness_v1` measures text availability (35), character integrity (20), reading-order proxies (20), section structure (15), and date readability (10). Assessed checks are normalized only when assessed weight is at least 80; otherwise the result is null. Failed text availability or character integrity blocks Job Match as unreliable extraction. ATS Readiness never changes Job Match.
