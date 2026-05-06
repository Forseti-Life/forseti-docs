# Feature Brief: APG Versatile Heritages

- Work item id: dc-apg-versatile-heritages
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-ancestry-feat-schedule, dc-cr-ancestry-system, dc-cr-heritage-system
- Source: PF2E Advanced Player's Guide, Chapter 1: Ancestries & Backgrounds
- Category: rule-system
- Created: 2026-04-25

## Goal

Implement the APG versatile heritage overlay system so changelings, dhampirs, aasimars, duskwalkers, and tieflings can replace a character's normal heritage while preserving ancestry-feat access and applying special sense-upgrade and trait rules.

## Source reference

> A versatile heritage replaces the character's normal heritage choice, grants its own traits and feat list, and still allows access to the base ancestry's ancestry feats.

## Implementation hint

Extend heritage selection to support an overlay heritage that replaces the normal ancestry heritage slot, can grant senses or upgrade low-light vision to darkvision, and attaches a second feat list without stacking base heritage abilities. This system also needs support for passive rules like dhampir negative healing and duskwalker haunt detection.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
