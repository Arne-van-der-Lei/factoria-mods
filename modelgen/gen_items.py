"""Item meshes — ~30 tris each. These are the DrawMeshInstanced belt items,
so every triangle here is multiplied by hundreds on screen.

The five Sparks form a silhouette ladder that reads as a tech tree in grayscale:
shard cluster -> riveted can -> coil-wrapped -> fluid vial -> caged core.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402

S = 0.30  # nominal item size in meters


def simple(name, builder, budget=60):
    F.reset()
    F.export(builder(name), name, budget=budget)


# --- Raw / ore-like ---------------------------------------------------------
simple("item_ferrite_shard", lambda n: F.join([
    F.rock(n + "_a", S * 0.42, cell="iron_blue", seed=2),
    F.rock(n + "_b", S * 0.28, cell="slate", x=S * 0.32, y=S * 0.2, seed=6),
], n))
simple("item_cuprite", lambda n: F.join([
    F.rock(n + "_a", S * 0.42, cell="copper", seed=4),
    F.rock(n + "_b", S * 0.26, cell="copper_deep", x=S * 0.3, y=-S * 0.2, seed=8),
], n))
simple("item_cinder", lambda n: F.join([
    F.rock(n + "_a", S * 0.40, cell="coal_black", seed=1),
    F.rock(n + "_b", S * 0.26, cell="hazard_black", x=S * 0.3, seed=5),
], n))
simple("item_regolith", lambda n: F.join([
    F.rock(n + "_a", S * 0.40, cell="weathered_stone", seed=3),
    F.rock(n + "_b", S * 0.24, cell="limestone", x=-S * 0.28, y=S * 0.22, seed=7),
], n))
simple("item_corium", lambda n: F.join([
    F.rock(n + "_a", S * 0.40, cell="olive_scrub", seed=11),
    F.plate("GLOW_Vein", S * 0.5, S * 0.12, cell="e_uranium", z=S * 0.3),
], n))
simple("item_coilwood", lambda n: F.join([
    F.cylinder(n + "_log", r=S * 0.22, h=S * 0.8, cell="bark", seg=6),
    F.cylinder(n + "_wire", r=S * 0.05, h=S * 0.9, cell="copper_patina", seg=4, x=S * 0.18),
], n))

# --- Bars / bricks / plates -------------------------------------------------
simple("item_bar", lambda n: F.box(n, S * 0.85, S * 0.42, S * 0.20, cell="steel_light", bevel=0.012))
simple("item_brick", lambda n: F.box(n, S * 0.75, S * 0.45, S * 0.28, cell="clay", bevel=0.010))
simple("item_plate_large", lambda n: F.join([
    F.box(n + "_p", S * 1.0, S * 0.7, S * 0.10, cell="galvanized", bevel=0.010),
    F.box(n + "_rib", S * 0.2, S * 0.7, S * 0.06, cell="steel_mid", bevel=0.0, z=S * 0.10),
], n))

# --- Mechanical -------------------------------------------------------------
simple("item_cog", lambda n: F.join([
    F.cylinder(n + "_hub", r=S * 0.34, h=S * 0.14, cell="cast_iron", seg=10),
    *[F.box(n + f"_t{i}", S * 0.12, S * 0.12, S * 0.14,
            cell="cast_iron", bevel=0.0,
            x=S * 0.40 * (1 if i in (0, 3) else -1),
            y=S * 0.40 * (1 if i in (0, 1) else -1)) for i in range(4)],
], n), budget=90)
simple("item_strand", lambda n: F.join([
    F.cylinder(n + "_coil", r=S * 0.30, h=S * 0.16, cell="copper", seg=10),
    F.cylinder(n + "_core", r=S * 0.12, h=S * 0.20, cell="copper_deep", seg=6),
], n))
simple("item_board", lambda n: F.join([
    F.box(n + "_pcb", S * 0.72, S * 0.52, S * 0.06, cell="copper_patina", bevel=0.0),
    F.box(n + "_chip", S * 0.24, S * 0.20, S * 0.08, cell="machine_shadow", bevel=0.0, z=S * 0.06),
], n))
simple("item_drive", lambda n: F.join([
    F.box(n + "_block", S * 0.6, S * 0.44, S * 0.30, cell="gunmetal", bevel=0.012),
    F.cylinder(n + "_shaft", r=S * 0.08, h=S * 0.5, cell="galvanized", seg=6, x=S * 0.36, z=S * 0.15),
], n))
simple("item_cell", lambda n: F.join([
    F.cylinder(n + "_can", r=S * 0.26, h=S * 0.62, cell="steel_mid", seg=10),
    F.cylinder(n + "_cap", r=S * 0.14, h=S * 0.10, cell="brass", seg=6, z=S * 0.62),
], n))
simple("item_core", lambda n: F.join([
    F.box(n + "_cage", S * 0.55, S * 0.55, S * 0.55, cell="gunmetal", bevel=0.02),
    F.plate("GLOW_Core", S * 0.36, S * 0.36, cell="e_hologram", z=S * 0.56),
], n))
simple("item_pile", lambda n: F.join([
    F.cone(n + "_heap", r_bottom=S * 0.44, r_top=S * 0.06, h=S * 0.38, cell="hazard_yellow", seg=8),
], n))
simple("item_barrel", lambda n: F.join([
    F.cylinder(n + "_body", r=S * 0.30, h=S * 0.70, cell="rust", seg=10),
    F.cylinder(n + "_band", r=S * 0.32, h=S * 0.06, cell="gunmetal", seg=10, z=S * 0.32),
], n))
simple("item_tile", lambda n: F.box(n, S * 0.9, S * 0.9, S * 0.10, cell="limestone", bevel=0.0))
simple("item_kit", lambda n: F.join([
    F.box(n + "_case", S * 0.62, S * 0.44, S * 0.24, cell="signal_red", bevel=0.012),
    F.box(n + "_clasp", S * 0.18, S * 0.06, S * 0.06, cell="galvanized", bevel=0.0, y=-S * 0.24, z=S * 0.12),
], n))
simple("item_chip", lambda n: F.join([
    F.box(n + "_sub", S * 0.5, S * 0.5, S * 0.08, cell="machine_shadow", bevel=0.0),
    F.plate("GLOW_Trace", S * 0.34, S * 0.34, cell="e_science_blue", z=S * 0.09),
], n))
simple("item_stamp", lambda n: F.join([
    F.box(n + "_frame", S * 0.62, S * 0.62, S * 0.06, cell="blueprint_blue", bevel=0.0),
    F.plate("GLOW_Grid", S * 0.44, S * 0.44, cell="e_hologram", z=S * 0.07),
], n))
simple("item_beacon_part", lambda n: F.join([
    F.cone(n + "_shell", r_bottom=S * 0.34, r_top=S * 0.12, h=S * 0.8, cell="galvanized", seg=8),
    F.plate("GLOW_Seam", S * 0.5, S * 0.08, cell="e_hologram", z=S * 0.4),
], n))

# --- Military ---------------------------------------------------------------
simple("item_magazine", lambda n: F.box(n, S * 0.3, S * 0.5, S * 0.22, cell="gunmetal", bevel=0.010))
simple("item_gun", lambda n: F.join([
    F.box(n + "_body", S * 0.25, S * 0.8, S * 0.22, cell="gunmetal", bevel=0.012),
    F.box(n + "_grip", S * 0.16, S * 0.18, S * 0.28, cell="bark", bevel=0.010, y=S * 0.25, z=-S * 0.2),
], n))
simple("item_charge", lambda n: F.join([
    F.cylinder(n + "_can", r=S * 0.26, h=S * 0.46, cell="signal_red", seg=8),
    F.cylinder(n + "_fuse", r=S * 0.05, h=S * 0.22, cell="hazard_yellow", seg=4, z=S * 0.46),
], n))

# --- The five Sparks: a silhouette ladder -----------------------------------
simple("item_spark_salvage", lambda n: F.join([  # raw shard cluster
    F.rock(n + "_a", S * 0.30, cell="dust_ochre", seed=2),
    F.rock(n + "_b", S * 0.22, cell="clay", x=S * 0.24, y=S * 0.16, seed=5),
    F.plate("GLOW_Core", S * 0.22, S * 0.22, cell="e_ember", z=S * 0.34),
], n))
simple("item_spark_forge", lambda n: F.join([  # riveted canister
    F.cylinder(n + "_can", r=S * 0.26, h=S * 0.62, cell="cast_iron", seg=8),
    F.cylinder(n + "_band", r=S * 0.28, h=S * 0.06, cell="rust", seg=8, z=S * 0.30),
    F.plate("GLOW_Core", S * 0.28, S * 0.10, cell="e_alert", z=S * 0.64),
], n))
simple("item_spark_volt", lambda n: F.join([  # coil-wrapped
    F.cylinder(n + "_glass", r=S * 0.24, h=S * 0.64, cell="steel_blue", seg=8),
    F.cylinder(n + "_coil", r=S * 0.28, h=S * 0.08, cell="copper", seg=8, z=S * 0.24),
    F.plate("GLOW_Core", S * 0.26, S * 0.26, cell="e_science_blue", z=S * 0.66),
], n))
simple("item_spark_synth", lambda n: F.join([  # fluid vial
    F.cylinder(n + "_vial", r=S * 0.22, h=S * 0.70, cell="limestone", seg=8),
    F.cone(n + "_neck", r_bottom=S * 0.22, r_top=S * 0.10, h=S * 0.16, cell="galvanized", seg=6, z=S * 0.70),
    F.plate("GLOW_Core", S * 0.30, S * 0.34, cell="e_science_green", z=S * 0.34),
], n))
simple("item_spark_core", lambda n: F.join([  # open cage around a glowing core
    *[F.box(n + f"_bar{i}", S * 0.05, S * 0.05, S * 0.66, cell="gunmetal", bevel=0.0,
            x=S * 0.24 * (1 if i in (0, 3) else -1),
            y=S * 0.24 * (1 if i in (0, 1) else -1)) for i in range(4)],
    F.box(n + "_ring", S * 0.56, S * 0.56, S * 0.06, cell="brass", bevel=0.0, z=S * 0.66),
    F.plate("GLOW_Core", S * 0.34, S * 0.34, cell="e_uranium", z=S * 0.34),
], n), budget=110)
