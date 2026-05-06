# Feature Brief: APG Rare Backgrounds

- Work item id: dc-apg-rare-backgrounds
- Website: dungeoncrawler
- Module: dungeoncrawler_content
- Status: deferred
- Defer reason: Gap-analysis coverage item captured for later PM triage; not assumed to be part of the current implementation slice.
- Priority: P2
- PM owner: pm-dungeoncrawler
- Dev owner: dev-dungeoncrawler
- QA owner: qa-dungeoncrawler
- Depends on: dc-cr-background-system, dc-cr-conditions
- Source: PF2E Advanced Player's Guide, Chapter 1: Ancestries & Backgrounds
- Category: game-mechanic
- Created: 2026-04-25

## Goal

Support APG rare backgrounds such as Haunted, Returned, Royalty, and Fey-Touched, including GM-approval gating and their nonstandard background perks like automatic feat grants, fortune effects, and fright-inducing drawbacks.

## Source reference

> Rare backgrounds follow the normal background chassis but require GM access and can add unusual mechanics such as `Fey's Fortune`, entity-assisted skill checks, or automatic feat grants.

## Implementation hint

Extend the background model with rarity/access controls and optional effect hooks beyond fixed boosts, skill training, and lore. This needs support for once-per-day fortune actions, automatic feat grants like Diehard, and condition effects such as frightened values that override normal reduction expectations.

## Mission alignment

- [x] Aligns with democratized community game experience
- [x] Does not add surveillance or restrict community access
