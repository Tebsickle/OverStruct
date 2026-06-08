import json
from pathlib import Path

for f in Path("data/minecraft/worldgen/structure_set").rglob("*.json"):
    with open(f) as fp:
        data = json.load(fp)

    placement = data.get("placement", {})

    if "spacing" in placement:
        placement["spacing"] = 2

    if "separation" in placement:
        placement["separation"] = 1

    with open(f, "w") as fp:
        json.dump(data, fp, indent=2)