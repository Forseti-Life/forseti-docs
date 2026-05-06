# Feature Brief: Witch Class

- Work item id: dc-apg-witch-class
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-character-class, dc-cr-familiar, dc-cr-focus-spells, dc-cr-spellcasting
- Source: PF2E Advanced Player's Guide, Chapter 2: Classes
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Implement the Witch as an Intelligence-based prepared caster whose patron theme sets spell tradition, familiar-granted spells, hex cantrip, and lesson progression, with the familiar acting as the class's spell repository.

## Source reference

> Witch spellcasting is mediated through a mandatory familiar that stores the class's spells, while hexes and lessons add focus-spell and patron-driven progression on top of prepared casting.

## Implementation hint

Add witch as a class package that reuses spellcasting, familiar, and focus-spell systems but layers in patron themes, familiar spellbook behavior, one-hex-per-turn enforcement, and lesson-based expansion of hexes and granted spells. Replacement-familiar behavior must preserve known spells so the class does not lose progression on familiar death.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
