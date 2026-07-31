"""Terrain, coilwood, and the ruins.

Ruin husks are readable broken versions of live machines — recognition is the
storytelling. Their GLOW children stay emissive-black (dead sockets read as eyes);
a BONE salvage-tag glyph recurs across the set, so one prior survivor threads the
whole environment. The Arc Forge shell holds the set's single live ember.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402


def salvage_tag(name, x=0.0, y=0.0, z=0.0):
    """The recurring mark of the one who came before."""
    return F.plate(name, 0.18, 0.12, cell="fang_bone", x=x, y=y, z=z)


# --- Cliffs: wall, corner, ramp; 1 m grid, ~1.5 m plateau step ---------------
F.reset()
F.export(F.join([
    F.box("cliff_face", 1.0, 0.55, 1.5, cell="granite", bevel=0.05),
    F.box("cliff_rubble", 1.0, 0.35, 0.28, cell="slate", bevel=0.04, y=-0.42),
    F.rock("cliff_boulder", 0.22, cell="basalt", x=0.32, y=-0.5, seed=3),
], "cliff_wall"), "cliff_wall", budget=300)

F.reset()
F.export(F.join([
    F.box("cliff_cx", 0.62, 1.0, 1.5, cell="granite", bevel=0.05, x=-0.19),
    F.box("cliff_cy", 1.0, 0.62, 1.5, cell="granite", bevel=0.05, y=0.19),
    F.rock("cliff_cnub", 0.26, cell="slate", x=0.3, y=-0.3, seed=7),
], "cliff_corner"), "cliff_corner", budget=300)

F.reset()
ramp = F.join([
    F.box("ramp_bed", 2.0, 3.0, 0.3, cell="dry_earth", bevel=0.03),
    F.box("ramp_riseA", 2.0, 1.0, 0.6, cell="dry_earth", bevel=0.03, y=0.5),
    F.box("ramp_riseB", 2.0, 1.0, 1.0, cell="dry_earth", bevel=0.03, y=1.2),
    F.box("ramp_wallL", 0.25, 3.0, 1.5, cell="granite", bevel=0.04, x=-1.1),
    F.box("ramp_wallR", 0.25, 3.0, 1.5, cell="granite", bevel=0.04, x=1.1),
], "cliff_ramp")
F.export(ramp, "cliff_ramp", budget=400)

# --- Water edge trim + scar tile --------------------------------------------
F.reset()
F.export(F.join([
    F.plate("water_plane", 1.0, 1.0, cell="deep_water", z=0.02),
    F.plate("water_foam", 1.0, 0.22, cell="shallow_water", y=-0.39, z=0.03),
], "water_edge"), "water_edge", budget=100)

F.reset()
scar = F.join([
    F.plate("scar_ground", 3.0, 3.0, cell="loam_dark", z=0.01),
    *[F.box(f"scar_lip{i}", 0.5, 0.16, 0.09, cell="basalt", bevel=0.02,
            x=-0.9 + i * 0.6, y=(-1.0 if i % 2 else 1.0), z=0.01) for i in range(4)],
], "scar_tile")
# the crack glow is the SAME uranium pulse as the Delver bore: "build here"
for i in range(3):
    F.parent(F.plate(f"GLOW_Crack{i}", 1.9, 0.07, cell="e_uranium",
                     y=-0.6 + i * 0.6, z=0.02), scar)
F.export(scar, "scar_tile", budget=300)

# --- Coilwood: dead cable-growths -------------------------------------------
F.reset()
tree = F.join([
    F.cylinder("coil_trunk", r=0.14, h=2.4, cell="bark", seg=7),
    F.cone("coil_crownA", r_bottom=0.85, r_top=0.15, h=1.1, cell="pine", seg=7, z=1.6),
    F.cone("coil_crownB", r_bottom=0.6, r_top=0.1, h=0.9, cell="forest_shadow", seg=7, z=2.3),
    F.cylinder("coil_cableA", r=0.045, h=1.3, cell="copper_patina", seg=5, x=0.16, z=0.7),
    F.cylinder("coil_cableB", r=0.04, h=1.0, cell="copper_deep", seg=5, x=-0.13, y=0.1, z=0.9),
], "coilwood_tree")
F.export(tree, "coilwood_tree", budget=300)

F.reset()
F.export(F.join([
    F.rock("deco_r0", 0.30, cell="granite", seed=1),
    F.rock("deco_r1", 0.19, cell="slate", x=0.42, y=0.18, seed=5),
    F.rock("deco_r2", 0.13, cell="weathered_stone", x=-0.3, y=0.3, seed=9),
], "rock_deco"), "rock_deco", budget=200)

# --- Ruin husks: six broken machines, each recognizable ---------------------
F.reset()
h = F.join([  # a fallen High Pylon lying across the ground — the spawn landmark
    F.truss("husk_pylon_mast", 1.1, 6.0, cell="rust", bars=5, thickness=0.10),
    F.box("husk_pylon_base", 1.8, 1.8, 0.22, cell="basalt", bevel=0.03, z=-0.1),
], "ruin_fallen_pylon")
h.rotation_euler = (0.0, 1.35, 0.4)
F.join([h, salvage_tag("husk_pylon_tag", x=0.6, z=0.6)], "ruin_fallen_pylon")
F.export(h, "ruin_fallen_pylon", budget=800)

F.reset()
h = F.join([  # snapped Arc Forge shell — holds the set's one live ember
    F.box("husk_forge_body", 2.6, 1.4, 1.5, cell="rust", bevel=0.05),
    F.box("husk_forge_shard", 1.1, 1.2, 0.9, cell="cast_iron", bevel=0.04, x=1.5, z=0.1),
    F.box("husk_forge_plinth", 2.9, 2.9, 0.18, cell="basalt", bevel=0.03),
    salvage_tag("husk_forge_tag", x=-0.9, y=-0.72, z=0.8),
], "ruin_forge_shell")
F.parent(F.plate("GLOW_LastEmber", 0.18, 0.10, cell="e_furnace", y=-0.71, z=0.35), h)
F.export(h, "ruin_forge_shell", budget=800)

F.reset()
F.export(F.join([  # half-buried Rollway spine
    F.box("husk_spine_bed", 0.9, 4.0, 0.14, cell="rust", bevel=0.02),
    F.box("husk_spine_rail", 0.07, 4.0, 0.10, cell="cast_iron", bevel=0.01, x=-0.4, z=0.14),
    F.box("husk_spine_broken", 0.9, 1.1, 0.12, cell="rust", bevel=0.02, y=2.6, z=0.35),
    salvage_tag("husk_spine_tag", y=-1.2, z=0.15),
], "ruin_rollway_spine"), "ruin_rollway_spine", budget=400)

F.reset()
h = F.join([  # dead Goliath on its side — the most eloquent husk
    F.box("husk_gol_thorax", 1.65, 2.3, 0.9, cell="chitin_dark", bevel=0.05, z=0.45),
    F.box("husk_gol_head", 1.05, 0.9, 0.7, cell="hide_dark", bevel=0.04, y=-1.5, z=0.4),
    *[F.box(f"husk_gol_leg{i}", 0.18, 0.18, 0.8, cell="chitin_dark", bevel=0.02,
            x=(-0.8 if i % 2 else 0.8), y=-0.5 + (i // 2) * 0.8, z=0.9) for i in range(6)],
    salvage_tag("husk_gol_tag", x=0.4, y=0.3, z=0.92),
], "ruin_dead_goliath")
h.rotation_euler = (1.35, 0.0, 0.6)
F.parent(F.plate("GLOW_DeadEyes", 0.3, 0.07, cell="hazard_black", y=-1.85, z=0.55), h)
F.export(h, "ruin_dead_goliath", budget=800)

F.reset()
F.export(F.join([  # collapsed bin stack
    F.box("husk_bin0", 0.9, 0.9, 0.8, cell="rust", bevel=0.03),
    F.box("husk_bin1", 0.85, 0.85, 0.75, cell="cast_iron", bevel=0.03, x=0.5, y=0.4, z=0.8),
    F.box("husk_bin2", 0.8, 0.8, 0.7, cell="rust", bevel=0.03, x=-0.6, y=0.2),
    salvage_tag("husk_bin_tag", x=0.0, y=-0.47, z=0.5),
], "ruin_bin_stack"), "ruin_bin_stack", budget=400)

F.reset()
F.export(F.join([  # cracked dome fragment
    F.cone("husk_dome", r_bottom=2.1, r_top=1.3, h=1.1, cell="weathered_stone", seg=10),
    F.box("husk_dome_crack", 0.2, 2.2, 1.2, cell="basalt", bevel=0.03, x=0.7),
    salvage_tag("husk_dome_tag", x=-1.1, y=-0.6, z=0.7),
], "ruin_dome"), "ruin_dome", budget=500)

# --- Cache husk: pry-open lid, ember seam -----------------------------------
F.reset()
cache = F.join([
    F.box("cache_shell", 1.2, 0.9, 0.62, cell="cast_iron", bevel=0.03),
    F.box("cache_foot", 1.3, 1.0, 0.10, cell="basalt", bevel=0.02),
    salvage_tag("cache_tag", y=-0.46, z=0.34),
], "cache_husk")
lid = F.box("ANIM_Lid", 1.16, 0.86, 0.12, cell="galvanized", bevel=0.02)
lid.location = (0.0, -0.43, 0.62)  # pivot at the front hinge
F.parent(lid, cache)
F.parent(F.plate("GLOW_Seam", 1.05, 0.05, cell="e_ember", z=0.60), cache)
F.export(cache, "cache_husk", budget=300)

# --- Memory post: dormant until touched -------------------------------------
F.reset()
post = F.join([
    F.box("mem_plinth", 0.5, 0.5, 0.16, cell="basalt", bevel=0.02),
    F.box("mem_shaft", 0.28, 0.22, 2.0, cell="weathered_stone", bevel=0.03, z=0.16),
    F.box("mem_break", 0.30, 0.24, 0.16, cell="granite", bevel=0.02, x=0.03, z=2.02),
], "memory_post")
F.parent(F.plate("GLOW_Glyph", 0.20, 0.5, cell="e_hologram", y=-0.12, z=1.2), post)
F.export(post, "memory_post", budget=300)
