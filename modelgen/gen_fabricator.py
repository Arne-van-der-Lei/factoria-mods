"""Fabricators — boxy chassis, chamfered top, a visible crank on one exposed face.

The animation IS the silhouette. Feed ports sit at tile edges; roof greeble is
limited to one vent plus one lamp so the crank stays the read.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402


def build(name, accent, glow_cell, tier):
    body = F.join([
        F.box(name + "_chassis", 2.6, 2.6, 1.35, cell="steel_mid", bevel=0.05, z=0.12),
        F.box(name + "_plinth", 2.85, 2.85, 0.14, cell="cast_iron", bevel=0.03),
        F.box(name + "_hood", 2.2, 2.2, 0.30, cell="gunmetal", bevel=0.04, z=1.47),
        F.box(name + "_vent", 0.55, 0.55, 0.16, cell=accent, bevel=0.02, x=-0.7, y=0.7, z=1.77),
        # feed ports at two tile edges
        F.box(name + "_portin", 0.60, 0.16, 0.32, cell=accent, bevel=0.02, y=-1.34, z=0.55),
        F.box(name + "_portout", 0.60, 0.16, 0.32, cell=accent, bevel=0.02, y=1.34, z=0.55),
    ], name)

    crank = F.join([
        F.cylinder(name + "_wheel", r=0.46, h=0.10, cell=accent, seg=14),
        F.box(name + "_spoke0", 0.86, 0.08, 0.06, cell="gunmetal", bevel=0.01, z=0.05),
        F.box(name + "_spoke1", 0.08, 0.86, 0.06, cell="gunmetal", bevel=0.01, z=0.05),
        F.cylinder(name + "_pin", r=0.07, h=0.16, cell="rust", seg=8, x=0.34, z=0.05),
    ], "ANIM_Crank")
    crank.location = (1.32, 0.0, 0.80)
    crank.rotation_euler = (0.0, 1.5708, 0.0)
    F.parent(crank, body)

    for i in range(tier):
        F.parent(F.plate(f"GLOW_Status{i}", 0.14, 0.05, cell=glow_cell,
                         x=-0.5 + i * 0.22, y=-1.31, z=1.10), body)
    return body


F.reset()
F.export(build("fabricator_1", "rust", "e_ember", 1), "fabricator_1", budget=1500)
F.reset()
F.export(build("fabricator_2", "copper", "e_science_blue", 2), "fabricator_2", budget=1500)
F.reset()
F.export(build("fabricator_3", "brass", "e_science_green", 3), "fabricator_3", budget=1500)

# Archive — a reader of old data: low drum with a glyph ring.
F.reset()
archive = F.join([
    F.box("archive_base", 2.8, 2.8, 0.55, cell="cast_iron", bevel=0.04),
    F.box("archive_desk", 2.3, 2.3, 0.45, cell="steel_mid", bevel=0.04, z=0.55),
    F.cylinder("archive_drum", r=0.85, h=0.75, cell="weathered_stone", seg=16, z=1.00),
    F.cylinder("archive_cap", r=0.95, h=0.10, cell="copper_patina", seg=16, z=1.75),
    *[F.box(f"archive_slot{i}", 0.30, 0.12, 0.20, cell="gunmetal", bevel=0.01,
            x=-0.9 + i * 0.6, y=-1.18, z=0.72) for i in range(4)],
], "archive")
ring = F.cylinder("GLOW_GlyphRing", r=1.02, h=0.05, cell="e_hologram", seg=20, z=1.86)
F.parent(ring, archive)
F.export(archive, "archive", budget=1500)

# Breaker — a shipbreaker's maw: captured Warden jaw geometry, chained down.
F.reset()
breaker = F.join([
    F.box("breaker_cradle", 2.8, 2.8, 0.60, cell="cast_iron", bevel=0.04),
    F.box("breaker_housing", 2.0, 2.2, 0.95, cell="steel_mid", bevel=0.04, z=0.60),
    F.box("breaker_hopper", 1.4, 1.0, 0.45, cell="rust", bevel=0.03, y=0.9, z=1.55),
    *[F.box(f"breaker_chain{i}", 0.10, 0.10, 0.95, cell="gunmetal", bevel=0.01,
            x=1.05 * (1 if i % 2 else -1), y=-0.85 + i * 0.1, z=0.60) for i in range(4)],
], "breaker")
for side, sgn in (("L", -1), ("R", 1)):
    jaw = F.join([
        F.box(f"breaker_jawplate{side}", 1.25, 0.22, 0.40, cell="galvanized", bevel=0.03),
        *[F.cone(f"breaker_tooth{side}{i}", r_bottom=0.11, r_top=0.02, h=0.34,
                 cell="fang_bone", seg=6, x=-0.45 + i * 0.3, z=0.40) for i in range(4)],
    ], f"ANIM_Jaw{side}")
    jaw.location = (0.0, sgn * 0.55, 1.55)
    F.parent(jaw, breaker)
    F.parent(F.plate(f"GLOW_Tip{side}", 0.9, 0.06, cell="e_alert", y=sgn * 0.62, z=1.98), breaker)
F.export(breaker, "breaker", budget=1500)
