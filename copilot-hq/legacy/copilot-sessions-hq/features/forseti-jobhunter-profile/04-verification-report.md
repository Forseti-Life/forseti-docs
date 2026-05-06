# Verification Report — forseti-jobhunter-profile

- Feature: JobHunter Profile Page
- QA owner: qa-forseti
- Date: 2026-04-25
- Decision: BLOCK

## KB references
- `knowledgebase/lessons/20260220-forseti-jobhunter-uid-vs-jobseeker-id.md`
- `sessions/pm-forseti/artifacts/20260220-job-hunter-profile-review/pm-review.md`

## Scope verified
- Targeted retest for dev item `20260405-011000-impl-forseti-jobhunter-profile`
- Current suite wiring in `qa-suites/products/forseti/suite.json`
- Live route/ACL behavior for key profile pages
- Live profile form markers for core and newer ATS-assist fields
- Role-based permission checks for the valid host

## Evidence

### PASS
1. **Core profile routes behave correctly on the valid host**:
   - Anonymous: `https://forseti.life/jobhunter/profile` → `403`
   - Authenticated (`qa_tester_authenticated` via ULI cookie):
     - `/jobhunter/profile` → `302` (redirect behavior matches AC)
     - `/jobhunter/profile/edit` → `200`
     - `/jobhunter/profile/dashboard` → `200`
     - `/jobhunter/profile/summary` → `200`
   - Administrator:
     - `/jobhunter/profile/edit` → `200`
2. **Profile edit form renders expected fields** in live HTML:
   - `field_target_job_titles`
   - resume file input
   - `field_age_18_or_older`
   - `field_hear_about_us`
   - `field_prior_company_email`
   - `field_country`
3. **Ownership guard exists in code** for resume delete:
   - `UserProfileController.php` checks `loadByUserId($current_user_id)` and denies when `job_seeker_profile->id != $resume->job_seeker_id` unless the user has admin permission.
4. **Automated role-based audit is clean for anon on the valid host**:
   - Artifact: `sessions/qa-forseti/artifacts/auto-site-audit/20260425-180025/findings-summary.md`
   - Result: `0` permission expectation violations, `0` other failures

### BLOCKERS
1. **Canonical profile Playwright runner is missing from the active repo layout**:
   - Expected by suite wiring / test plan: `/home/ubuntu/forseti.life/testing/jobhunter-profile.mjs`
   - Actual: file not present anywhere under `/home/ubuntu/forseti.life` or `/var/www/html/forseti`
2. **Previous suite wiring was stale for this host**:
   - It still referenced `http://localhost` and `jhtr:qa-users-ensure`
   - On this machine, `localhost` is rejected by trusted-host settings
   - `vendor/bin/drush list` shows no `jhtr:` namespace
3. **Core data-persistence assertions remain unverified**:
   - Direct DB check for QA user (`uid=1600`) shows `jobhunter_job_seeker.consolidated_profile_json` is currently `NULL`
   - Without a runnable profile E2E/form-submit harness, QA could not verify:
     - resume upload persistence
     - consolidated JSON save/update
     - profile completeness update after save
     - download/delete behavior with owned fixture data
     - corrupt JSON / queue failure handling

## Conclusion
This item remains **BLOCKED**. The live profile surface and ACL behavior are healthy, the edit form renders expected fields, and admin access behaves as expected. However, the release-critical verification path for profile save/upload/persistence cannot be completed because the canonical `jobhunter-profile.mjs` runner is missing from the active repo layout and the suite metadata had drifted to invalid host/setup assumptions.

## Recommended fixes
- Dev/owner of the profile E2E workflow:
  - Restore or relocate `testing/jobhunter-profile.mjs` into the active repo layout, or provide the new canonical runner path.
- QA/manifest owner:
  - Keep the suite host/login wiring aligned with `https://forseti.life` and the existing `qa_tester_authenticated` user.
- PM:
  - Keep this feature blocked for Gate 2 until a runnable profile E2E/form-submit path exists and produces fresh persistence evidence.
