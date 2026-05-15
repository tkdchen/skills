#!/usr/bin/env python3
"""Validate that SKILL.md's current Fedora releases match live data from bodhi."""

import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen, Request

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"
BODHI_URL = "https://bodhi.fedoraproject.org/releases/?rows_per_page=100"


def parse_skill_releases() -> set[int]:
    """Parse the current Fedora release numbers from SKILL.md."""
    text = SKILL_MD.read_text()
    # Match "Current releases are 44, 43 and 42" pattern
    matches = re.findall(r"\b(\d+)\b", re.search(r"Current releases are\s+(.+)", text).group(1))
    if not matches:
        print("ERROR: Could not parse release numbers from SKILL.md")
        sys.exit(1)
    return {int(m) for m in matches}


def fetch_current_releases() -> set[int]:
    """Fetch currently supported Fedora releases from bodhi API."""
    req = Request(BODHI_URL, headers={"User-Agent": "fedora-releases-validator/1.0"})
    with urlopen(req, timeout=15) as resp:
        data = json.load(resp)

    current = set()
    for release in data.get("releases", []):
        name = release.get("name", "")
        state = release.get("state", "")
        # Match only pure release names like F42, F43, F44 (skip variants like F42C, F42F)
        m = re.match(r"^F(\d+)$", name)
        if m and state == "current":
            current.add(int(m.group(1)))
    return current


def main() -> int:
    skill_releases = parse_skill_releases()
    print(f"SKILL.md releases: {sorted(skill_releases)}")

    try:
        bodhi_releases = fetch_current_releases()
        print(f"Bodhi 'current' releases: {sorted(bodhi_releases)}")
    except Exception as e:
        print(f"ERROR: Failed to fetch from bodhi: {e}")
        return 1

    # Check: all releases in SKILL.md should be in bodhi's current list
    missing_from_bodhi = skill_releases - bodhi_releases
    # Check: all bodhi current releases should be in SKILL.md
    missing_from_skill = bodhi_releases - skill_releases

    if missing_from_bodhi:
        print(f"WARNING: SKILL.md lists releases not in bodhi 'current': {sorted(missing_from_bodhi)}")
    if missing_from_skill:
        print(f"WARNING: SKILL.md is missing current releases from bodhi: {sorted(missing_from_skill)}")

    if not missing_from_bodhi and not missing_from_skill:
        print("✅ SKILL.md is up to date with bodhi.")
        return 0
    else:
        print("⚠️  SKILL.md may need updating.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
