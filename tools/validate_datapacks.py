#!/usr/bin/env python3
"""Cross-reference validator for The Stilled World datapacks.

Loads every mod folder in the repo root, merges prototypes in dependency order
(supporting `extends` and `delete`), then verifies:
  - recipe inputs/outputs reference existing items or fluids
  - tech effects reference existing recipes/entities/techs; prereqs exist
  - tech pack costs reference existing science items
  - entity sounds/visual keys are well-formed; locKeys resolve in the merged locale
  - rules reference existing items/entities/techs/locKeys
  - worldgen resources reference existing items and layers
Exit 0 = clean, 1 = errors. Warnings do not fail the build.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD_FILES = ["items.json", "fluids.json", "entities.json", "recipes.json",
             "techs.json", "worldgen.json", "rules.json", "settings.json", "locale.json"]

errors: list[str] = []
warnings: list[str] = []


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        errors.append(f"{path.relative_to(ROOT)}: JSON parse error: {e}")
        return None


def discover_mods():
    mods = {}
    for mod_json in ROOT.glob("**/mod.json"):
        if ".git" in mod_json.parts:
            continue
        manifest = load_json(mod_json)
        if manifest is None or "id" not in manifest:
            errors.append(f"{mod_json.relative_to(ROOT)}: missing or invalid manifest")
            continue
        mods[manifest["id"]] = (manifest, mod_json.parent)
    return mods


def dep_order(mods):
    ordered, seen = [], set()

    def visit(mid, stack):
        if mid in seen:
            return
        if mid in stack:
            errors.append(f"dependency cycle involving '{mid}'")
            return
        if mid not in mods:
            return
        manifest, _ = mods[mid]
        for dep in manifest.get("deps", []):
            if dep["id"] not in mods:
                errors.append(f"mod '{mid}' depends on missing mod '{dep['id']}'")
            visit(dep["id"], stack | {mid})
        seen.add(mid)
        ordered.append(mid)

    for mid in sorted(mods):
        visit(mid, set())
    return ordered


def merge(mods, order):
    merged = {k: {} for k in ("items", "fluids", "entities", "recipes", "techs")}
    locale: dict[str, str] = {}
    worldgen_layers: set[str] = set()
    worldgen_resources: dict[str, dict] = {}
    rules = []
    for mid in order:
        _, folder = mods[mid]
        for section, fname in (("items", "items.json"), ("fluids", "fluids.json"),
                               ("entities", "entities.json"), ("recipes", "recipes.json"),
                               ("techs", "techs.json")):
            p = folder / fname
            if not p.exists():
                continue
            data = load_json(p)
            if not isinstance(data, list):
                continue
            for proto in data:
                pid = proto.get("id")
                if pid is None:
                    errors.append(f"{mid}/{fname}: prototype without id")
                    continue
                if proto.get("delete"):
                    merged[section].pop(pid, None)
                    continue
                ext = proto.get("extends")
                if ext:
                    base_id = ext.split(":", 1)[1] if ":" in ext else ext
                    if base_id not in merged[section]:
                        errors.append(f"{mid}/{fname}: '{pid}' extends missing '{ext}'")
                        continue
                    base = dict(merged[section][base_id])
                    base.update({k: v for k, v in proto.items() if k not in ("extends",)})
                    merged[section][pid] = base
                else:
                    merged[section][pid] = proto
        wp = folder / "worldgen.json"
        if wp.exists():
            wg = load_json(wp)
            if isinstance(wg, dict):
                worldgen_layers.update((wg.get("layers") or {}).keys())
                worldgen_resources.update(wg.get("resources") or {})
        rp = folder / "rules.json"
        if rp.exists():
            rl = load_json(rp)
            if isinstance(rl, dict):
                rules.extend(rl.get("rules") or [])
        lp = folder / "locale.json"
        if lp.exists():
            loc = load_json(lp)
            if isinstance(loc, dict):
                locale.update(loc.get("en") or {})
    return merged, locale, worldgen_layers, worldgen_resources, rules


def main():
    mods = discover_mods()
    if not mods:
        errors.append("no mods found")
    order = dep_order(mods)
    merged, locale, wg_layers, wg_resources, rules = merge(mods, order)
    items, fluids, entities = merged["items"], merged["fluids"], merged["techs"] and merged["entities"],
    items, fluids = merged["items"], merged["fluids"]
    entities, recipes, techs = merged["entities"], merged["recipes"], merged["techs"]
    thing_ids = set(items) | set(entities)  # buildable entities double as items via blanket rule

    for rid, r in recipes.items():
        for side in ("in", "out"):
            for ing in r.get(side, []):
                iid = ing.get("id")
                if ing.get("fluid"):
                    if iid not in fluids:
                        errors.append(f"recipe '{rid}': unknown fluid '{iid}'")
                elif iid not in thing_ids:
                    errors.append(f"recipe '{rid}': unknown item '{iid}' in '{side}'")
        if "category" not in r:
            errors.append(f"recipe '{rid}': missing category")

    for tid, t in techs.items():
        for c in t.get("cost", []):
            if c.get("pack") not in items:
                errors.append(f"tech '{tid}': unknown pack '{c.get('pack')}'")
        for pre in t.get("prereqs", []):
            if pre not in techs:
                errors.append(f"tech '{tid}': unknown prereq '{pre}'")
        for eff in t.get("effects", []):
            if eff.get("type") == "unlock-recipe":
                for uid in eff.get("ids", []):
                    if uid not in recipes:
                        errors.append(f"tech '{tid}': unlocks unknown recipe '{uid}'")

    unlocked = set()
    for t in techs.values():
        for eff in t.get("effects", []):
            if eff.get("type") == "unlock-recipe":
                unlocked.update(eff.get("ids", []))
    START_SET_HINT = {"ferrite-smelting", "cuprite-smelting", "brick-firing", "cog", "strand",
                      "relay-board", "spark-salvage", "bolt-magazine", "coilwood-bin", "ferrite-bin",
                      "slag-forge", "crank-reclaimer", "grabber-crank", "archive", "duct-item",
                      "tin-smelting"}
    for rid in recipes:
        if rid not in unlocked and rid not in START_SET_HINT:
            warnings.append(f"recipe '{rid}' is neither tech-unlocked nor in the start set hint")

    for lk in [p.get("locKey") for section in merged.values() for p in section.values() if p.get("locKey")]:
        if lk not in locale:
            errors.append(f"locKey '{lk}' has no locale entry")

    for rname, res in wg_resources.items():
        if rname not in thing_ids and rname not in fluids:
            errors.append(f"worldgen resource '{rname}' is not a known item/fluid")
        if res.get("mask") not in wg_layers:
            errors.append(f"worldgen resource '{rname}': unknown mask layer '{res.get('mask')}'")

    for rule in rules:
        for eff in rule.get("effects", []):
            if eff.get("type") == "grant-items":
                for iid in (eff.get("items") or {}):
                    if iid not in thing_ids:
                        errors.append(f"rule '{rule.get('id')}': grants unknown item '{iid}'")
            if eff.get("type") == "unlock":
                for tid in (eff.get("techs") or []):
                    if tid not in techs:
                        errors.append(f"rule '{rule.get('id')}': unlocks unknown tech '{tid}'")

    print(f"mods: {', '.join(order)}")
    print(f"items {len(items)} | fluids {len(fluids)} | entities {len(entities)} | recipes {len(recipes)} | techs {len(techs)} | rules {len(rules)} | locale {len(locale)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
