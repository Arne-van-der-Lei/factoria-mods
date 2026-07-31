"""Ichor and synthetics — ducts, tanks, the Still, the Vat, the Corespinner,
the Seep Pump, plus bins, the Rover and the misc props.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402

F.reset()
F.export(F.join([
    F.pipe_segment("duct_run", r=0.22, length=1.0, cell="cast_iron", z=0.24, axis="Y"),
    F.cylinder("duct_flangeA", r=0.26, h=0.06, cell="gunmetal", seg=8, y=-0.47, z=0.24),
    F.cylinder("duct_flangeB", r=0.26, h=0.06, cell="gunmetal", seg=8, y=0.47, z=0.24),
], "duct"), "duct", budget=200)

F.reset()
F.export(F.join([
    F.box("ductu_hood", 0.9, 0.5, 0.44, cell="machine_shadow", bevel=0.03, z=0.02),
    F.pipe_segment("ductu_stub", r=0.20, length=0.5, cell="cast_iron", y=-0.4, z=0.24, axis="Y"),
], "duct_under"), "duct_under", budget=200)

F.reset()
tank = F.join([
    F.cylinder("tank_body", r=1.32, h=2.1, cell="steel_mid", seg=16, z=0.16),
    F.box("tank_base", 2.9, 2.9, 0.16, cell="cast_iron", bevel=0.03),
    F.cylinder("tank_lid", r=1.36, h=0.12, cell="galvanized", seg=16, z=2.26),
    F.pipe_segment("tank_portA", r=0.18, length=0.6, cell="copper_patina", x=1.4, z=0.5, axis="X"),
], "holding_tank")
F.parent(F.plate("GLOW_Gauge", 0.16, 1.4, cell="e_science_green", y=-1.33, z=1.2), tank)
F.export(tank, "holding_tank", budget=1500)

F.reset()
F.export(F.join([
    F.box("fpump_body", 0.8, 1.7, 0.7, cell="gunmetal", bevel=0.03, z=0.1),
    F.box("fpump_base", 0.95, 1.9, 0.12, cell="cast_iron", bevel=0.02),
    F.pipe_segment("fpump_in", r=0.18, length=0.5, cell="cast_iron", y=-0.95, z=0.42, axis="Y"),
    F.pipe_segment("fpump_out", r=0.18, length=0.5, cell="cast_iron", y=0.95, z=0.42, axis="Y"),
    F.cylinder("fpump_motor", r=0.24, h=0.4, cell="copper", seg=10, z=0.8),
], "flow_pump"), "flow_pump", budget=500)

F.reset()
F.export(F.join([
    F.box("spump_deck", 0.9, 1.9, 0.3, cell="cast_iron", bevel=0.03),
    F.box("spump_housing", 0.7, 0.7, 0.7, cell="steel_mid", bevel=0.03, y=0.5, z=0.3),
    F.pipe_segment("spump_snorkel", r=0.16, length=1.1, cell="copper_patina", y=-0.5, z=0.2, axis="Y"),
], "shore_pump"), "shore_pump", budget=400)

F.reset()
seep = F.join([
    F.box("seep_pad", 2.9, 2.9, 0.22, cell="cast_iron", bevel=0.03),
    F.box("seep_frame", 0.9, 1.6, 2.3, cell="rust", bevel=0.04, z=0.22),
    F.box("seep_tank", 1.1, 1.1, 0.8, cell="steel_mid", bevel=0.03, x=0.9, y=-0.8, z=0.22),
], "seep_pump")
head = F.join([
    F.box("seep_beam", 0.35, 2.2, 0.30, cell="gunmetal", bevel=0.02),
    F.box("seep_weight", 0.5, 0.5, 0.4, cell="basalt", bevel=0.02, y=0.9),
], "ANIM_Head")
head.location = (0.0, 0.0, 2.4)
F.parent(head, seep)
F.export(seep, "seep_pump", budget=1500)

F.reset()
still = F.join([
    F.box("still_pad", 4.9, 4.9, 0.25, cell="basalt", bevel=0.04),
    F.box("still_body", 3.0, 3.0, 1.6, cell="steel_mid", bevel=0.05, z=0.25),
    F.cylinder("still_columnA", r=0.55, h=3.4, cell="galvanized", seg=12, x=-1.0, y=0.8, z=1.85),
    F.cylinder("still_columnB", r=0.45, h=2.6, cell="rust", seg=12, x=1.1, y=-0.6, z=1.85),
    F.pipe_segment("still_cross", r=0.14, length=2.2, cell="copper_patina", z=3.6, axis="X"),
], "ichor_still")
F.parent(F.plate("GLOW_Window", 0.5, 0.9, cell="e_science_green", y=-1.52, z=0.9), still)
F.export(still, "ichor_still", budget=3000)

F.reset()
vat = F.join([
    F.box("vat_pad", 2.9, 2.9, 0.22, cell="cast_iron", bevel=0.03),
    F.cylinder("vat_drum", r=1.05, h=1.5, cell="steel_mid", seg=14, z=0.22),
    F.cylinder("vat_lid", r=1.12, h=0.14, cell="galvanized", seg=14, z=1.72),
    F.pipe_segment("vat_inlet", r=0.16, length=1.1, cell="copper_patina", x=1.2, z=1.0, axis="X"),
], "synth_vat")
F.parent(F.plate("GLOW_Vat", 1.6, 1.6, cell="e_science_green", z=1.88), vat)
F.export(vat, "synth_vat", budget=1500)

F.reset()
spin = F.join([
    F.box("spin_pad", 2.9, 2.9, 0.25, cell="basalt", bevel=0.03),
    F.box("spin_housing", 2.1, 2.1, 1.7, cell="galvanized", bevel=0.05, z=0.25),
    F.box("spin_cap", 1.6, 1.6, 0.2, cell="gunmetal", bevel=0.03, z=1.95),
], "corespinner")
rotor = F.cylinder("ANIM_Spin", r=0.72, h=0.5, cell="steel_light", seg=14)
rotor.location = (0.0, 0.0, 2.15)
F.parent(rotor, spin)
F.parent(F.plate("GLOW_Window", 0.6, 0.16, cell="e_uranium", y=-1.06, z=1.0), spin)
F.export(spin, "corespinner", budget=1500)

# --- Bins --------------------------------------------------------------------
for bname, cell, lid in (("coilwood_bin", "timber", "bark"),
                         ("ferrite_bin", "cast_iron", "gunmetal"),
                         ("steel_bin", "steel_mid", "galvanized")):
    F.reset()
    F.export(F.join([
        F.box(bname + "_body", 0.88, 0.88, 0.72, cell=cell, bevel=0.03),
        F.box(bname + "_lid", 0.92, 0.92, 0.10, cell=lid, bevel=0.02, z=0.72),
    ], bname), bname, budget=200)

# --- Rover: cobbled-from-parts charm, one headlight ---------------------------
F.reset()
rover = F.join([
    F.box("rover_chassis", 1.75, 2.8, 0.45, cell="rust", bevel=0.04, z=0.32),
    F.box("rover_cab", 1.35, 1.2, 0.55, cell="steel_mid", bevel=0.04, y=0.35, z=0.77),
    F.box("rover_bar", 1.6, 0.14, 0.22, cell="gunmetal", bevel=0.02, y=-1.42, z=0.55),
    F.cylinder("rover_stack", r=0.10, h=0.5, cell="cast_iron", seg=6, x=0.6, y=0.9, z=1.32),
], "rover")
for i in range(4):
    w = F.cylinder(f"ANIM_Wheel{i}", r=0.36, h=0.24, cell="hazard_black", seg=10)
    w.location = (0.88 * (1 if i % 2 else -1), 0.95 * (1 if i < 2 else -1), 0.36)
    w.rotation_euler = (0, 1.5708, 0)
    F.parent(w, rover)
trunk = F.box("ANIM_Trunk", 1.3, 0.9, 0.10, cell="galvanized", bevel=0.02)
trunk.location = (0.0, -0.55, 0.77)
F.parent(trunk, rover)
F.parent(F.plate("GLOW_Headlight", 0.22, 0.14, cell="e_lamp", x=-0.4, y=-1.44, z=0.62), rover)
F.export(rover, "rover", budget=1500)

# --- Misc props ---------------------------------------------------------------
F.reset()
F.export(F.join([
    F.box("tablet_body", 0.30, 0.22, 0.02, cell="ui_slate", bevel=0.004),
    F.plate("GLOW_Screen", 0.26, 0.18, cell="e_hologram", z=0.021),
], "tablet"), "tablet", budget=100)

F.reset()
F.export(F.join([
    F.cylinder("wand_grip", r=0.03, h=0.16, cell="bark", seg=6),
    F.cylinder("wand_shaft", r=0.018, h=0.34, cell="gunmetal", seg=6, z=0.16),
    F.plate("GLOW_Tip", 0.05, 0.05, cell="e_hologram", z=0.50),
], "builder_wand"), "builder_wand", budget=100)
