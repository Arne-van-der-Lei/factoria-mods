"""Forges — monolithic single volumes, slightly tapered, one dark recessed mouth.

Mass is the message: minimal appendages. Stone tier is masonry-chamfered;
steel adds riveted banding; the arc tier gets a coil ring instead of a chimney.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402


def mouth(name, w, h, y, z, cell="e_furnace"):
    """A recessed arch: dark surround + emissive inner plate (no booleans)."""
    surround = F.box(name + "_surround", w + 0.14, 0.10, h + 0.14,
                     cell="machine_shadow", bevel=0.02, y=y, z=z)
    glow = F.plate("GLOW_Mouth", w, h, cell=cell, y=y - 0.055, z=z + h / 2.0 + 0.07)
    glow.rotation_euler = (1.5708, 0, 0)
    return surround, glow


F.reset()
body = F.join([
    F.box("slag_body", 1.75, 1.75, 1.55, cell="weathered_stone", bevel=0.05),
    F.box("slag_cap", 1.45, 1.45, 0.22, cell="granite", bevel=0.04, z=1.55),
    F.cylinder("slag_flue", r=0.20, h=0.55, cell="basalt", seg=8, x=0.45, y=0.45, z=1.77),
    F.box("slag_hearth", 1.9, 1.9, 0.16, cell="basalt", bevel=0.03),
], "slag_forge")
sur, glow = mouth("slag", 0.62, 0.52, -0.88, 0.28)
F.join([body, sur], "slag_forge")
F.parent(glow, body)
F.export(body, "slag_forge", budget=800)

F.reset()
body = F.join([
    F.box("blast_body", 1.8, 1.8, 1.85, cell="cast_iron", bevel=0.045),
    F.box("blast_band0", 1.9, 1.9, 0.12, cell="rust", bevel=0.02, z=0.55),
    F.box("blast_band1", 1.9, 1.9, 0.12, cell="rust", bevel=0.02, z=1.25),
    F.cylinder("blast_flue", r=0.22, h=0.70, cell="gunmetal", seg=8, x=0.5, y=0.5, z=1.85),
    F.box("blast_hearth", 1.95, 1.95, 0.16, cell="basalt", bevel=0.03),
], "blast_forge")
sur, glow = mouth("blast", 0.70, 0.58, -0.91, 0.32)
F.join([body, sur], "blast_forge")
F.parent(glow, body)
F.export(body, "blast_forge", budget=1500)

F.reset()
body = F.join([
    F.box("arc_body", 2.7, 2.7, 1.95, cell="steel_mid", bevel=0.05),
    F.box("arc_plinth", 2.95, 2.95, 0.20, cell="cast_iron", bevel=0.03),
    F.cylinder("arc_ring", r=1.05, h=0.16, cell="copper", seg=16, z=1.95),
    F.box("arc_conduit", 0.24, 0.24, 0.85, cell="gunmetal", bevel=0.02, x=1.15, y=1.15, z=1.95),
], "arc_forge")
sur, glow = mouth("arc", 0.95, 0.70, -1.36, 0.40)
F.join([body, sur], "arc_forge")
F.parent(glow, body)
F.parent(F.plate("GLOW_Coil", 1.6, 1.6, cell="e_science_blue", z=2.12), body)
F.export(body, "arc_forge", budget=1500)
