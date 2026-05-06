# Feature Brief: Oracle Class

- Work item id: dc-apg-oracle-class
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-character-class, dc-cr-focus-spells, dc-cr-spellcasting
- Source: PF2E Advanced Player's Guide, Chapter 2: Classes
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Implement the Oracle as a divine spontaneous caster with mystery selection, revelation spells, a two-point focus pool, and the escalating oracular curse progression that defines the class.

## Source reference

> Oracle chooses a mystery at character creation, learns revelation spells as focus spells, and advances through curse stages from basic to minor, moderate, and later major or extreme states.

## Implementation hint

Add oracle as a class package layered on top of the spellcasting and focus-spell systems. It needs mystery-specific spell lists and revelation options, curse stage state tracking, signature-spell handling, and the special refocus and overwhelmed rules that make oracular curse management a core gameplay loop.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
