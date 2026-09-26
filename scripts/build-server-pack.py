import hashlib, json, pathlib, urllib.parse
root=pathlib.Path("server-pack-files")
files=[]
base="https://raw.githubusercontent.com/m1naaato/Valhalla-Launcher/main/server-pack-files/"
for p in sorted(root.rglob("*")):
    if p.is_file():
        rel=p.relative_to(root).as_posix()
        with p.open("rb") as f:
            sha=hashlib.sha256(f.read()).hexdigest()
        files.append({"path":rel,"url":base+urllib.parse.quote(rel),"sha256":sha,"size":p.stat().st_size})
manifest={"name":"Valhalla Server Pack","version":"auto","minecraftVersion":"26.3","loader":"auto","files":files}
pathlib.Path("server-pack.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
