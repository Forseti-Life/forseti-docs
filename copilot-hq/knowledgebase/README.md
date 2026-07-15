<!-- REVIEWED: 2026-07-15 -->
# Continuous Improvement Knowledgebase

This is a shared, cross-agent learning system for capturing mistakes, regressions, and improvements.

## What goes here
- **Lessons learned** (mistakes + prevention)
- **Playbooks** (how we do something reliably)
- **Proposals** for improving instructions and processes

## How agents use this
1. Before starting work, read:
   - this `knowledgebase/README.md`
   - the target repo's **instructions.md** (see below)
2. While working, add new lessons when we hit a failure mode.
3. Suggest improvements by creating a proposal file.

## Required reading: target repo instructions
All agents MUST read the target repository instructions before making changes.

For the forseti.life repo, this is:
- `forseti.life/.github/instructions/instructions.md`

Agents may propose edits to that file via the proposal process below.

## Adding a lesson
Create: `knowledgebase/lessons/YYYYMMDD-short-title.md`
Use template: `templates/lesson-learned.md`

## Proposing instruction changes
Create: `knowledgebase/proposals/YYYYMMDD-instructions-change-<short>.md`
Use template: `templates/instructions-change-proposal.md`

Proposals should include:
- the problem/rationale
- the minimal change
- risks
- a suggested diff snippet

CEO/human owner reviews and approves before changes are applied to the target repo.

## Agentic Development Readiness

- **Quick start:** Start with this README, then inspect the local architecture and install guides before changing code.
- **Key entry points:** `copilot-hq/knowledgebase/README.md`
- **Verification:** Run the narrowest existing tests or validation commands that exercise this component before marking work complete.
- **Source of truth:** Treat the checked-in code and documentation under this component directory as the authoritative reference before updating adjacent layers.
- **Architecture map:** Document the core runtime, source, and documentation entry points for this component.
