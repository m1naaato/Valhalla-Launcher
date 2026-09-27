"""Build a validated client manifest from approved DD&SS server assets."""
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

root = Path("ddss-pack-files")
allowed = {
    "mods": {".jar"},
    "scripts": {".zs"},
    "config/betterquesting": {".json", ".cfg"},
    "config/artisanworktables": {".json", ".cfg"},
    "config/modularmachinery": {".json", ".cfg"},
    "config": {".cfg"},
}
files = []
for directory, extensions in allowed.items():
    source = root / directory
    if not source.exists():
        continue
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        relative = path.relative_to(root).as_posix()
        if directory == "config/modularmachinery" and relative not in {
            "config/modularmachinery/machinery/advanced_alloysmelter.json",
            "config/modularmachinery/machinery/master_assembler.json",
            "config/modularmachinery/machinery/variables/casings.var.json",
            "config/modularmachinery/modularmachinery.cfg",
        }:
            continue
        if directory == "config" and relative not in {"config/cyclicmagic.cfg", "config/natura.cfg"}:
            continue
        size = path.stat().st_size
        if size > 95 * 1024 * 1024:
            raise SystemExit(f"File too large for public GitHub: {relative}")
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        url = "https://raw.githubusercontent.com/m1naaato/Valhalla-Launcher/main/ddss-pack-files/" + quote(relative)
        files.append({"path": relative, "url": url, "sha256": sha, "size": size})
mods = [x for x in files if x["path"].startswith("mods/")]
if len(mods) < 100:
    raise SystemExit(f"DD&SS pack incomplete: only {len(mods)} mods")
if any("neoforge" in x["path"].lower() for x in mods):
    raise SystemExit("Old NeoForge mod detected; refused to publish.")
manifest = {
    "name": "DD&SS Valhalla",
    "version": "server",
    "minecraftVersion": "1.12.2",
    "loader": "Forge",
    "files": files,
}
Path("ddss-server-pack.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
