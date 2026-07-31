"""Power — verticality. Poles, stacks and chimneys are the skyline; structures
taper upward and vent from the top so they read against the sky.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402

# --- Cinderbox: boiler, 2x3, firebox glow at the front -----------------------
F.reset()
box_ = F.join([
    F.box("cinderbox_hull", 1.85, 2.85, 1.25, cell="cast_iron", bevel=0.045),
    F.box("cinderbox_pad", 2.0, 3.0, 0.14, cell="basalt", bevel=0.03),
    F.cylinder("cinderbox_drum", r=0.55, h=1.9, cell="rust", seg=14, z=1.25),
    F.cylinder("cinderbox_stack", r=0.22, h=0.9, cell="gunmetal", seg=8, y=-1.0, z=1.25),
    F.pipe_segment("cinderbox_feed", r=0.14, length=0.7, cell="copper_patina", x=1.0, y=1.1, z=0.45, axis="X"),
], "cinderbox")
F.parent(F.plate("GLOW_Firebox", 0.72, 0.5, cell="e_furnace", y=-1.44, z=0.42), box_)
F.export(box_, "cinderbox", budget=1500)

# --- Piston Dynamo / Vane Dynamo: 2x4, flywheel is the animated read ---------
def dynamo(name, cell_body, cell_wheel, glow, wheel_r):
    body = F.join([
        F.box(name + "_bed", 1.9, 3.9, 0.55, cell="cast_iron", bevel=0.04),
        F.box(name + "_block", 1.5, 2.6, 0.95, cell=cell_body, bevel=0.045, z=0.55),
        F.pipe_segment(name + "_rod", r=0.11, length=1.6, cell="galvanized", y=-0.2, z=1.05, axis="Y"),
        F.box(name + "_head", 1.1, 0.7, 0.7, cell="gunmetal", bevel=0.03, y=-1.55, z=0.55),
    ], name)
    wheel = F.join([
        F.cylinder(name + "_wheel", r=wheel_r, h=0.14, cell=cell_wheel, seg=16),
        F.box(name + "_sp0", wheel_r * 1.9, 0.07, 0.06, cell="gunmetal", bevel=0.0, z=0.07),
        F.box(name + "_sp1", 0.07, wheel_r * 1.9, 0.06, cell="gunmetal", bevel=0.0, z=0.07),
    ], "ANIM_Flywheel")
    wheel.location = (0.0, 1.45, 1.05)
    wheel.rotation_euler = (0.0, 1.5708, 0.0)
    F.parent(wheel, body)
    F.parent(F.plate("GLOW_Gauge", 0.22, 0.08, cell=glow, x=0.78, y=0.4, z=1.2), body)
    return body


F.reset()
F.export(dynamo("piston_dynamo", "steel_mid", "copper", "e_ember", 0.72), "piston_dynamo", budget=1500)
F.reset()
F.export(dynamo("vane_dynamo", "galvanized", "brass", "e_science_blue", 0.92), "vane_dynamo", budget=1500)

# --- Corium Pile: 5x5 landmark, width > height, radial cooling fins ----------
F.reset()
pile = F.join([
    F.box("pile_slab", 4.9, 4.9, 0.35, cell="weathered_stone", bevel=0.04),
    F.box("pile_jacket", 3.9, 3.9, 2.1, cell="cast_iron", bevel=0.06, z=0.35),
    F.cylinder("pile_core", r=1.45, h=2.5, cell="gunmetal", seg=18, z=0.35),
    F.cylinder("pile_cap", r=1.65, h=0.28, cell="galvanized", seg=18, z=2.85),
], "corium_pile")
for i in range(8):
    ang = i * 0.7854
    import math as _m
    fin = F.box(f"pile_fin{i}", 0.16, 1.5, 1.7, cell="steel_mid", bevel=0.02,
                x=_m.cos(ang) * 2.1, y=_m.sin(ang) * 2.1, z=0.35)
    fin.rotation_euler = (0, 0, ang)
    F.join([pile, fin], "corium_pile")
F.parent(F.cylinder("GLOW_Core", r=1.5, h=0.06, cell="e_uranium", seg=18, z=2.86), pile)
for i in range(4):
    F.parent(F.plate(f"GLOW_Seam{i}", 0.10, 1.4, cell="e_uranium",
                     x=(1.98 if i < 2 else -1.98), y=(1.0 if i % 2 else -1.0), z=1.3), pile)
F.export(pile, "corium_pile", budget=3000)

# --- Dawncatcher / Nightcell -------------------------------------------------
F.reset()
sun = F.join([
    F.box("dawn_frame", 2.85, 2.85, 0.16, cell="gunmetal", bevel=0.03),
    F.box("dawn_panel", 2.55, 2.55, 0.09, cell="steel_blue", bevel=0.02, z=0.16),
    *[F.box(f"dawn_leg{i}", 0.12, 0.12, 0.30, cell="cast_iron", bevel=0.01,
            x=1.2 * (1 if i in (0, 3) else -1), y=1.2 * (1 if i in (0, 1) else -1)) for i in range(4)],
], "dawncatcher")
F.parent(F.plate("GLOW_Cells", 2.3, 2.3, cell="e_science_blue", z=0.26), sun)
F.export(sun, "dawncatcher", budget=800)

F.reset()
night = F.join([
    F.box("night_case", 1.85, 1.85, 1.15, cell="steel_mid", bevel=0.04),
    F.box("night_base", 1.95, 1.95, 0.14, cell="cast_iron", bevel=0.03),
    F.box("night_lid", 1.5, 1.5, 0.14, cell="gunmetal", bevel=0.02, z=1.15),
], "nightcell")
for i in range(3):
    F.parent(F.plate(f"GLOW_Charge{i}", 0.5, 0.07, cell="e_lamp", y=-0.93, z=0.35 + i * 0.25), night)
F.export(night, "nightcell", budget=800)

# --- Pylons: the skyline -----------------------------------------------------
F.reset()
stub = F.join([
    F.box("stub_base", 0.45, 0.45, 0.14, cell="cast_iron", bevel=0.02),
    F.box("stub_post", 0.16, 0.16, 2.3, cell="timber", bevel=0.02, z=0.14),
    F.box("stub_arm", 1.0, 0.10, 0.08, cell="timber", bevel=0.01, z=2.28),
    *[F.cylinder(f"stub_ins{i}", r=0.05, h=0.12, cell="copper_patina", seg=6,
                 x=-0.42 + i * 0.84, z=2.36) for i in range(2)],
], "stub_pylon")
F.export(stub, "stub_pylon", budget=300)

F.reset()
pylon = F.join([
    F.box("pylon_base", 0.6, 0.6, 0.16, cell="cast_iron", bevel=0.02),
    F.truss("pylon_mast", 0.42, 3.4, cell="gunmetal", bars=4, thickness=0.07, z=0.16),
    F.box("pylon_arm", 1.5, 0.10, 0.09, cell="gunmetal", bevel=0.01, z=3.5),
    *[F.cylinder(f"pylon_ins{i}", r=0.05, h=0.14, cell="copper_patina", seg=6,
                 x=-0.65 + i * 0.65, z=3.6) for i in range(3)],
], "pylon")
F.export(pylon, "pylon", budget=800)

F.reset()
high = F.join([
    F.box("high_base", 1.85, 1.85, 0.20, cell="cast_iron", bevel=0.03),
    F.truss("high_mast", 1.1, 6.2, cell="steel_mid", bars=6, thickness=0.10, z=0.20),
    F.box("high_arm0", 2.6, 0.12, 0.11, cell="steel_mid", bevel=0.01, z=5.2),
    F.box("high_arm1", 2.6, 0.12, 0.11, cell="steel_mid", bevel=0.01, z=6.2),
], "high_pylon")
F.parent(F.plate("GLOW_Beacon", 0.14, 0.14, cell="e_alert", z=6.42), high)
F.export(high, "high_pylon", budget=1500)

F.reset()
node = F.join([
    F.box("grid_base", 1.9, 1.9, 0.22, cell="cast_iron", bevel=0.03),
    F.box("grid_body", 1.4, 1.4, 1.5, cell="steel_mid", bevel=0.04, z=0.22),
    F.cylinder("grid_coil", r=0.5, h=0.9, cell="copper", seg=14, z=1.72),
    F.box("grid_cap", 1.1, 1.1, 0.14, cell="galvanized", bevel=0.02, z=2.62),
], "gridnode")
F.parent(F.plate("GLOW_Arc", 0.9, 0.9, cell="e_science_blue", z=2.78), node)
F.export(node, "gridnode", budget=800)

# --- Lamp: the machine that makes night worth having -------------------------
F.reset()
lamp = F.join([
    F.box("lamp_base", 0.42, 0.42, 0.10, cell="cast_iron", bevel=0.02),
    F.box("lamp_post", 0.10, 0.10, 1.5, cell="gunmetal", bevel=0.01, z=0.10),
    F.cone("lamp_shade", r_bottom=0.34, r_top=0.14, h=0.26, cell="galvanized", seg=10, z=1.60),
], "lamp")
F.parent(F.plate("GLOW_Bulb", 0.30, 0.30, cell="e_lamp", z=1.58), lamp)
F.export(lamp, "lamp", budget=300)
