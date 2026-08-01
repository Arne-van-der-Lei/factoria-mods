"""The dead cities: roads, highways and the buildings between them.

The Lattice had towns, and the player walks through their ruins. These are the
models that make that legible on the ground rather than only on the map.

Design rules, from the art bible:
  * Straight lines are the storytelling. Nothing in nature is straight, so a kerb
    or a lane marking says "this was built" before any lore does.
  * Everything is worn: cracked slabs, missing kerb sections, subsided lanes. A
    pristine road would read as someone else's live city, not a dead one.
  * Ground pieces stay under 0.5 m so they never block sightlines to machines,
    exactly like belts and pipes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402


def cracked_slab(name, w, d, cell, seed, z=0.0, thickness=0.06):
    """A paving slab with one corner subsided -- reads as old, costs 12 tris."""
    slab = F.box(name, w, d, thickness, cell=cell, bevel=0.0, z=z)
    lift = 0.02 + ((seed % 5) * 0.004)
    for v in slab.data.vertices:
        if v.co.x > 0 and v.co.y > 0:
            v.co.z += lift
    return slab


# --- town road: 1 m tile with kerbs -----------------------------------------
F.reset()
road = F.join([
    cracked_slab("road_bed", 1.0, 1.0, "slate", seed=1),
    # Kerbs on two sides; the tile is placed rotated so a street gets both edges.
    F.box("road_kerbA", 1.0, 0.09, 0.10, cell="weathered_stone", bevel=0.01, y=-0.455),
    F.box("road_kerbB", 1.0, 0.09, 0.10, cell="weathered_stone", bevel=0.01, y=0.455),
], "town_road")
F.export(road, "town_road", budget=120)

# --- road junction: no kerbs, worn crown ------------------------------------
F.reset()
junction = F.join([
    cracked_slab("junction_bed", 1.0, 1.0, "slate", seed=3),
    F.box("junction_patch", 0.34, 0.34, 0.02, cell="basalt", bevel=0.0, z=0.06),
], "town_road_junction")
F.export(junction, "town_road_junction", budget=100)

# --- highway: the long-haul route between towns -----------------------------
# Wider, raised on a bed, with a centre divider. It should read as a different
# class of thing from a town street even at a glance.
F.reset()
highway = F.join([
    F.box("hw_bed", 1.0, 1.0, 0.10, cell="basalt", bevel=0.0),
    cracked_slab("hw_surface", 0.94, 1.0, "rust", seed=7, z=0.10, thickness=0.05),
    F.box("hw_divider", 0.10, 1.0, 0.07, cell="hazard_yellow", bevel=0.01, z=0.15),
    F.box("hw_railA", 0.06, 1.0, 0.16, cell="gunmetal", bevel=0.01, x=-0.47, z=0.10),
    F.box("hw_railB", 0.06, 1.0, 0.16, cell="gunmetal", bevel=0.01, x=0.47, z=0.10),
], "highway")
F.export(highway, "highway", budget=200)

# Highway with a collapsed section: dropped deck, bent rail.
F.reset()
broken = F.join([
    F.box("hwb_bed", 1.0, 1.0, 0.06, cell="basalt", bevel=0.0),
    cracked_slab("hwb_surface", 0.9, 0.55, "rust", seed=11, z=0.06, thickness=0.05),
    F.box("hwb_rubbleA", 0.3, 0.3, 0.12, cell="slate", bevel=0.02, x=0.2, y=0.3),
    F.box("hwb_rubbleB", 0.22, 0.22, 0.09, cell="granite", bevel=0.02, x=-0.25, y=0.36),
    F.box("hwb_rail", 0.06, 0.45, 0.16, cell="gunmetal", bevel=0.01, x=-0.47, y=-0.25, z=0.06),
], "highway_broken")
F.export(broken, "highway_broken", budget=250)


# --- town buildings ----------------------------------------------------------
def ruined_building(name, w, d, h, cell, seed, floors=0, collapse=0.0):
    """
    A building that has clearly stopped being a building: the shell stands, the
    roof is gone, one wall has come down. Modelled as four separate walls rather
    than a box so the interior is visible and the silhouette is broken.
    """
    t = 0.18                       # wall thickness
    parts = [F.box(name + "_slab", w + 0.3, d + 0.3, 0.08, cell="weathered_stone", bevel=0.02)]

    # Walls, each with its own height so the roofline is ragged.
    heights = [
        h,
        h * (0.9 - collapse * 0.5),
        h * (0.75 - collapse * 0.4),
        h * (0.55 - collapse * 0.3),
    ]
    parts.append(F.box(name + "_wN", w, t, max(heights[0], 0.4), cell=cell, bevel=0.03,
                       y=d / 2 - t / 2, z=0.08))
    parts.append(F.box(name + "_wS", w, t, max(heights[1], 0.4), cell=cell, bevel=0.03,
                       y=-d / 2 + t / 2, z=0.08))
    parts.append(F.box(name + "_wE", t, d, max(heights[2], 0.4), cell=cell, bevel=0.03,
                       x=w / 2 - t / 2, z=0.08))
    # The fourth wall is mostly gone: a stub only.
    stub = max(heights[3] * 0.45, 0.35)
    parts.append(F.box(name + "_wW", t, d * 0.4, stub, cell=cell, bevel=0.03,
                       x=-w / 2 + t / 2, y=-d * 0.28, z=0.08))

    # Surviving floor plates, seen through the missing wall.
    for i in range(floors):
        fz = 0.08 + (i + 1) * (h / (floors + 1))
        parts.append(F.box(name + f"_floor{i}", w * 0.82, d * 0.82, 0.08,
                           cell="cast_iron", bevel=0.01, z=fz))

    # Rubble at the foot of the collapsed side.
    parts.append(F.rock(name + "_rubble", 0.32 + collapse * 0.2, cell="slate",
                        x=-w / 2 - 0.2, y=0.2, seed=seed))
    return F.join(parts, name)


F.reset()
F.export(ruined_building("town_house_small", 3.0, 3.0, 2.6, "clay", seed=2, floors=0,
                         collapse=0.2), "town_house_small", budget=500)

F.reset()
F.export(ruined_building("town_house_mid", 5.0, 4.0, 4.2, "dust_ochre", seed=5, floors=1,
                         collapse=0.15), "town_house_mid", budget=700)

F.reset()
F.export(ruined_building("town_block", 7.0, 6.0, 6.5, "weathered_stone", seed=8, floors=2,
                         collapse=0.1), "town_block", budget=900)

# A tower: the landmark you steer by when navigating a ruined city.
F.reset()
tower = ruined_building("town_tower", 4.5, 4.5, 11.0, "granite", seed=13, floors=3,
                        collapse=0.05)
F.join([
    tower,
    F.cylinder("tower_mast", r=0.09, h=2.2, cell="gunmetal", seg=6, z=11.0),
], "town_tower")
F.parent(F.plate("GLOW_Beacon", 0.16, 0.16, cell="e_alert", z=13.3), tower)
F.export(tower, "town_tower", budget=1200)

# --- plaza centrepiece -------------------------------------------------------
# Every town has one: a monument to whatever the Lattice was proud of here.
F.reset()
monument = F.join([
    F.box("plaza_base", 3.2, 3.2, 0.22, cell="limestone", bevel=0.03),
    F.box("plaza_step", 2.4, 2.4, 0.20, cell="weathered_stone", bevel=0.03, z=0.22),
    F.cone("plaza_spire", r_bottom=0.55, r_top=0.10, h=3.4, cell="galvanized", seg=8, z=0.42),
    F.rock("plaza_fallen", 0.3, cell="granite", x=1.3, y=-1.1, seed=17),
], "town_monument")
F.parent(F.plate("GLOW_Glyph", 0.5, 0.5, cell="e_hologram", z=0.44), monument)
F.export(monument, "town_monument", budget=600)

# --- street furniture --------------------------------------------------------
F.reset()
F.export(F.join([
    F.box("lamp_base", 0.22, 0.22, 0.10, cell="cast_iron", bevel=0.02),
    F.cylinder("lamp_post", r=0.055, h=2.6, cell="gunmetal", seg=6, z=0.10),
    F.box("lamp_arm", 0.5, 0.08, 0.07, cell="gunmetal", bevel=0.01, x=0.2, z=2.66),
], "street_lamp_dead"), "street_lamp_dead", budget=200)

F.reset()
F.export(F.join([
    F.box("hulk_body", 1.9, 3.4, 0.9, cell="rust", bevel=0.05, z=0.22),
    F.box("hulk_cab", 1.5, 1.1, 0.7, cell="cast_iron", bevel=0.04, y=1.0, z=1.12),
    F.cylinder("hulk_wheelA", r=0.33, h=0.2, cell="hazard_black", seg=8, x=-0.85, y=-1.0, z=0.33),
    F.cylinder("hulk_wheelB", r=0.33, h=0.2, cell="hazard_black", seg=8, x=0.85, y=-1.0, z=0.33),
], "street_hulk"), "street_hulk", budget=400)
