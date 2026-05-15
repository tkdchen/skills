#!/usr/bin/env python3
"""Query the latest RPM build for a Python package from Koji."""

import argparse
import subprocess
import sys

from packaging.requirements import Requirement


def convert_name(pypi_name: str) -> list[str]:
    """Convert PyPI name to a list of RPM package candidate names."""
    r = Requirement(pypi_name)
    name = r.name

    if name.lower() == "django":
        majors = (6, 5)
        candidates = [f"python-django{m}" for m in majors]
    elif name.lower() == "pyyaml":
        candidates = ["PyYAML"]
    else:
        candidates = [
            "python-" + name,
            "python3-" + name,
            "python-" + name.removeprefix("py"),
        ]

    return candidates


def main():
    parser = argparse.ArgumentParser(
        description="Query the latest RPM build for a Python package from Koji."
    )
    parser.add_argument(
        "package",
        help="Python package name (PyPI name, with or without specifiers/markers)",
    )
    parser.add_argument(
        "--releases", "-r",
        nargs="+",
        required=True,
        help="Fedora releases to query (e.g. -r f41 f42)",
    )
    args = parser.parse_args()

    candidates = convert_name(args.package)

    for candidate_name in candidates:
        print(f"Checking candidate package name: {candidate_name}", file=sys.stderr)
        builds_info: list[str] = []
        cmd = ["koji", "latest-build", "--quiet", "release", candidate_name]
        for rel in args.releases:
            cmd[3] = rel
            result = subprocess.run(cmd, capture_output=True, text=True)
            build_info = result.stdout.strip()
            if build_info:
                builds_info.append(build_info)
        if builds_info:
            print(sorted(builds_info))
            break


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("Error on querying latest build:", e.stderr, file=sys.stderr)
        raise
