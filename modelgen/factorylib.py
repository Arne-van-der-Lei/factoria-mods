"""factorylib — shared Blender helpers for The Stilled World model generators.

Design rules (from the art bible):
  * One material for everything: UVs collapse to the center of a palette cell,
    so a 64x64 point-filtered texture colors the whole game in one draw call.
  * Origin at footprint ground-center, 1 m grid, meters, FBX scale 1 in Unity.
  * Bevel every visible edge 2-4 cm; no modeled detail under 5 cm (VR legibility).
  * No booleans (headless EXACT solver makes slivers) - overlap solid primitives.
  * Animatable children are named ANIM_*, emissive children GLOW_*, belt surfaces BELT_*.

Usage from a generator:

    import factorylib as F
    F.reset()
    body = F.box("Body", 2.0, 2.0, 1.2, cell="steel_mid", bevel=0.03)
    rotor = F.cylinder("ANIM_Rotor", r=0.5, h=0.5, z=1.2, cell="copper")
    F.parent(rotor, body)
    F.export(body, "crank_reclaimer")
"""
from __future__ import annotations

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------------------
# Palette — 8x8 grid, row 7 reserved for emissives. Must match palette.py.
# ---------------------------------------------------------------------------
PALETTE: dict[str, int] = {}
_ROWS = [
    # row 0 — soils
    ["loam_dark", "loam", "dry_earth", "dust_ochre", "clay", "sunbaked", "pale_silt", "dawn_sand"],
    # row 1 — stone & water
    ["coal_black", "basalt", "slate", "granite", "weathered_stone", "limestone", "deep_water", "shallow_water"],
    # row 2 — machine metals
    ["machine_shadow", "gunmetal", "cast_iron", "steel_mid", "steel_light", "zinc", "galvanized", "worklight_white"],
    # row 3 — resources & brand
    ["copper_deep", "copper", "copper_patina", "iron_blue", "steel_blue", "brass", "rust", "orange"],
    # row 4 — nature
    ["forest_shadow", "pine", "leaf", "sage", "dry_grass", "olive_scrub", "bark", "timber"],
    # row 5 — warning & UI
    ["hazard_black", "hazard_yellow", "signal_red", "signal_green", "signal_blue", "blueprint_blue", "ui_slate", "ui_paper"],
    # row 6 — faction / warden
    ["chitin_dark", "hide_dark", "hide", "belly", "fang_bone", "spawner_flesh", "sludge", "alien_teal"],
    # row 7 — EMISSIVE
    ["e_furnace", "e_ember", "e_lamp", "e_hologram", "e_alert", "e_science_green", "e_science_blue", "e_uranium"],
]
for _r, _names in enumerate(_ROWS):
    for _c, _n in enumerate(_names):
        PALETTE[_n] = _r * 8 + _c

GRID = 8
EMISSIVE_ROW = 7


def cell_uv(cell: str | int) -> tuple[float, float]:
    """Center UV of a palette cell. Collapsed UVs cannot bleed or mip-smear."""
    idx = PALETTE[cell] if isinstance(cell, str) else int(cell)
    col, row = idx % GRID, idx // GRID
    return ((col + 0.5) / GRID, 1.0 - (row + 0.5) / GRID)


def is_emissive(cell: str | int) -> bool:
    idx = PALETTE[cell] if isinstance(cell, str) else int(cell)
    return idx // GRID == EMISSIVE_ROW


# ---------------------------------------------------------------------------
# Scene management
# ---------------------------------------------------------------------------
def reset() -> None:
    """Wipe the scene. Every generator starts from an empty file."""
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _finish(mesh_obj, cell):
    """Assign palette UVs, recalc normals, flat shade."""
    me = mesh_obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)  # inverted normals = invisible in Unity
    uv_layer = bm.loops.layers.uv.verify()
    u, v = cell_uv(cell)
    for face in bm.faces:
        face.smooth = False
        for loop in face.loops:
            loop[uv_layer].uv = (u, v)
    bm.to_mesh(me)
    bm.free()
    me.validate()
    return mesh_obj


def _new_obj(name: str, bm: bmesh.types.BMesh, cell, loc=(0.0, 0.0, 0.0)):
    me = bpy.data.meshes.new(name + "_mesh")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    return _finish(obj, cell)


# ---------------------------------------------------------------------------
# Primitives — all origins at bottom-center unless stated, meters
# ---------------------------------------------------------------------------
def box(name: str, w: float, d: float, h: float, cell="steel_mid", bevel: float = 0.03,
        x: float = 0.0, y: float = 0.0, z: float = 0.0, segments: int = 1):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector((w, d, h)), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector((0, 0, h / 2.0)), verts=bm.verts)
    if bevel > 0.0:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bevel,
                        segments=segments, profile=0.5, affect="EDGES")
    return _new_obj(name, bm, cell, (x, y, z))


def cylinder(name: str, r: float, h: float, cell="steel_mid", seg: int = 12,
             x: float = 0.0, y: float = 0.0, z: float = 0.0, bevel: float = 0.02):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=r, radius2=r, depth=h)
    bmesh.ops.translate(bm, vec=Vector((0, 0, h / 2.0)), verts=bm.verts)
    if bevel > 0.0:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bevel, segments=1,
                        profile=0.5, affect="EDGES")
    return _new_obj(name, bm, cell, (x, y, z))


def cone(name: str, r_bottom: float, r_top: float, h: float, cell="steel_mid", seg: int = 12,
         x: float = 0.0, y: float = 0.0, z: float = 0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=r_bottom, radius2=r_top, depth=h)
    bmesh.ops.translate(bm, vec=Vector((0, 0, h / 2.0)), verts=bm.verts)
    return _new_obj(name, bm, cell, (x, y, z))


