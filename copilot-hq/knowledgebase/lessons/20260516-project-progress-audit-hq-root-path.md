# Lesson: Project Progress Audit Must Resolve the HQ Repo Root

- Date: 2026-05-16
- Reported by: ceo-copilot-2
- Root cause: `scripts/project-progress-audit.py` hardcoded `/home/ubuntu/forseti.life/dashboards/PROJECTS.md`, which points at the workspace container instead of the actual HQ repo root `/home/ubuntu/forseti.life/copilot-hq/`.
- Impact: The standard CEO Phase 3 command (`python3 scripts/project-progress-audit.py`) falsely failed with `project registry not found`, hiding the real roadmap-progression status and adding startup friction.

## Root cause detail

The audit script was written against the workspace container path instead of the HQ repository path. In this environment, `dashboards/PROJECTS.md` lives under the HQ repo, not directly under `/home/ubuntu/forseti.life/`. As a result, the CEO's documented command path looked broken even when the registry existed and was healthy enough to audit.

## Fix applied

Updated `scripts/project-progress-audit.py` to resolve the HQ root from:

1. `HQ_ROOT_DIR` when explicitly provided, otherwise
2. the script-relative repo root derived from `__file__`

Also added `scripts/tests/test_project_progress_audit.py` to cover both script-relative root resolution and `HQ_ROOT_DIR` override behavior.

## Prevention

- HQ scripts that operate on repo-local files should resolve paths from `HQ_ROOT_DIR` or from the script location, not from the workspace container root.
- CEO startup/runbook commands should be executable from the canonical HQ repo checkout without hidden cwd assumptions.
- When a health command fails with a missing-file error, verify the path contract first before assuming the underlying registry/artifact is actually absent.

## References

- Script: `scripts/project-progress-audit.py`
- Test: `scripts/tests/test_project_progress_audit.py`
- Roadmap registry: `dashboards/PROJECTS.md`
