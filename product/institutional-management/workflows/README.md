<!-- REVIEWED: 2026-07-15 -->
# Institutional Management Workflows

---

## Overview

This directory contains process flow documentation for all core institutional management workflows. Each workflow defines the steps, actors, decisions, and data requirements needed to complete business processes.

**Approach**: Process-first documentation. We define workflows first, then derive data entities and fields from the process requirements.

---

## Core Workflows

### Phase 1: Must-Have (MVP)

| Workflow | Status | Priority | Dependencies |
|----------|--------|----------|--------------|
| [Institution Onboarding](./institution-onboarding.md) | 🔲 Draft | P0 | None |
| [Staff Registration & Onboarding](./staff-onboarding.md) | 🔲 Pending | P0 | Institution |
| [Participant Enrollment](./participant-enrollment.md) | 🔲 Pending | P0 | Institution, Staff |
| [Daily Check-In/Check-Out](./daily-checkin-checkout.md) | 🔲 Pending | P0 | Participant |
| [Incident Reporting & Response](./incident-management.md) | 🔲 Pending | P0 | Participant, Staff |
| [Payment Processing](./payment-processing.md) | 🔲 Pending | P0 | Institution |

### Phase 2: Enhanced Operations

| Workflow | Status | Priority | Dependencies |
|----------|--------|----------|--------------|
| Staff Shift Scheduling | 🔲 Pending | P1 | Staff |
| Progress Tracking | 🔲 Pending | P1 | Participant |
| Document Management | 🔲 Pending | P1 | All entities |
| Parent Communication | 🔲 Pending | P1 | Participant |
| Compliance Reporting | 🔲 Pending | P1 | All entities |

### Phase 3: Advanced Features

| Workflow | Status | Priority | Dependencies |
|----------|--------|----------|--------------|
| Multi-Location Management | 🔲 Pending | P2 | Institution |
| Asset Management | 🔲 Pending | P2 | Institution |
| Marketing & Inquiries | 🔲 Pending | P2 | Institution |
| Advanced Analytics | 🔲 Pending | P2 | All entities |

---

## Workflow Documentation Template

Each workflow document should include:

1. **Overview** - Purpose and scope
2. **Actors** - Who participates (roles)
3. **Preconditions** - What must exist before starting
4. **Process Steps** - Detailed step-by-step flow
5. **Decision Points** - Where branching occurs
6. **Data Requirements** - What data is needed/created
7. **Validation Rules** - Business rules and constraints
8. **Success Criteria** - What defines completion
9. **Error Handling** - What happens when things fail
10. **Derived Entities** - What data structures are needed

---

## Workflow Notation

### Process Steps
```
1. User Action
   → System Response
   → Data Created/Updated
   
2. Decision Point
   ✓ If condition A → Step 3
   ✗ If condition B → Step 5
```

### Actor Notation
- 👤 **User Role** - Human actor
- 🤖 **System** - Automated process
- 📧 **External System** - Third-party integration

### State Transitions
```
[Initial State] → (action) → [New State]
```

---

## Next Steps

1. Document Institution Onboarding workflow (most critical)
2. Derive entity definitions from workflow data requirements
3. Document Staff Onboarding workflow
4. Continue iterating through all Phase 1 workflows
5. Build data dictionary from accumulated requirements

---

**Maintained By**: Product Team  
**Review Frequency**: Weekly during development

## Scope covered by this document

- **Primary target:** `product/institutional-management/workflows/README.md`
- **Purpose:** the purpose of the `workflows` directory
- **Nearby files:** `founder-journey.md`, `institution-onboarding.md`

## Agentic Development Readiness

- **Quick start:** Read `product/institutional-management/workflows/README.md` and capture the current scope before editing. Cross-check `product/institutional-management/workflows/founder-journey.md` to align terms, boundaries, and linked issue context. Align with parent context in `product/institutional-management/README.md` before finalizing the readiness block.
- **Key entry points:** `product/institutional-management/workflows/founder-journey.md`, `product/institutional-management/workflows/institution-onboarding.md`
- **Verification:** Run `git --no-pager grep -n "## Agentic Development Readiness" "product/institutional-management/workflows/README.md"`; then run `git --no-pager grep -n "^#" "product/institutional-management/workflows/founder-journey.md"`.
- **Source of truth:** Treat the checked-in code and documentation under this component directory as the authoritative reference before updating adjacent layers.
- **Constraints / gotchas:** ### Phase 1: Must-Have (MVP).
- **Architecture map:** `product/institutional-management/workflows/README.md`, `product/institutional-management/workflows/founder-journey.md`, `product/institutional-management/workflows/institution-onboarding.md`
