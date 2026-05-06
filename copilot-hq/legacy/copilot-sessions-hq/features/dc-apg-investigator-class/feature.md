# Feature Brief: Investigator Class

- Work item id: dc-apg-investigator-class
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-action-economy, dc-cr-character-class, dc-cr-exploration-mode, dc-cr-skill-system
- Source: PF2E Advanced Player's Guide, Chapter 2: Classes
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Implement the Investigator as a playable class with lead-tracking, `Devise a Stratagem`, Strategic Strike precision damage, and methodology choices such as Alchemical Sciences, Empiricism, Forensic Medicine, and Interrogation.

## Source reference

> Investigator centers on `Pursue a Lead` and `Devise a Stratagem`, using Intelligence to plan attacks and adding precision damage when those plans pay off.

## Implementation hint

Add a character class package with lead state, once-per-round stratagem rolls, methodology-granted skills and feats, and precision damage scaling. The class needs exploration-mode support for active leads, action-economy support for stratagem timing, and class-level progression for methodology features and follow-up reactions like Clue In.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
