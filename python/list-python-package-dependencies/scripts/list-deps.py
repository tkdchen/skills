#!/usr/bin/env python3
"""
List dependencies of Python packages from PyPI.

This script downloads the source distribution (sdist) of a package and extracts
dependency information from PKG-INFO metadata.
"""

import argparse
import email.parser
import json
import re
import sys
import tempfile
from pathlib import Path
from subprocess import run, CalledProcessError
from collections.abc import Iterable


def list_dependencies(package_spec: str, exclude_extras: list[str] | None = None) -> Iterable[str]:
    """
    List dependencies for a given package specification.

    :param package_spec: Package name or ``package==version``.
    :type package_spec: str
    :param exclude_extras: List of extra names to exclude from output.
    :type exclude_extras: list[str] or None
    """
    with tempfile.TemporaryDirectory() as work_dir:
        tmpdir_path = Path(work_dir)

        cmd = ["pip", "download", "--no-deps", "--no-binary", ":all:", package_spec]
        run(cmd, cwd=work_dir, capture_output=True, text=True, check=True)

        tarballs = list(tmpdir_path.glob("*.tar.gz"))
        if not tarballs:
            msg = f"Error: {package_spec} has no source distribution (sdist) available, only wheels"
            raise FileNotFoundError(msg)

        tarball = tarballs[0]

        extract_cmd = ["tar", "-Oxzf", str(tarball), "--wildcards", "*/PKG-INFO", "--strip-components=1"]
        proc = run(extract_cmd, cwd=work_dir, capture_output=True, text=True, check=True)

        exclude_extras_suffix = []
        if exclude_extras:
            exclude_extras_suffix = [f'; extra == "{extra}"' for extra in exclude_extras]

        parser = email.parser.Parser()
        pkg_info = parser.parsestr(proc.stdout)

        for info_key, value in pkg_info.items():
            if info_key == "Requires-Dist":
                if any(value.endswith(suffix) for suffix in exclude_extras_suffix):
                    continue
                yield value


class FlatView:

    def __init__(self, data: list[str], writer=None, strip_markers=False) -> None:
        self._data = data
        self._writer = writer or sys.stdout

    def as_normal(self):
        writer = self._writer
        for item in self._data:
            print(item.split(";")[0], file=writer)

    def as_json(self):
        json.dump([item.split(";")[0] for item in self._data], self._writer)

    def as_yaml(self):
        for item in self._data:
            print("-", item.split(";")[0], file=self._writer)


class GroupView:

    def __init__(self, data: list[str], writer = None) -> None:
        self._data = data
        self._writer = writer or sys.stdout
        # extra name -> package spec
        self._groups: dict[str, list[str]] = {"base": []}
        self._group_package_specs()

    def _group_package_specs(self) -> None:
        for item in self._data:
            if match := re.search(r"extra == \"([-\w]+)\"", item):
                key = match.group(1)
                package_spec = item.split(";")[0]
                self._groups.setdefault(key, []).append(package_spec)
            else:
                self._groups["base"].append(item)

    def as_normal(self):
        writer = self._writer
        for key, value in self._groups.items():
            print(key + ":", file=writer)
            for package_spec in value:
                print("\t", package_spec, file=writer)

    def as_json(self):
        json.dump(self._groups, self._writer)

    def as_yaml(self):
        writer = self._writer
        for key, package_specs in self._groups.items():
            print(key + ":", file=writer)
            for item in package_specs:
                print("-", item, file=writer)


def main():
    parser = argparse.ArgumentParser(
        description="List dependencies of Python packages from PyPI"
    )
    parser.add_argument("package", help="Package specification (e.g., 'django' or 'django==4.2.0')")
    parser.add_argument(
        "-e", "--exclude-extras", nargs="+", metavar="EXTRA", help="Exclude dependencies for specific extras"
    )
    parser.add_argument("-g", "--group", action="store_true", dest="group_extras", help="Group extras.")
    parser.add_argument("--format", choices=["json", "yaml"], help="Output format.")
    parser.add_argument("--strip-markers", action="store_true", help="Strip markers part completely. This does not apply to grouping dependencies.")

    args = parser.parse_args()

    try:
        deps = list_dependencies(args.package, args.exclude_extras)
    except CalledProcessError as e:
        print("Error on listing dependencies:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("Error on listing dependencies:", str(e), file=sys.stderr)
        sys.exit(1)

    if args.group_extras:
        view = GroupView(list(deps))
    else:
        view = FlatView(list(deps))

    match args.format:
        case "json":
            view.as_json()
        case "yaml":
           view.as_yaml()
        case _:
            view.as_normal()


if __name__ == "__main__":
    main()
