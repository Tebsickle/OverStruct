import json
from pathlib import Path
import random

SETTINGS_FILE = Path(__file__).with_name("currentSettings.txt")


def load_current_settings() -> dict[str, int]:
    settings = {"spacing": 32, "separation": 1}

    if not SETTINGS_FILE.exists():
        return settings

    for line in SETTINGS_FILE.read_text().splitlines():
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()

        if key in settings:
            try:
                settings[key] = int(value.strip())
            except ValueError:
                pass

    return settings


def prompt_for_value(label: str, current_value: int) -> int:
    while True:
        raw_value = input(f"Enter {label} (current: {current_value}, press Enter to keep): ").strip()
        if raw_value == "":
            return current_value

        try:
            return int(raw_value)
        except ValueError:
            print(f"Please enter a whole number or press Enter to keep {current_value}.")


current_settings = load_current_settings()
spacing = prompt_for_value("spacing", current_settings["spacing"])
separation = prompt_for_value("separation", current_settings["separation"])

for f in Path("data/minecraft/worldgen/structure_set").rglob("*.json"):
    with open(f) as fp:
        data = json.load(fp)

    placement = data.get("placement", {})

    if "spacing" in placement:
        placement["spacing"] = spacing

    if "separation" in placement:
        placement["separation"] = separation

    if "salt" in placement:
        placement["salt"] = random.randint(10000, 99999)

    with open(f, "w") as fp:
        json.dump(data, fp, indent=2)

SETTINGS_FILE.write_text(f"spacing={spacing}\nseparation={separation}\n")