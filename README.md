# The Stilled World — Mod SDK & Base Game Data

This repository contains **everything a mod author needs** for *The Stilled World*, a
Factorio-inspired automation game built as a VRChat world — and the shipped game itself,
because **the base game is a mod**: the entire vanilla experience (items, machines,
recipes, research, world generation, tutorial, victory) is defined as a datapack in
[`base/`](base/), loaded through the exact same pipeline as any community mod.

> The planet was a world-scale factory called the Lattice. It shut itself down when its
> caretaker mind judged that running unserved was pointless. Only the Wardens — the grid's
> immune drones — kept their patrol. You are a Reclaimer. Relight the World-Beacon.

## Repository layout

```
core/               Engine-required minimum (character prototype, error assets, UI strings)
base/               The vanilla game — the reference implementation for modders
peaceful/           Official variant mod: deletes Warden spawners
quickstart/         Official variant mod: bigger starter kit + pre-decoded tier 1
deathwatch/         Official variant mod: Static/evolution curves cranked
sandbox/            Official variant mod: free build, no costs
examples/testmod/   Documented example mod (adds one ore + one recipe override)
schemas/            JSON Schemas per file type — the source of truth for validation
modelgen/           Blender Python model-generation pipeline (headless, Blender 4.5 LTS)
tools/              pack_mod.py (fold a mod folder into a web bundle) + validators
```

## What a mod is

A folder (or single-file web bundle) of JSON:

| File | Contents |
|---|---|
| `mod.json` | id, version, dependencies, description |
| `items.json` | items: category, stack size, fuel value, visual binding |
| `fluids.json` | fluid definitions (separate id namespace) |
| `entities.json` | machines/structures: prototype category + parameters |
| `recipes.json` | crafting recipes (integer tick times, deterministic ratios) |
| `techs.json` | research tree: costs, prereqs, typed effects |
| `worldgen.json` | declarative world generation (noise layers, terrain rules, resources) |
| `rules.json` | trigger→effect gameplay rules (objectives, victory conditions, events) |
| `settings.json` | tunables (per-platform budget pairs supported) |
| `locale.json` | all player-facing strings |
| `models/` | FBX models (local mods only; web bundles reuse + recolor existing meshes) |

Mods merge in dependency order. Later mods may **add**, **override by id**
(`"extends": "base:fabricator-1"` — change only the fields that differ), or **delete**.
No code, ever: gameplay logic is expressed through prototype parameters and the
declarative rule layer, which keeps every mod deterministic and multiplayer-safe.

## Web mods

Mods can be loaded **at runtime, in VRChat, from a URL** — no world re-upload:

1. `python tools/pack_mod.py mymod/` → `mymod.factoriamod.json`
2. Host it on GitHub (raw), Gist, or Pastebin (VRChat-trusted domains — players need no settings changes)
3. Paste the URL at the in-world lobby console

All players in the instance must hold byte-identical packs (hash-locked before the game
starts) — the lobby shows readiness per player. Web bundles can add data, rules, worldgen,
and re-skin existing meshes via the closed `visual` block; new geometry requires a local
mod shipped with the world.

## Rules for submissions

- **License**: content must be redistributable (CC0 or your own work).
- **No third-party IP.** Explicitly: no Factorio assets, sprites, names, or data — this
  project's original identity is deliberate. Submissions that import them are rejected.
- Stay inside the Quest performance budgets documented in `MODDING.md`.
- VRChat Terms of Service apply to everything.

## Status

Pre-release — the world is in active development. Schemas and formats may change until
v1.0; the `CHANGELOG.md` records format versions and engine compatibility.

*The Stilled World is an original game inspired by the factory-automation genre.
It is not affiliated with or endorsed by Wube Software.*
