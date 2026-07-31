"""Rollways and Grabbers â€” the ground layer. Nothing here rises above 0.5 m,
so machine silhouettes are never blocked.

Belt surfaces are separate BELT_ children so the scrolling-UV shader can drive
them for free; item motion is instanced separately.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402

TIERS = [("rollway", "cast_iron", "rust"),
         ("swift_rollway", "gunmetal", "copper"),
         ("surge_rollway", "steel_mid", "brass")]


def frame(name, frame_cell, w=0.94, d=0.94):
    return F.join([
        F.box(name + "_bed", w, d, 0.14, cell=frame_cell, bevel=0.02),
        F.box(name + "_railL", 0.07, d, 0.10, cell="gunmetal", bevel=0.01, x=-w / 2 + 0.035, z=0.14),
        F.box(name + "_railR", 0.07, d, 0.10, cell="gunmetal", bevel=0.01, x=w / 2 - 0.035, z=0.14),
    ], name)


for tier, frame_cell, accent in TIERS:
    # straight
    F.reset()
    body = frame(tier, frame_cell)
    surf = F.plate("BELT_Surface", 0.78, 0.98, cell=accent, z=0.155)
    F.parent(surf, body)
    F.export(body, tier, budget=300)

    # underground entrance â€” a ramp mouth that reads as "goes under"
    F.reset()
    body = F.join([
        frame(tier + "_u", frame_cell),
        F.box(tier + "_hood", 0.94, 0.42, 0.34, cell="machine_shadow", bevel=0.02, y=0.28, z=0.14),
        F.box(tier + "_lip", 0.94, 0.10, 0.06, cell=accent, bevel=0.01, y=-0.42, z=0.15),
    ], tier + "_under")
    F.parent(F.plate("BELT_Surface", 0.78, 0.55, cell=accent, y=-0.2, z=0.155), body)
    F.export(body, tier + "_under", budget=300)

    # splitter â€” 2x1
    F.reset()
    body = F.join([
        F.box(tier + "_sbed", 1.94, 0.94, 0.14, cell=frame_cell, bevel=0.02),
        F.box(tier + "_shead", 1.94, 0.22, 0.26, cell="gunmetal", bevel=0.02, y=0.36, z=0.14),
        F.box(tier + "_sdiv", 0.10, 0.60, 0.20, cell=accent, bevel=0.01, z=0.14),
    ], tier + "_splitter")
    F.parent(F.plate("BELT_SurfaceL", 0.80, 0.90, cell=accent, x=-0.5, z=0.155), body)
    F.parent(F.plate("BELT_SurfaceR", 0.80, 0.90, cell=accent, x=0.5, z=0.155), body)
    F.export(body, tier + "_splitter", budget=560)


def grabber(name, arm_cell, base_cell, reach, glow):
    """Jointed arm hierarchy: ANIM_Arm0 -> ANIM_Arm1 -> ANIM_Hand, pivots at joints."""
    base = F.join([
        F.box(name + "_pad", 0.86, 0.86, 0.12, cell=base_cell, bevel=0.02),
        F.cylinder(name + "_post", r=0.16, h=0.34, cell="gunmetal", seg=10, z=0.12),
        F.box(name + "_dir", 0.10, 0.30, 0.04, cell=arm_cell, bevel=0.0, y=0.32, z=0.13),
    ], name)

    arm0 = F.join([
        F.cylinder(name + "_j0", r=0.10, h=0.14, cell="gunmetal", seg=8),
        F.box(name + "_seg0", 0.09, 0.09, 0.44 * reach, cell=arm_cell, bevel=0.01, z=0.07),
    ], "ANIM_Arm0")
    arm0.location = (0.0, 0.0, 0.46)
    F.parent(arm0, base)

    arm1 = F.join([
        F.cylinder(name + "_j1", r=0.08, h=0.12, cell="gunmetal", seg=8),
        F.box(name + "_seg1", 0.08, 0.08, 0.40 * reach, cell=arm_cell, bevel=0.01, z=0.06),
    ], "ANIM_Arm1")
    arm1.location = (0.0, 0.0, 0.44 * reach + 0.07)
    F.parent(arm1, arm0)

    hand = F.join([
        F.box(name + "_palm", 0.16, 0.10, 0.06, cell="galvanized", bevel=0.01),
        F.box(name + "_fingerL", 0.04, 0.04, 0.13, cell="galvanized", bevel=0.0, x=-0.06, z=0.06),
        F.box(name + "_fingerR", 0.04, 0.04, 0.13, cell="galvanized", bevel=0.0, x=0.06, z=0.06),
    ], "ANIM_Hand")
    hand.location = (0.0, 0.0, 0.40 * reach + 0.06)
    F.parent(hand, arm1)

    F.parent(F.plate("GLOW_Status", 0.10, 0.04, cell=glow, y=-0.40, z=0.14), base)
    return base


for gname, arm, base_c, reach, glow in [
    ("grabber_crank", "rust", "cast_iron", 1.0, "e_furnace"),
    ("grabber", "copper", "cast_iron", 1.0, "e_science_blue"),
    ("grabber_long", "copper", "cast_iron", 1.6, "e_science_blue"),
    ("grabber_swift", "brass", "gunmetal", 1.0, "e_science_green"),
    ("grabber_filter", "copper_patina", "gunmetal", 1.0, "e_hologram"),
    ("grabber_stack", "brass", "gunmetal", 1.2, "e_ember"),
]:
    F.reset()
    F.export(grabber(gname, arm, base_c, reach, glow), gname, budget=560)
