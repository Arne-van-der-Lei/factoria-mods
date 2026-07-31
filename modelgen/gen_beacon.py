"""The World-Beacon — the one megastructure. Nothing else may compete in height.

Built in three visible stages as materials arrive (STAGE_ sub-roots the engine
enables in order). Clamshell doors, a leaning gantry, and GLOW_BeamColumn: the
shader quad that becomes the column of dawn light at Ignition.

Memorable detail: one terrace step is newer and patched — someone tried before you.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402

F.reset()

# Root is the crater ring foundation everything hangs off.
root = F.box("beacon_frame", 8.8, 8.8, 0.30, cell="basalt", bevel=0.05)

# --- STAGE 1: stepped octagonal crater ring ---------------------------------
foundation_parts = []
for i in range(8):
    ang = i * math.pi / 4.0
    # one step is visibly newer: patched by whoever came before
    cell = "limestone" if i == 5 else "weathered_stone"
    seg = F.box(f"beacon_step{i}", 3.2, 1.5, 0.9, cell=cell, bevel=0.05,
                x=math.cos(ang) * 3.3, y=math.sin(ang) * 3.3, z=0.30)
    seg.rotation_euler = (0, 0, ang)
    foundation_parts.append(seg)
foundation_parts.append(F.box("beacon_pit", 4.6, 4.6, 0.25, cell="machine_shadow", bevel=0.04, z=0.30))
stage1 = F.join(foundation_parts, "STAGE_Foundation")
F.parent(stage1, root)

# --- STAGE 2: the spire structure -------------------------------------------
stage2 = F.join([
    F.cylinder("beacon_drum", r=2.2, h=2.6, cell="cast_iron", seg=16, z=0.55),
    F.cone("beacon_taperA", r_bottom=2.1, r_top=1.5, h=3.2, cell="steel_mid", seg=12, z=3.15),
    F.cone("beacon_taperB", r_bottom=1.5, r_top=0.9, h=3.4, cell="galvanized", seg=12, z=6.35),
    F.cone("beacon_crown", r_bottom=0.9, r_top=0.35, h=2.4, cell="copper", seg=10, z=9.75),
    *[F.box(f"beacon_rib{i}", 0.22, 0.22, 5.6, cell="rust", bevel=0.02,
            x=math.cos(i * math.pi / 2) * 2.0, y=math.sin(i * math.pi / 2) * 2.0, z=0.55)
      for i in range(4)],
], "STAGE_Structure")
F.parent(stage2, root)

# --- STAGE 3: gantry + doors -------------------------------------------------
gantry_mast = F.truss("beacon_gantry_mast", 1.3, 9.5, cell="gunmetal", bars=8, thickness=0.14)
gantry_arm = F.box("beacon_gantry_arm", 2.6, 0.5, 0.35, cell="gunmetal", bevel=0.03, x=1.3, z=8.6)
gantry = F.join([gantry_mast, gantry_arm], "ANIM_Gantry")
gantry.location = (3.4, 0.0, 0.55)
gantry.rotation_euler = (0.0, -0.10, 0.0)  # leaning, mid-retraction
F.parent(gantry, root)

for side, sgn in (("L", -1), ("R", 1)):
    door = F.join([
        F.box(f"beacon_door{side}", 4.0, 2.1, 0.30, cell="galvanized", bevel=0.04),
        F.box(f"beacon_doorrib{side}", 4.0, 0.22, 0.14, cell="hazard_yellow", bevel=0.02, z=0.30),
    ], f"ANIM_Door{side}")
    door.location = (0.0, sgn * 2.4, 0.62)  # pivot at the outer hinge
    F.parent(door, root)

# --- Emissives ---------------------------------------------------------------
F.parent(F.plate("GLOW_Ring", 5.2, 5.2, cell="e_hologram", z=0.58), root)
F.parent(F.plate("GLOW_Crown", 0.8, 0.8, cell="e_lamp", z=12.16), root)
# the ignition column: a tall quad the shader drives from dark to dawn-light
column = F.box("GLOW_BeamColumn", 1.6, 1.6, 40.0, cell="e_lamp", bevel=0.0)
column.location = (0.0, 0.0, 0.6)
F.parent(column, root)

F.export(root, "beacon_frame", budget=8000)
