---
name: getting-koji-builds-for-python-packages
description: Use when ask to get the latest RPM build for a Python package from koji.
---

# Overview

Query the corresponding latest RPM package build from Koji build system for a given Python package.

The Python package is given by a name, a PyPI name generally, and with or without specifier and markers.

# Scripts

- `scripts/query.py`: query latest Fedora package build for a given Python package.

# Usage

Run `scripts/query.py`:

```bash
python scripts/query.py <pypi-name> --releases f41 f42
```

It converts the PyPI name to RPM candidate names, queries Koji for each across
the specified Fedora releases, and returns the first candidate found in all
releases.

- `<pypi-name>` (positional, required): Python package name.
- `--releases` / `-r` **(required)**: Fedora releases to query (e.g. `-r f41 f42`).

## Name conversion rules

- `django` → `python-django6`, `python-django5`
- `PyYAML` → `PyYAML`
- Other packages → `python-<name>`, `python3-<name>`, `python-<name>` (with `py` prefix stripped)

# Reference

- Package - [Requirements](https://packaging.pypa.io/en/stable/requirements.html)
