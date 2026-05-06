# Verification Report — forseti-jobhunter-browser-automation

- Feature: BrowserAutomationService Phase 1 + Phase 2
- QA owner: qa-forseti
- Date: 2026-04-25
- Decision: BLOCK

## KB references
- `knowledgebase/lessons/20260227-routing-permission-mismatch-companyresearch.md`
- `knowledgebase/lessons/20260220-forseti-jobhunter-uid-vs-jobseeker-id.md`

## Scope verified
- Targeted retest for dev item `20260405-011000-impl-forseti-jobhunter-browser-automation`
- Unit suite path and bootstrap validity
- Credentials route anonymous/authenticated access behavior
- Site audit / role-based URL validation path for this host

## Evidence

### PASS
1. **Unit coverage passes** with Drupal-aware PHPUnit config:
   - Command: `cd /var/www/html/forseti && vendor/bin/phpunit -c web/core/phpunit.xml.dist web/modules/custom/job_hunter/tests/src/Unit/Service/BrowserAutomationServiceTest.php --testdox`
   - Result: `15 tests, 40 assertions, exit 0`
   - Coverage signal: routing/manual-required outcomes, attempt logging, bridge exception handling, missing-table graceful handling.
2. **Credentials route ACL behaves correctly on the live host**:
   - Anonymous: `curl -i -s https://forseti.life/jobhunter/settings/credentials` → `403 Forbidden`
   - Authenticated: `curl -i -s -H "Cookie: <qa_tester_authenticated session>" https://forseti.life/jobhunter/settings/credentials` → `200 OK`
3. **Anonymous restriction remains in place** for related protected surface:
   - `curl -i -s https://forseti.life/talk-with-forseti` → `403 Forbidden`

### BLOCKERS
1. **Canonical unit suite command in the manifest was stale** before this QA pass:
   - Plain `vendor/bin/phpunit ...BrowserAutomationServiceTest.php` failed with `Class "Drupal\Tests\UnitTestCase" not found`.
   - Root cause: wrong file path and missing Drupal PHPUnit config.
2. **Canonical functional suite is not runnable**:
   - Command: `cd /var/www/html/forseti && vendor/bin/phpunit web/modules/custom/job_hunter/tests/src/Functional/CredentialsControllerTest.php --testdox`
   - Result: `6 failures`
   - Root cause: `CredentialsControllerTest.php` resolves `job_hunter.routing.yml` via a broken relative path in the deployed tree.
3. **Alternate BrowserTestBase functional test is also blocked by environment gaps**:
   - Command: `cd /var/www/html/forseti && SIMPLETEST_BASE_URL=http://localhost vendor/bin/phpunit -c web/core/phpunit.xml.dist web/modules/custom/job_hunter/tests/src/Functional/Controller/CredentialControllerTest.php --filter testCredentialsPageAllowsAuthenticatedUser --testdox`
   - Result: after setting `SIMPLETEST_BASE_URL`, test still errors with `Class "Behat\Mink\Driver\BrowserKitDriver" not found`.
4. **Automated site audit defaults are invalid on this host**:
   - `http://localhost` returns `400 The provided host name is not valid for this server.`
   - Production-gated audit with `ALLOW_PROD_QA=1 FORSETI_BASE_URL=https://forseti.life` runs, but its authenticated-session probe still marks the session invalid even though direct cookie-based curl to the credentials route returns `200`.

## Conclusion
Feature behavior is **partially verified**: the shipped unit coverage passes and the credentials route currently enforces the expected anonymous/authenticated access behavior on `https://forseti.life`. This item remains **BLOCKED** because the canonical automated verification path for the feature is not clean: the functional suite is broken, the BrowserTestBase alternative is missing required test dependencies, and the site-audit automation is still misaligned with this host's valid base URL/session flow.

## Recommended fixes
- Dev/owner of product tests:
  - Fix `web/modules/custom/job_hunter/tests/src/Functional/CredentialsControllerTest.php` relative path resolution.
  - Add the missing BrowserKit/Mink dependency or otherwise document the supported functional-test harness for `CredentialControllerTest.php`.
- QA/manifest owner:
  - Keep the unit suite command aligned with `-c web/core/phpunit.xml.dist` and the real `tests/src/Unit/Service/` path.
- CEO/site/runbook owner:
  - Update site/runbook guidance that still defaults Forseti pre-release QA to `http://localhost` on this host; valid host is `https://forseti.life`.
