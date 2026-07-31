"""Reclaimers â€” squat, wide-stance, the rotor mass dominating the top third.

Silhouette brief: the machine is a motor wearing a frame; legs splay outward like
a braced rig, one exhaust stack breaks the symmetry. Reads as "gripping the earth".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factorylib as F  # noqa: E402


def legs(name, span, height, cell="gunmetal", thickness=0.14):
    parts = []
    for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
        parts.append(F.box(f"{name}_leg{i}", thickness, thickness, height, cell=cell,
                           bevel=0.02, x=sx * span, y=sy * span))
        parts.append(F.box(f"{name}_foot{i}", thickness * 2.2, thickness * 2.2, 0.08,
                           cell="cast_iron", bevel=0.02, x=sx * span, y=sy * span))
    return parts


def build(name, size, body_h, rotor_r, burner):
    half = size / 2.0
    body = F.join([
        F.box(name + "_hull", size * 0.82, size * 0.82, body_h, cell="steel_mid", bevel=0.035, z=0.22),
        F.box(name + "_skirt", size * 0.94, size * 0.94, 0.18, cell="cast_iron", bevel=0.03, z=0.06),
        # asymmetry: one exhaust stack
        F.cylinder(name + "_stack", r=0.13, h=0.55, cell="rust", seg=8,
                   x=half * 0.55, y=half * 0.55, z=body_h + 0.22),
        *legs(name, half * 0.78, 0.24),
    ], name)

    # the rotor mass on top â€” the animated part
    rotor = F.join([
        F.cylinder(name + "_rhub", r=rotor_r * 0.45, h=0.22, cell="gunmetal", seg=10),
        F.cylinder(name + "_rrim", r=rotor_r, h=0.12, cell="copper" if burner else "steel_blue", seg=12, z=0.18),
        *[F.box(name + f"_rtooth{i}", 0.12, 0.12, 0.16, cell="hazard_yellow", bevel=0.01,
                x=rotor_r * 0.82 * (1 if i in (0, 3) else -1),
                y=rotor_r * 0.82 * (1 if i in (0, 1) else -1), z=0.10)
          for i in range(4)],
    ], "ANIM_Rotor")
    rotor.location = (0.0, 0.0, body_h + 0.22)
    F.parent(rotor, body)

    if burner:
        glow = F.plate("GLOW_Firebox", 0.34, 0.06, cell="e_furnace", z=0.30, y=-size * 0.41)
        F.parent(glow, body)
    else:
        glow = F.plate("GLOW_Status", 0.26, 0.05, cell="e_science_blue", z=body_h + 0.10, y=-size * 0.41)
        F.parent(glow, body)
    return body


F.reset()
F.export(build("crank_reclaimer", 2.0, 0.85, 0.62, True), "crank_reclaimer", budget=1000)

F.reset()
F.export(build("volt_reclaimer", 3.0, 1.15, 0.95, False), "volt_reclaimer", budget=1500)

# Delver â€” verticality inverted: the shortest 3x3 in the game, boring downward.
F.reset()
delver = F.join([
    F.box("delver_pad", 2.9, 2.9, 0.22, cell="cast_iron", bevel=0.03),
    F.box("delver_hood", 2.1, 2.1, 0.55, cell="steel_mid", bevel=0.04, z=0.22),
    F.cylinder("delver_collar", r=0.75, h=0.30, cell="gunmetal", seg=12, z=0.77),
    *[F.box(f"delver_brace{i}", 0.16, 0.16, 0.62, cell="rust", bevel=0.02,
            x=1.15 * (1 if i in (0, 3) else -1), y=1.15 * (1 if i in (0, 1) else -1), z=0.22)
      for i in range(4)],
], "delver")
bore = F.join([
    F.cylinder("delver_bit", r=0.55, h=0.42, cell="gunmetal", seg=12),
    F.cone("delver_tip", r_bottom=0.55, r_top=0.12, h=0.30, cell="cast_iron", seg=12, z=-0.30),
], "ANIM_Bore")
bore.location = (0.0, 0.0, 0.62)
F.parent(bore, delver)
# same uranium-green pulse as scar cracks â€” the pairing teaches itself
F.parent(F.plate("GLOW_Bore", 0.9, 0.9, cell="e_uranium", z=0.24), delver)
F.export(delver, "delver", budget=1500)
