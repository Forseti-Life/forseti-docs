# Feature Brief: APG Archetype Dedications

- Work item id: dc-apg-archetype-dedications
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-action-economy, dc-cr-animal-companion, dc-cr-familiar, dc-cr-focus-spells, dc-cr-multiclass-archetype
- Source: PF2E Advanced Player's Guide, Chapter 3: Archetypes
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Support the APG's non-multiclass archetype catalog, including dedication feat gating, the "two feats before another dedication" restriction, and specialist archetypes such as Beastmaster, Cavalier, Marshal, Medic, Ritualist, Scroll Trickster, and Vigilante.

## Source reference

> Archetype feats are specialization options gated by a Dedication feat, and APG adds dozens of archetypes with bespoke actions, auras, companions, focus spells, and proficiency-scaling rules.

## Implementation hint

Model archetypes as content bundles with dedication prerequisites, feat trees, and optional subsystem hooks. Reuse the existing archetype foundation for the general dedication rule, but extend it for non-multiclass archetypes that grant animal companions, marshal auras, reactive actions, downtime activities, scroll tricks, stance effects, or retraining exceptions.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
