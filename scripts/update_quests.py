#!/usr/bin/env python3
"""Generate the MSQ list from the community wiki's ordered main-scenario tables.

Run: pip install requests beautifulsoup4
     python scripts/update_quests.py
"""
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE = "https://ffxiv.consolegameswiki.com/wiki/Main_Scenario_Quests"
OUTPUT = Path(__file__).resolve().parents[1] / "quests.json"
START = "Soul Searching"
END = "The Coming Dawn"  # not used as cutoff; retained only as a known checkpoint
HEADINGS = (
    "Post-Stormblood Main Scenario Quests",
    "Shadowbringers Main Scenario Quests",
    "Post-Shadowbringers Main Scenario Quests",
    "Post-Shadowbringers Main Scenario Quests II",
    "Endwalker Main Scenario Quests",
    "Post-Endwalker Main Scenario Quests",
    "Dawntrail Main Scenario Quests",
    "Post-Dawntrail Main Scenario Quests",
    "Post-Dawntrail Main Scenario Quests II",
)
def clean(s):
    return re.sub(r"\s+", " ", s).strip()

def main():
    response = requests.get(SOURCE, timeout=45, headers={"User-Agent": "MSQJourneyQuestList/1.0 (noncommercial personal fan tracker)"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    root = soup.select_one(".mw-parser-output") or soup.select_one("#mw-content-text") or soup
    entries = []
    section = ""
    subsection = ""
    started = False
    seen = set()
    for node in root.find_all(["h2", "h3", "h4", "table"]):
        if node.name in ("h2", "h3", "h4"):
            title = clean(node.get_text(" ", strip=True)).replace("[edit]", "").strip()
            if node.name == "h2":
                section = title
                subsection = ""
            elif node.name == "h3":
                subsection = title
            continue
        if not any(section.startswith(s) for s in HEADINGS):
            continue
        rows = node.find_all("tr")
        if not rows:
            continue
        header = [clean(c.get_text(" ", strip=True)).lower() for c in rows[0].find_all(["th", "td"], recursive=False)]
        if not header or not header[0].startswith("quest") or "level" not in header:
            continue
        level_index = header.index("level")
        for tr in rows[1:]:
            cells = tr.find_all(["td", "th"], recursive=False)
            if len(cells) <= level_index:
                continue
            name = clean(cells[0].get_text(" ", strip=True))
            level = clean(cells[level_index].get_text(" ", strip=True))
            if not name or not re.match(r"^\d{1,3}$", level):
                continue
            if not started:
                if name != START:
                    continue
                started = True
            key = (section, name)
            if key in seen:
                continue
            seen.add(key)
            entries.append({"id": f"msq-{len(entries)+1:04d}", "name": name, "expansion": section.replace(" Main Scenario Quests", ""), "patch": subsection, "level": int(level)})
    print(f"DEBUG: found {len(entries)} entries, current section={section!r}, first candidate={entries[:2]!r}")
    if not started:
        raise RuntimeError(f"Could not locate starting quest {START!r}; refusing to overwrite dataset")
    names = [e["name"] for e in entries]
    checkpoints = ["Soul Searching", "A Requiem for Heroes", "The Syrcus Trench", "The Next Ship to Sail", "A New World to Explore", "A Royal Invitation"]
    missing = [x for x in checkpoints if x not in names]
    if missing or len(entries) < 400:
        raise RuntimeError(f"Suspicious quest extraction: {len(entries)} entries, missing checkpoints {missing}; refusing to overwrite dataset")
    if entries[0]["name"] != START:
        raise RuntimeError("Wrong starting quest")
    OUTPUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} quests, {entries[0]['name']} -> {entries[-1]['name']}")

if __name__ == "__main__":
    main()
