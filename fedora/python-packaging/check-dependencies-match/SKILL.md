---
name: check-dependencies-match
description: Used when asked if Fedora releases X, Y has the required dependencies of upstream version X, or can upstream version X be built.
---

# Requires

- `list-python-package-dependencies`: List dependencies of a Python package from PyPI.
- `query-koji-builds-for-python-packages`: Query latest Fedora RPM build for a Python package.
- `fedora-releases`: Current Fedora releases and their status.

# Workflow

- List dependencies of upstream version.
- Dependencies include standard ones and the extras.
- Exclude meta and testing related extras like `all`, `all...`, `dev`, `devel`, `testing`, but reserve `pytest`, `responses` such packages.
- Get the latest build of every dependency for current Fedora releases
  - Include rawhide
  - Exclude the release going to be EOL
- Generate report in table with columns, PyPI package name, dependency specifier, supported releases (e.g. f43, f44).
- Ask me whether to try next version.
