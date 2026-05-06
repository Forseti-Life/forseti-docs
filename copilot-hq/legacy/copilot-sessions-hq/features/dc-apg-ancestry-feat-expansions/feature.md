# Feature Brief: APG Ancestry Feat Expansions

- Work item id: dc-apg-ancestry-feat-expansions
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-ancestry-feat-schedule, dc-cr-ancestry-system
- Source: PF2E Advanced Player's Guide, Chapter 1: Ancestries & Backgrounds
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Load the APG's supplemental ancestry feats and ancestry-specific natural weapon options so core ancestries and new APG ancestries have their expanded build choices available during character creation and leveling.

## Source reference

> APG provides additional heritages, ancestry feats, and ancestry feats for all Core Rulebook ancestries; each must be loadable as ancestry feat options and related unarmed attacks must be represented with correct stats.

## Implementation hint

Extend ancestry feat content and ancestry-option loading so APG feat lists can attach to both existing core ancestries and new APG ancestries. Support new unarmed attack entries where ancestry feats grant claws, fangs, or similar natural weapons, and enforce ancestry/heritage prerequisites in the feat picker.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
