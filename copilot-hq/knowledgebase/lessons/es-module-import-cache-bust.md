
## 2026-09-08 — Drupal library versions do not bust transitive ES modules

When Drupal serves an entrypoint module through `libraries.yml`, the library `version:` query string only applies to the declared asset (for example `js/dungeon-editor.js`). Browser module caches may continue reusing transitive imports unless each import specifier changes.

Rule: for browser ES-module chains, hardcode and bump a shared `?v=<stamp>` at every relative import site in that chain whenever any module in the chain changes. Keep all stamps in the editor chain identical and enforce with a lightweight Node contract test. Be careful with shared modules: different query strings create separate module instances on the same page, so avoid mixed stamps in pages that load both chains.
