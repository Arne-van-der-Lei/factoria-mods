#!/usr/bin/env python3
"""Generate palette.png — the single 64x64 texture that colors the entire game.

8x8 grid of 8px flat cells. Row 7 is emissive-only. Run with plain Python
(no Blender needed): `python palette.py [--out <dir>]`.

Unity import settings that MUST accompany this texture (set by ModelPostprocessor):
  Filter Mode: Point, Compression: None, Max Size: 64, sRGB on, mips off.
"""
from __future__ import annotations

import os
import struct
import sys
import zlib

CELL = 8
GRID = 8
SIZE = CELL * GRID

ROWS = [
    # row 0 — soils (dark -> dawn)
    ["3E3128", "574434", "6E5741", "8A6F4D", "A3805A", "BC9668", "D2B183", "E8CD9E"],
    # row 1 — stone & water
    ["26241F", "33363B", "4C5157", "6B6F73", "8E9092", "B5B2A6", "1F4A5C", "3C7C8A"],
    # row 2 — machine metals
    ["2B2B30", "3C4048", "52565E", "6C7178", "8B9096", "A9ADB2", "C6C9CC", "E4E4DE"],
    # row 3 — resources & brand
    ["7A3E22", "B5622C", "58907E", "6F7E8E", "4A5E74", "C79A45", "A5402A", "E07B39"],
    # row 4 — nature
    ["223528", "375841", "4F7A4A", "749362", "A3A35F", "6C7A45", "4C3B2A", "A9855A"],
    # row 5 — warning & UI
    ["1E1B18", "E8B23A", "C43B2E", "4FA05E", "3E7DB8", "5E8FB0", "2C3440", "E9E2D0"],
    # row 6 — faction / warden
    ["2E2430", "4A2E3A", "6E4152", "A5766B", "D8C9A8", "8A4E5E", "5E5A3A", "3F6B66"],
    # row 7 — EMISSIVE
    ["FF7A1A", "FFC33D", "FFE9C4", "4FD8FF", "FF3B30", "58FF7D", "4D8CFF", "9BFF3B"],
]


def rgb(h: str) -> tuple[int, int, int]:
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def build_png() -> bytes:
    raw = bytearray()
    for y in range(SIZE):
        raw.append(0)  # filter type 0 per scanline
        row_colors = ROWS[y // CELL]
        for x in range(SIZE):
            r, g, b = rgb(row_colors[x // CELL])
            raw += bytes((r, g, b))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 2, 0, 0, 0)  # 8-bit RGB
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def out_dir() -> str:
    if "--out" in sys.argv:
        return sys.argv[sys.argv.index("--out") + 1]
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "base", "models"))


def main() -> int:
    target = out_dir()
    os.makedirs(target, exist_ok=True)
    path = os.path.join(target, "palette.png")
    with open(path, "wb") as fh:
        fh.write(build_png())
    print(f"[OK ] palette.png: {SIZE}x{SIZE}, {GRID * GRID} cells -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
