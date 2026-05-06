# Feature Brief: Kobold Ancestry

- Work item id: dc-apg-kobold-ancestry
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

Add Kobold as a playable ancestry with draconic exemplar selection, damage-type and breath-shape mapping, and heritage options such as Cavern, Dragonscaled, Spellscale, Strongjaw, and Venomtail.

## Source reference

> Kobolds are Small Uncommon ancestries with HP 6, Darkvision, Dexterity/Charisma/Free boosts, a Constitution flaw, and a 1st-level draconic exemplar that drives multiple ancestry abilities.

## Implementation hint

Model draconic exemplar as an ancestry-linked choice that stores dragon type, damage type, breath shape, and save type for later feat and heritage resolution. Heritage entries should cover exemplar-based resistance, innate cantrips, climbing and squeeze modifiers, jaws attacks, and the once-per-day `Tail Toxin` weapon-poison rider.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