def pipe_segment(name: str, r: float, length: float, cell="cast_iron", seg: int = 8,
                 x: float = 0.0, y: float = 0.0, z: float = 0.0, axis: str = "X"):
    """A horizontal pipe run of `length` along the given axis, centered on origin."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=r, radius2=r, depth=length)
    rot = {"X": (0, math.pi / 2, 0), "Y": (math.pi / 2, 0, 0), "Z": (0, 0, 0)}[axis]
    obj = _new_obj(name, bm, cell, (x, y, z))
    obj.rotation_euler = rot
    return obj


def plate(name: str, w: float, d: float, cell="steel_mid", z: float = 0.01,
          x: float = 0.0, y: float = 0.0, thickness: float = 0.02):
    """A thin flat slab — floors, panels, belt surfaces, decals."""
    return box(name, w, d, thickness, cell=cell, bevel=0.0, x=x, y=y, z=z)


def truss(name: str, length: float, height: float, cell="gunmetal", bars: int = 4,
          thickness: float = 0.08, x: float = 0.0, y: float = 0.0, z: float = 0.0):
    """A simple lattice mast: two rails plus diagonal bars, joined into one mesh."""
    parts = [
        box(name + "_r0", thickness, thickness, height, cell=cell, bevel=0.01, x=-length / 2),
        box(name + "_r1", thickness, thickness, height, cell=cell, bevel=0.01, x=length / 2),
    ]
    for i in range(bars):
        zz = height * (i + 0.5) / bars
        parts.append(box(name + f"_b{i}", length, thickness, thickness, cell=cell, bevel=0.0, z=zz))
    obj = join(parts, name)
    obj.location = (x, y, z)
    return obj


def rock(name: str, r: float, cell="granite", x=0.0, y=0.0, z=0.0, seed: int = 0):
    """A low-poly boulder: an icosphere squashed deterministically."""
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
    for i, v in enumerate(bm.verts):
        k = ((seed * 37 + i * 11) % 7) / 20.0  # deterministic, no RNG
        v.co.x *= 1.0 + k
        v.co.y *= 1.0 - k * 0.5
        v.co.z *= 0.7 + k
    bmesh.ops.translate(bm, vec=Vector((0, 0, r * 0.6)), verts=bm.verts)
    return _new_obj(name, bm, cell, (x, y, z))


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------
def join(objs: list, name: str):
    """Merge meshes into one object (used instead of booleans)."""
    objs = [o for o in objs if o is not None]
    if not objs:
        raise ValueError("join() got no objects")
    if len(objs) == 1:
        objs[0].name = name
        return objs[0]
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = name
    return joined


def parent(child, par):
    """Parent keeping world transform (child origins are its animation pivot)."""
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()
    return child


PREFIXES = ("ANIM_", "GLOW_", "BELT_", "STAGE_")


def validate(root) -> list[str]:
    """Naming + budget checks; returns a list of problems (empty = good)."""
    problems: list[str] = []
    seen: set[str] = set()

    def walk(o):
        if o.name in seen:
            problems.append(f"duplicate object name '{o.name}' (FBX would add .001)")
        seen.add(o.name)
        if o is not root and not o.name.startswith(PREFIXES):
            problems.append(f"child '{o.name}' lacks an ANIM_/GLOW_/BELT_/STAGE_ prefix")
        for c in o.children:
            walk(c)

    walk(root)
    return problems


def tri_count(root) -> int:
    total = 0
    stack = [root]
    while stack:
        o = stack.pop()
        if o.type == "MESH":
            total += sum(max(len(p.vertices) - 2, 0) for p in o.data.polygons)
        stack.extend(o.children)
    return total


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
def out_dir() -> str:
    """`-- --out <dir>` from the command line, else <repo>/base/models."""
    argv = sys.argv
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        if "--out" in rest:
            return rest[rest.index("--out") + 1]
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "base", "models"))


def export(root, name: str, budget: int = 0) -> str:
    """Rotate to Unity's Y-up, export FBX at scale 1, print a one-line summary."""
    problems = validate(root)
    tris = tri_count(root)
    if budget and tris > budget:
        problems.append(f"tri budget exceeded: {tris} > {budget}")
    for p in problems:
        print(f"  ! {name}: {p}")

    # Y-up fix on the root only (bake_space_transform is broken for deep hierarchies)
    bpy.ops.object.select_all(action="DESELECT")
    root.select_set(True)
    bpy.context.view_layer.objects.active = root
    root.rotation_euler = (-math.pi / 2, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    root.rotation_euler = (math.pi / 2, 0, 0)

    target = out_dir()
    os.makedirs(target, exist_ok=True)
    path = os.path.join(target, name + ".fbx")

    def sel(o):
        o.select_set(True)
        for c in o.children:
            sel(c)

    bpy.ops.object.select_all(action="DESELECT")
    sel(root)
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        apply_scale_options="FBX_SCALE_UNITS",
        apply_unit_scale=True,
        global_scale=1.0,
        axis_forward="-Z",
        axis_up="Y",
        object_types={"MESH", "EMPTY"},
        mesh_smooth_type="FACE",
        use_triangles=True,
        bake_anim=False,
        add_leaf_bones=False,
        bake_space_transform=False,
        path_mode="COPY",
    )
    status = "OK " if not problems else "WARN"
    print(f"[{status}] {name}: {tris} tris -> {path}")
    return path
