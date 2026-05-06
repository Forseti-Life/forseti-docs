# Feature Brief: Orc Ancestry

- Work item id: dc-apg-orc-ancestry
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-ancestry-system, dc-cr-ancestry-traits, dc-cr-heritage-system, dc-cr-languages
- Source: PF2E Advanced Player's Guide, Chapter 1: Ancestries & Backgrounds
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Add Orc as a playable ancestry with its no-flaw stat block and heritage set covering harsh-terrain adaptation, martial weapon readiness, enhanced darkvision, negative healing, and physical resistance.

## Source reference

> Orcs are Uncommon Medium ancestries with HP 10, Speed 25, Strength plus free boosts, no listed ability flaw, and Darkvision.

## Implementation hint

Create the orc ancestry record and a heritage set including Badlands, Battle-Ready, Deep, Grave, Hold-Scarred, and Rainfall orcs. The ancestry needs support for no-flaw validation, negative-healing interactions on Grave Orc, and resistance or terrain modifiers that scale by level or environment.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
