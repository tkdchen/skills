---
name: getting-koji-builds-for-python-packages
description: Use when ask to get the latest RPM build for a Python package from koji.
---

# Overview

Query the corresponding latest RPM package build from Koji build system for a given Python package.

The Python package is given by a name, a PyPI name generally, and with or without specifier and markers.

# Name conversion

Run this script to convert the names.

```python
import sys
from packaging.requirements import Requirement

"""Convert PyPI name to a list of RPM package candidate names"""

pypi_name = sys.argv[1]
r = Requirement(pypi_name)
name = r.name
if name.lower() == "django":
    majors = (6, 5)
    for m in majors:
        print(f"python-django{m}")
if name.lower() == "pyyaml":
    print("PyYAML")
else:
    print("python-" + name)
    print("python3-" + name)
    print("python-" + name.removeprefix("py"))
```

# Query latest build from Koji

Run this script which reads the candidate package names from a file.

```bash
while read -r candidate_name
do
    printf "Checking candidate package name: %s\n" "$candidate_name" >&2
    found=true
    for rel in <release>; do
        build_info=$(koji latest-build --quiet "$rel" "$candidate_name")
        printf "%s" "$build_info"
        if [[ -z "$build_info" ]]; then
            found=false
            break
        fi
    done
    if [[ "$found" == true ]]; then
        break
    fi
done <"$candidate_package_names_file"
```

`<release>` is expanded to current supported Fedora releases.

# Process

- Run the Python script to get candidate package names.
- Write them into a file.
- Run the Bash script to query the latest RPM build.

# Reference

- Package - [Requirements](https://packaging.pypa.io/en/stable/requirements.html)
