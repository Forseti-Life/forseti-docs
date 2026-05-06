# Verification Report — forseti-jobhunter-e2e-flow

- Feature: JobHunter End-to-End Workflow
- QA owner: qa-forseti
- Date: 2026-04-25
- Decision: BLOCK

## KB references
- `knowledgebase/lessons/20260220-forseti-jobhunter-uid-vs-jobseeker-id.md`
- `knowledgebase/lessons/20260227-jobhunter-e2e-csrf-token-empty-save-job.md`

## Scope verified
- Targeted retest for dev item `20260405-011000-impl-forseti-jobhunter-e2e-flow`
- Current suite wiring in `qa-suites/products/forseti/suite.json`
- Live route/ACL behavior for key JobHunter pages
- Automated site audit / role-based permission checks for the current valid host

## Evidence

### PASS
1. **Protected JobHunter routes respond correctly on the valid host**:
   - Anonymous: `https://forseti.life/jobhunter` → `403`
   - Authenticated (`qa_tester_authenticated` via ULI cookie): `/jobhunter` → `200`, `/jobhunter/my-jobs` → `200`, `/jobhunter/profile/edit` → `200`
2. **Automated role-based audit is clean for anon on the valid host**:
   - Artifact: `sessions/qa-forseti/artifacts/auto-site-audit/20260425-173231/findings-summary.md`
   - Result: `0` permission expectation violations, `0` other failures
3. **Environment host constraint confirmed**:
   - `web/sites/default/settings.php` enforces `$base_url = 'https://forseti.life'`
   - `trusted_host_patterns` allow only `forseti.life` / `www.forseti.life`

### BLOCKERS
1. **Canonical Playwright runner is missing from the active repo layout**:
   - Expected by AC / suite wiring / implementation notes: `/home/ubuntu/forseti.life/testing/jobhunter-workflow-step1-6-data-engineer.mjs`
   - Actual: file not present anywhere under `/home/ubuntu/forseti.life` or `/var/www/html/forseti`
2. **Previous suite wiring was stale for this host**:
   - It still referenced `http://localhost` and `jhtr:qa-users-ensure`
   - On this machine, `http://localhost` returns `400 The provided host name is not valid for this server.`
   - `vendor/bin/drush list` shows no `jhtr:` namespace
3. **Without the Playwright script, core AC cannot be re-verified**:
   - Step 1–6 workflow completion
   - `submission.success: true`
   - Save/apply/track path
   - Stage-break assertion (no external account creation)

## Additional observations
- A direct authenticated curl to the search page for the historical query did not expose any `btn-save-job` elements or non-empty `data-csrf-token` attributes in the raw HTML response during this pass, so Step 2 could not be independently smoke-tested via curl alone.
- This is secondary evidence only; the primary blocker is the missing canonical E2E runner.

## Conclusion
This item remains **BLOCKED**. The live JobHunter routes and anon ACL look healthy on `https://forseti.life`, but the release-critical E2E workflow cannot be re-verified because the referenced Playwright script is missing from the active repository layout and the suite metadata had drifted to an invalid host/setup path.

## Recommended fixes
- Dev/owner of the E2E workflow:
  - Restore or relocate `testing/jobhunter-workflow-step1-6-data-engineer.mjs` into the active repo layout, or replace it with the new canonical runner path.
- QA/manifest owner:
  - Keep the suite host/ULI wiring aligned with `https://forseti.life` and the existing `qa_tester_authenticated` user.
- PM:
  - Keep this feature blocked for Gate 2 until the canonical E2E runner exists and produces fresh artifacts.
