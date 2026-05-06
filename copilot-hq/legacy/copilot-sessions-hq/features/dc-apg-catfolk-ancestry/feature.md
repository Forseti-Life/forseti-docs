# Feature Brief: Catfolk Ancestry

- Work item id: dc-apg-catfolk-ancestry
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

Add Catfolk as a playable ancestry with its stat block, `Land on Your Feet` passive, and heritage set including Clawed, Hunting, Jungle, and Nine Lives catfolk options.

## Source reference

> Catfolk are Uncommon Medium ancestries with HP 8, Speed 25, Dex/Cha/Free boosts, a Wisdom flaw, low-light vision, and a passive that halves fall damage and prevents landing prone.

## Implementation hint

Create a catfolk ancestry record plus heritage records that add claw attacks, scent-based tracking, undergrowth movement benefits, and critical-hit dying mitigation. Store Amurrun as the ancestry language, apply Catfolk/Humanoid traits, and wire the ancestry to ancestry feat and heritage selection flows.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
