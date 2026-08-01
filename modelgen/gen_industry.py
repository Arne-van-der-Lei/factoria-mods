"""The walled yards: industry the Lattice ran, and the garrisons that watched it.

Compounds are the map's answer to "why would I walk over there". An industrial
yard is where the ore still is -- the Lattice built its plants straight onto the
deposits, so the richest easy ore on the map is inside somebody's fence. A
garrison is where the Wardens still are. Both are worth the walk; only one wants
you there, and the player needs to tell which is which from a long way off.

Design rules, from the art bible:
  * Silhouette does the telling. Industry is vertical and round -- stacks, silos,
    tanks. Military is low, wide and angular -- 45 degree wedges, nothing taller
    than it needs to be. You should be able to read a compound as a shape on the
    horizon before any texture resolves.
  * Chrome (steel_light) is reserved for Warden hardware. Industrial metal is
    rust, cast iron and galvanized; the garrison gets the cold stuff.
  * Everything is stopped. No smoke, no lights, no movement -- the one exception
    is the garrison beacon, which is still dutifully turning.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402


def rusted_panels(name, w, d, h, cell, seed, ribs=4):
    """A shed: ribbed sheet walls with one panel missing. ~90 tris."""
    parts = [F.box(name + "_shell", w, d, h, cell=cell, bevel=0.04, z=0.0)]
    for i in range(ribs):
        t = (i + 1) / (ribs + 1)
        parts.append(F.box(f"{name}_rib{i}", 0.08, d + 0.04, h * 0.92,
                           cell="gunmetal", bevel=0.0, x=(t - 0.5) * w, z=0.0))
    # The missing panel: a dark recess, so the shed reads as open, not sealed.
    parts.append(F.box(name + "_gap", w * 0.26, 0.10, h * 0.55, cell="machine_shadow",
                       bevel=0.0, x=w * 0.22, y=-d / 2, z=0.0))
    parts.append(F.rock(name + "_spill", 0.28, cell="slate",
                        x=w * 0.22, y=-d / 2 - 0.35, seed=seed))
    return F.join(parts, name)


# --- industry: vertical, round, stopped mid-shift ---------------------------

# Ore silo. The tallest thing in a yard and the reason you spotted it.
F.reset()
silo = F.join([
    F.cylinder("silo_skirt", r=1.7, h=0.5, cell="weathered_stone", seg=10),
    F.cylinder("silo_body", r=1.5, h=6.4, cell="galvanized", seg=10, z=0.5),
    F.cylinder("silo_band", r=1.56, h=0.16, cell="rust", seg=10, z=3.2),
    F.cone("silo_cap", r_bottom=1.5, r_top=0.35, h=1.1, cell="cast_iron", seg=10, z=6.9),
    # The chute that fed it, still hanging.
    F.box("silo_chute", 0.5, 0.5, 2.4, cell="rust", bevel=0.03, x=1.6, y=0.3, z=2.6),
], "yard_silo")
F.export(silo, "yard_silo", budget=900)

# Chimney stack. Cold for a very long time.
F.reset()
stack = F.join([
    F.box("stk_base", 2.6, 2.6, 0.9, cell="weathered_stone", bevel=0.04),
    F.cone("stk_shaft", r_bottom=1.05, r_top=0.6, h=9.5, cell="clay", seg=10, z=0.9),
    F.cylinder("stk_lip", r=0.68, h=0.3, cell="cast_iron", seg=10, z=10.4),
    F.box("stk_ladder", 0.10, 0.10, 8.0, cell="gunmetal", bevel=0.0, x=0.95, z=1.0),
], "yard_stack")
F.export(stack, "yard_stack", budget=900)

# Fluid tank. Squat, banded, with the ladder nobody came back down.
F.reset()
tank = F.join([
    F.cylinder("tnk_body", r=2.4, h=3.2, cell="steel_blue", seg=12),
    F.cylinder("tnk_bandA", r=2.46, h=0.14, cell="rust", seg=12, z=0.9),
    F.cylinder("tnk_bandB", r=2.46, h=0.14, cell="rust", seg=12, z=2.1),
    F.cylinder("tnk_roof", r=2.4, h=0.22, cell="galvanized", seg=12, z=3.2),
    F.box("tnk_ladder", 0.09, 0.09, 3.4, cell="gunmetal", bevel=0.0, x=2.42),
    F.box("tnk_rail", 1.6, 0.07, 0.5, cell="gunmetal", bevel=0.0, y=1.6, z=3.42),
], "yard_tank")
F.export(tank, "yard_tank", budget=800)

# Warehouse. The yard's floor plate: long, low, ribbed, gutted.
F.reset()
F.export(rusted_panels("yard_warehouse", 9.0, 6.0, 3.4, "rust", seed=3, ribs=6),
         "yard_warehouse", budget=700)

# Machine hall: same language, taller, with a monitor roof.
F.reset()
hall = F.join([
    rusted_panels("hall_shell", 7.0, 5.0, 5.0, "dust_ochre", seed=5, ribs=4),
    F.box("hall_monitor", 2.6, 5.1, 0.9, cell="cast_iron", bevel=0.03, z=5.0),
], "yard_hall")
F.export(hall, "yard_hall", budget=900)

# Gantry crane. Straight lines at height -- the single most "this was built"
# silhouette in the set, which is why the yard gets one.
F.reset()
gantry = F.join([
    F.box("gan_legA", 0.36, 0.36, 5.0, cell="hazard_yellow", bevel=0.02, x=-3.4),
    F.box("gan_legB", 0.36, 0.36, 5.0, cell="hazard_yellow", bevel=0.02, x=3.4),
    F.truss("gan_span", length=7.6, height=0.7, cell="gunmetal", bars=6, z=4.9),
    F.box("gan_trolley", 0.9, 0.8, 0.6, cell="cast_iron", bevel=0.02, x=-1.1, z=4.3),
    F.box("gan_hook", 0.14, 0.14, 1.6, cell="rust", bevel=0.0, x=-1.1, z=2.7),
], "yard_gantry")
F.export(gantry, "yard_gantry", budget=900)

# Pipe rack: the connective tissue that makes a yard look like a system.
F.reset()
rack = F.join([
    F.box("rck_postA", 0.22, 0.22, 2.6, cell="gunmetal", bevel=0.02, x=-2.2),
    F.box("rck_postB", 0.22, 0.22, 2.6, cell="gunmetal", bevel=0.02, x=2.2),
    F.box("rck_beam", 4.8, 0.20, 0.20, cell="gunmetal", bevel=0.02, z=2.5),
    F.pipe_segment("rck_pipeA", r=0.22, length=5.0, cell="copper_patina", z=2.9),
    F.pipe_segment("rck_pipeB", r=0.16, length=5.0, cell="cast_iron", y=0.5, z=2.85),
    F.pipe_segment("rck_pipeC", r=0.16, length=5.0, cell="rust", y=-0.5, z=2.85),
], "yard_piperack")
F.export(rack, "yard_piperack", budget=700)

# Conveyor bridge from the deposit to the plant -- the yard's thesis statement.
F.reset()
conveyor = F.join([
    F.box("cnv_footA", 0.6, 0.6, 0.3, cell="weathered_stone", bevel=0.02, x=-2.6),
    F.box("cnv_legA", 0.24, 0.24, 3.0, cell="rust", bevel=0.02, x=-2.6, z=0.3),
    F.box("cnv_legB", 0.24, 0.24, 4.2, cell="rust", bevel=0.02, x=2.6, z=0.3),
    F.box("cnv_belt", 6.0, 1.1, 0.5, cell="machine_shadow", bevel=0.02, z=3.4),
    F.box("cnv_hood", 6.0, 1.2, 0.35, cell="galvanized", bevel=0.02, z=3.9),
], "yard_conveyor")
F.export(conveyor, "yard_conveyor", budget=700)

# The yard fence: chain-link on concrete feet, with the panel that came down.
F.reset()
fence = F.join([
    F.box("fnc_foot", 1.0, 0.34, 0.16, cell="weathered_stone", bevel=0.02),
    F.box("fnc_postA", 0.09, 0.09, 2.0, cell="gunmetal", bevel=0.01, x=-0.45, z=0.16),
    F.box("fnc_mesh", 0.9, 0.03, 1.7, cell="machine_shadow", bevel=0.0, z=0.30),
    F.box("fnc_top", 0.95, 0.05, 0.05, cell="rust", bevel=0.0, z=2.05),
], "yard_fence")
F.export(fence, "yard_fence", budget=150)

F.reset()
gate = F.join([
    F.box("gt_pierA", 0.34, 0.34, 2.4, cell="weathered_stone", bevel=0.03, x=-1.4),
    F.box("gt_pierB", 0.34, 0.34, 2.4, cell="weathered_stone", bevel=0.03, x=1.4),
    F.box("gt_lintel", 3.2, 0.28, 0.34, cell="cast_iron", bevel=0.02, z=2.4),
    # One leaf swung open and rusted that way. A closed gate is a wall; an open
    # one is an invitation, and the yards are meant to be entered.
    F.box("gt_leaf", 0.06, 1.2, 1.9, cell="rust", bevel=0.02, x=-1.3, y=0.65, z=0.1),
], "yard_gate")
F.parent(F.plate("GLOW_Sign", 0.7, 0.3, cell="e_ember", z=2.62), gate)
F.export(gate, "yard_gate", budget=400)


# --- military: low, wide, angular, still switched on ------------------------

def wedge(name, w, d, h, cell, cut=0.35):
    """A block with its top edges pulled in -- reads as armour, not architecture."""
    obj = F.box(name, w, d, h, cell=cell, bevel=0.02)
    for v in obj.data.vertices:
        if v.co.z > h * 0.5:
            v.co.x *= (1.0 - cut)
            v.co.y *= (1.0 - cut)
    return obj


# Bunker. The lowest thing in the set on purpose: it is trying not to be hit.
F.reset()
bunker = F.join([
    wedge("bnk_body", 5.6, 4.4, 2.2, "weathered_stone", cut=0.28),
    F.box("bnk_slit", 3.0, 0.16, 0.34, cell="machine_shadow", bevel=0.0, y=-2.2, z=1.3),
    F.box("bnk_hood", 3.4, 0.5, 0.24, cell="granite", bevel=0.02, y=-2.3, z=1.7),
    F.box("bnk_hatch", 1.0, 1.0, 0.22, cell="gunmetal", bevel=0.02, x=1.6, y=1.2, z=2.2),
], "garrison_bunker")
F.export(bunker, "garrison_bunker", budget=600)

# Watchtower: the one vertical the garrison allows itself, and it is all sensor.
F.reset()
tower = F.join([
    F.box("wt_legA", 0.26, 0.26, 6.0, cell="gunmetal", bevel=0.02, x=-1.0, y=-1.0),
    F.box("wt_legB", 0.26, 0.26, 6.0, cell="gunmetal", bevel=0.02, x=1.0, y=-1.0),
    F.box("wt_legC", 0.26, 0.26, 6.0, cell="gunmetal", bevel=0.02, x=-1.0, y=1.0),
    F.box("wt_legD", 0.26, 0.26, 6.0, cell="gunmetal", bevel=0.02, x=1.0, y=1.0),
    F.box("wt_brace", 2.4, 2.4, 0.14, cell="cast_iron", bevel=0.01, z=3.0),
    F.box("wt_deck", 3.2, 3.2, 0.18, cell="cast_iron", bevel=0.02, z=6.0),
    F.box("wt_cab", 2.4, 2.4, 1.6, cell="steel_light", bevel=0.04, z=6.18),
    F.box("wt_visor", 2.5, 0.12, 0.5, cell="machine_shadow", bevel=0.0, y=-1.2, z=6.9),
], "garrison_tower")
F.parent(F.plate("GLOW_Eye", 0.5, 0.18, cell="e_alert", z=7.05), tower)
F.export(tower, "garrison_tower", budget=900)

# Barricade: the 45 degree wedge the whole military family is built from.
F.reset()
barricade = F.join([
    wedge("bar_block", 1.8, 0.9, 1.1, "granite", cut=0.45),
    F.box("bar_stripe", 1.6, 0.06, 0.22, cell="hazard_yellow", bevel=0.0, y=-0.45, z=0.5),
    F.box("bar_stripe2", 1.6, 0.06, 0.22, cell="hazard_black", bevel=0.0, y=-0.45, z=0.14),
], "garrison_barricade")
F.export(barricade, "garrison_barricade", budget=200)

# Hangar: where the Wardens were serviced. Big enough to walk a Goliath into.
F.reset()
hangar = F.join([
    F.box("hgr_shell", 11.0, 8.0, 4.6, cell="steel_blue", bevel=0.05),
    F.box("hgr_roof", 11.2, 8.2, 0.5, cell="gunmetal", bevel=0.03, z=4.6),
    F.box("hgr_mouth", 5.4, 0.3, 3.6, cell="machine_shadow", bevel=0.0, y=-4.0),
    F.box("hgr_doorA", 2.8, 0.22, 3.8, cell="steel_light", bevel=0.02, x=-3.6, y=-4.05),
    F.box("hgr_doorB", 2.8, 0.22, 3.8, cell="steel_light", bevel=0.02, x=3.6, y=-4.05),
    F.box("hgr_railL", 11.0, 0.16, 0.12, cell="cast_iron", bevel=0.0, y=-4.15),
], "garrison_hangar")
F.parent(F.plate("GLOW_Bay", 4.8, 0.9, cell="e_alert", y=-3.9, z=0.05), hangar)
F.export(hangar, "garrison_hangar", budget=1100)

# Muster mast: the garrison's one still-working piece of kit. It is what calls
# the Wardens when the player starts taking the yard apart.
F.reset()
mast = F.join([
    F.box("mst_pad", 2.2, 2.2, 0.30, cell="weathered_stone", bevel=0.03),
    F.cylinder("mst_column", r=0.30, h=5.4, cell="steel_light", seg=8, z=0.30),
    F.box("mst_vaneA", 1.5, 0.10, 0.34, cell="gunmetal", bevel=0.01, z=5.0),
    F.box("mst_vaneB", 0.10, 1.5, 0.34, cell="gunmetal", bevel=0.01, z=5.4),
    F.cone("mst_head", r_bottom=0.44, r_top=0.14, h=0.7, cell="cast_iron", seg=8, z=5.7),
], "garrison_mast")
F.parent(F.plate("ANIM_Sweep", 1.2, 0.2, cell="e_alert", z=5.2), mast)
F.parent(F.plate("GLOW_Beacon", 0.26, 0.26, cell="e_alert", z=6.42), mast)
F.export(mast, "garrison_mast", budget=700)

# Ammunition bunker: half buried, blast wall in front, the only red in the yard.
F.reset()
magazine = F.join([
    F.box("mag_berm", 6.0, 4.6, 1.4, cell="dry_earth", bevel=0.06),
    wedge("mag_shell", 4.2, 3.2, 1.9, "weathered_stone", cut=0.22),
    F.box("mag_blast", 5.2, 0.4, 2.2, cell="granite", bevel=0.03, y=-2.6),
    F.box("mag_door", 1.4, 0.18, 1.5, cell="signal_red", bevel=0.02, y=-1.7, z=0.05),
], "garrison_magazine")
F.export(magazine, "garrison_magazine", budget=600)
