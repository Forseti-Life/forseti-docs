# Feature Brief: Swashbuckler Class

- Work item id: dc-apg-swashbuckler-class
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-action-economy, dc-cr-character-class, dc-cr-encounter-rules
- Source: PF2E Advanced Player's Guide, Chapter 2: Classes
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Implement the Swashbuckler as a Dexterity-based martial class with style selection, panache generation, Precise Strike scaling, Finisher actions, Opportune Riposte, and Vivacious Speed progression.

## Source reference

> Swashbuckler gameplay revolves around earning panache through stylish actions and spending it on Finishers that convert bravado into burst damage and tactical effects.

## Implementation hint

Add swashbuckler as a class package with style-specific panache triggers, a persistent panache state, finisher restrictions, and level-based speed and precision-damage scaling. The class needs tight integration with encounter rules, trait-based weapon checks, and action resolution because panache changes what attacks and reactions are legal on a given turn.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
