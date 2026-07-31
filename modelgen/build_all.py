#!/usr/bin/env python3
"""Run every generator headlessly, rebuilding only what changed.

Change detection uses the SHA1 of the generator source plus factorylib.py and
palette.py (content hash, not mtime, so a fresh git checkout doesn't force a
full rebuild). Stamps live in .build_stamps.json next to this script.

    python build_all.py                 # incremental
    python build_all.py --force         # rebuild everything
    python build_all.py --blender <exe> # explicit Blender path
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STAMPS = os.path.join(HERE, ".build_stamps.json")
SHARED = ["factorylib.py", "palette.py"]
TIMEOUT = 300


def find_blender() -> str | None:
    if "--blender" in sys.argv:
        return sys.argv[sys.argv.index("--blender") + 1]
    env = os.environ.get("BLENDER")
    if env and os.path.exists(env):
        return env
    which = shutil.which("blender")
    if which:
        return which
    roots = [r"C:\Program Files\Blender Foundation", r"C:\Program Files (x86)\Blender Foundation"]
    found = []
    for root in roots:
        if os.path.isdir(root):
            for entry in sorted(os.listdir(root), reverse=True):
                exe = os.path.join(root, entry, "blender.exe")
                if os.path.exists(exe):
                    found.append(exe)
    return found[0] if found else None


def sha1_of(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def main() -> int:
    force = "--force" in sys.argv
    blender = find_blender()
    if not blender:
        print("ERROR: Blender not found. Install Blender 4.5 LTS or pass --blender <exe>.")
        return 1

    shared_hash = hashlib.sha1()
    for name in SHARED:
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            shared_hash.update(sha1_of(p).encode())
    shared_key = shared_hash.hexdigest()

    stamps = {}
    if os.path.exists(STAMPS) and not force:
        try:
            stamps = json.loads(open(STAMPS, encoding="utf-8").read())
        except json.JSONDecodeError:
            stamps = {}

    gens = sorted(f for f in os.listdir(HERE) if f.startswith("gen_") and f.endswith(".py"))
    if not gens:
        print("ERROR: no gen_*.py generators found")
        return 1

    # The palette texture is pure Python — always cheap, always first.
    subprocess.run([sys.executable, os.path.join(HERE, "palette.py")], check=False)

    built, skipped, failed = [], [], []
    for gen in gens:
        key = sha1_of(os.path.join(HERE, gen)) + ":" + shared_key
        if stamps.get(gen) == key and not force:
            skipped.append(gen)
            continue
        print(f"--- {gen}")
        t0 = time.time()
        try:
            proc = subprocess.run(
                [blender, "-b", "--factory-startup", "--python-exit-code", "1", "--python", gen],
                cwd=HERE, capture_output=True, text=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"    TIMEOUT after {TIMEOUT}s")
            failed.append(gen)
            continue
        for line in proc.stdout.splitlines():
            if line.startswith(("[OK", "[WARN", "  !")):
                print("   ", line)
        if proc.returncode != 0:
            tail = [ln for ln in (proc.stdout + proc.stderr).splitlines()
                    if "Error" in ln or "line " in ln][-6:]
            for ln in tail:
                print("    ", ln)
            failed.append(gen)
            continue
        stamps[gen] = key
        built.append((gen, time.time() - t0))

    with open(STAMPS, "w", encoding="utf-8") as fh:
        json.dump(stamps, fh, indent=2, sort_keys=True)

    print(f"\nbuilt {len(built)}, skipped {len(skipped)}, failed {len(failed)}")
    for gen, dt in built:
        print(f"  built  {gen} ({dt:.1f}s)")
    for gen in failed:
        print(f"  FAILED {gen}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
