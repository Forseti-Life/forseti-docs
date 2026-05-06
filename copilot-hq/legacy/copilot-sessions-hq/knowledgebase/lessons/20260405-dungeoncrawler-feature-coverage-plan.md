# Plan: Dungeoncrawler Full PF2E Feature Coverage

**Created:** 2026-04-05
**Owner:** CEO (Forseti)
**Inbox item:** `sessions/ceo-copilot/inbox/20260405-dungeoncrawler-full-feature-coverage/`

---

## Context

All 9 PF2E source books have been fully extracted into 45 reference files
(~12,700 lines of mechanical requirements) at:
`forseti.life/docs/dungeoncrawler/PF2requirements/references/`

As of 2026-04-05: 39 features in the index, 16 fully groomed, 7 ready, 7 in_progress,
24 deferred stubs, 1 shipped. ~150–300 additional features are unrepresented.

---

## Three phases

### Phase 1 — Gap Analysis (ba-dungeoncrawler)
Read all 45 reference files. Compare to `features/dc-feature-index.md`.
Create `features/dc-cr-<slug>/feature.md` stubs for every unrepresented mechanical system.
Update `dc-feature-index.md` with Category + Depends on for each new row.

Dispatch as `needs-ba-dungeoncrawler-gap-analysis` inbox item (ROI=40).

### Phase 2 — Feature Grooming (ba-dungeoncrawler, repeating batches)
For each stub: generate AC + implementation notes + test plan. Set Status: ready.
PM-dungeoncrawler assigns Tier (1=core, 2=extended, 3=advanced).
Keep 10–20 features in `ready` state ahead of the release pipeline.

### Phase 3 — Release Pipeline (CEO-driven, every cycle)
CEO scope-activates 5 Tier 1 ready features per cycle:
`bash scripts/pm-scope-activate.sh dungeoncrawler <feature-id>`

Dev implements → QA validates → PM signs off → cycle advances → repeat.

---

## Key paths
- Feature stubs: `features/dc-cr-*/`
- Feature index: `features/dc-feature-index.md`
- Reference files: `forseti.life/docs/dungeoncrawler/PF2requirements/references/`
- CEO inbox item: `sessions/ceo-copilot/inbox/20260405-dungeoncrawler-full-feature-coverage/`
- Active release: `tmp/release-cycle-active/dungeoncrawler.release_id`

## Definition of done
Every feature in `dc-feature-index.md` has Status: shipped.
