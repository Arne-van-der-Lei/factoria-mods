"""Wardens and the defenses raised against them.

Wardens are sleek lens-eyed chrome custodians â€” geometric, never organic; menacing
the way a guard dog guarding an empty house is menacing. Chrome (galvanized) is
reserved as the Warden faction color. Legs and mandibles carry vertex-colour weight
for the wiggle shader; alert-red eyes fade to hologram cyan after the Ignition.

Defenses are angular and low: 45-degree chamfers, wedge profiles, barrels the longest line.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402


def warden(name, scale, plate_cell, budget):
    s = scale
    body = F.join([
        F.box(name + "_thorax", 0.62 * s, 0.86 * s, 0.34 * s, cell=plate_cell, bevel=0.02 * s, z=0.30 * s),
        F.box(name + "_carapace", 0.52 * s, 0.62 * s, 0.20 * s, cell="galvanized", bevel=0.02 * s, z=0.62 * s),
        F.box(name + "_head", 0.40 * s, 0.34 * s, 0.26 * s, cell="galvanized", bevel=0.02 * s, y=-0.58 * s, z=0.34 * s),
    ], name)

    for i in range(6):
        side = -1 if i < 3 else 1
        yy = (-0.30 + (i % 3) * 0.30) * s
        leg = F.join([
            F.box(f"{name}_thigh{i}", 0.07 * s, 0.07 * s, 0.34 * s, cell="chitin_dark", bevel=0.01 * s),
            F.box(f"{name}_shin{i}", 0.05 * s, 0.05 * s, 0.30 * s, cell="chitin_dark", bevel=0.01 * s,
                  x=side * 0.12 * s, z=-0.28 * s),
        ], f"ANIM_Leg{i}")
        leg.location = (side * 0.30 * s, yy, 0.30 * s)
        leg.rotation_euler = (0, side * 0.5, 0)
        F.parent(leg, body)

    for side, sgn in (("L", -1), ("R", 1)):
        mand = F.join([
            F.cone(f"{name}_mand{side}", r_bottom=0.07 * s, r_top=0.015 * s, h=0.34 * s,
                   cell="fang_bone", seg=6),
        ], f"ANIM_Mandible{side}")
        mand.location = (sgn * 0.13 * s, -0.72 * s, 0.32 * s)
        mand.rotation_euler = (1.35, 0, sgn * 0.25)
        F.parent(mand, body)

    F.parent(F.plate("GLOW_Eyes", 0.26 * s, 0.06 * s, cell="e_alert",
                     y=-0.71 * s, z=0.42 * s), body)
    return body


F.reset()
F.export(warden("warden_scarab", 0.6 / 0.6, "hide", 300), "warden_scarab", budget=820)
F.reset()
F.export(warden("warden_lancer", 1.0 / 0.6, "hide_dark", 450), "warden_lancer", budget=820)
F.reset()
F.export(warden("warden_goliath", 1.6 / 0.6, "chitin_dark", 800), "warden_goliath", budget=820)

# --- Warden Node: 5x5 custodial architecture, geometric hive -----------------
F.reset()
node = F.join([
    F.box("node_apron", 4.9, 4.9, 0.28, cell="basalt", bevel=0.04),
    F.box("node_drum", 3.2, 3.2, 1.5, cell="spawner_flesh", bevel=0.06, z=0.28),
    F.cone("node_spire", r_bottom=1.7, r_top=0.5, h=2.2, cell="chitin_dark", seg=8, z=1.78),
], "warden_node")
for i in range(4):
    ang = i * 1.5708 + 0.7854
    buttress = F.box(f"node_buttress{i}", 0.36, 1.5, 1.9, cell="hide_dark", bevel=0.03,
                     x=math.cos(ang) * 1.9, y=math.sin(ang) * 1.9, z=0.28)
    buttress.rotation_euler = (0, 0, ang)
    F.join([node, buttress], "warden_node")
for i in range(3):
    F.parent(F.plate(f"GLOW_Vent{i}", 0.5, 0.10, cell="e_alert",
                     y=-1.63, z=0.6 + i * 0.35), node)
F.parent(F.cone("GLOW_Crown", r_bottom=0.52, r_top=0.12, h=0.30, cell="e_alert", seg=8, z=3.98), node)
F.export(node, "warden_node", budget=3000)

# --- Sentry / Beam Sentry: trapezoid base, articulated head, long barrel -----
def sentry(name, barrel_cell, glow, beam):
    base = F.join([
        F.box(name + "_pad", 1.85, 1.85, 0.22, cell="cast_iron", bevel=0.03),
        F.cone(name + "_wedge", r_bottom=0.85, r_top=0.55, h=0.55, cell="steel_mid", seg=8, z=0.22),
        *[F.box(f"{name}_chevron{i}", 0.5, 0.09, 0.05, cell="hazard_yellow", bevel=0.0,
                x=-0.5 + i * 0.5, y=-0.88, z=0.10) for i in range(3)],
    ], name)
    head = F.join([
        F.box(name + "_head", 0.62, 0.62, 0.40, cell="gunmetal", bevel=0.03),
        F.pipe_segment(name + "_barrel", r=0.09 if not beam else 0.12, length=1.25,
                       cell=barrel_cell, y=-0.62, z=0.18, axis="Y"),
    ], "ANIM_Head")
    head.location = (0.0, 0.0, 0.77)
    F.parent(head, base)
    F.parent(F.plate("GLOW_Sight", 0.14, 0.05, cell=glow, y=-0.30, z=1.02), base)
    return base


F.reset()
F.export(sentry("sentry", "galvanized", "e_ember", False), "sentry", budget=800)
F.reset()
F.export(sentry("beam_sentry", "copper", "e_science_blue", True), "beam_sentry", budget=800)

# --- Ramparts ---------------------------------------------------------------
F.reset()
wall = F.join([
    F.box("rampart_block", 0.96, 0.96, 1.15, cell="weathered_stone", bevel=0.04),
    F.box("rampart_cap", 1.02, 1.02, 0.12, cell="granite", bevel=0.02, z=1.15),
], "rampart")
F.export(wall, "rampart", budget=300)

F.reset()
gate = F.join([
    F.box("gate_postL", 0.20, 0.96, 1.25, cell="cast_iron", bevel=0.03, x=-0.38),
    F.box("gate_postR", 0.20, 0.96, 1.25, cell="cast_iron", bevel=0.03, x=0.38),
    F.box("gate_lintel", 0.96, 0.96, 0.14, cell="granite", bevel=0.02, z=1.25),
], "rampart_gate")
for side, sgn in (("L", -1), ("R", 1)):
    leaf = F.box(f"ANIM_Leaf{side}", 0.30, 0.10, 1.05, cell="galvanized", bevel=0.02)
    leaf.location = (sgn * 0.18, 0.0, 0.05)
    F.parent(leaf, gate)
F.parent(F.plate("GLOW_Sill", 0.7, 0.06, cell="e_hologram", z=0.03), gate)
F.export(gate, "rampart_gate", budget=400)

# --- Echo Mast --------------------------------------------------------------
F.reset()
mast = F.join([
    F.box("echo_base", 2.8, 2.8, 0.28, cell="cast_iron", bevel=0.03),
    F.truss("echo_mast", 0.9, 2.6, cell="gunmetal", bars=4, thickness=0.09, z=0.28),
    F.box("echo_house", 1.0, 1.0, 0.5, cell="steel_mid", bevel=0.03, z=2.88),
], "echo_mast")
dish = F.join([
    F.cone("echo_dish", r_bottom=1.05, r_top=0.25, h=0.42, cell="galvanized", seg=14),
    F.cylinder("echo_horn", r=0.09, h=0.45, cell="copper", seg=6, z=0.42),
], "ANIM_Dish")
dish.location = (0.0, 0.0, 3.38)
dish.rotation_euler = (0.5, 0.0, 0.0)
F.parent(dish, mast)
F.parent(F.plate("GLOW_Ping", 0.16, 0.06, cell="e_hologram", y=-0.52, z=3.05), mast)
F.export(mast, "echo_mast", budget=1500)
