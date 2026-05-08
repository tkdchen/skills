---
name: list-python-package-dependencies
description: List dependencies of a Python package from PyPI. Use this skill whenever the user asks about Python package dependencies, requirements, what packages depend on, or needs to see the dependency list for any Python package. Triggers on phrases like "list dependencies", "what does X depend on", "show requirements for", "check dependencies", or any mention of Python package requirements.
---

# List Python Package Dependencies

This skill retrieves and displays the dependencies of Python packages from PyPI by downloading the source distribution (sdist) and extracting dependency information from PKG-INFO.

## Why This Approach

Downloading the sdist and reading PKG-INFO directly from the package metadata is the most reliable way to get accurate dependency information. This avoids inconsistencies that can occur when relying on PyPI's API or web scraping, and ensures you're seeing exactly what the package declares in its distribution metadata.

## Input Format

Accept a single package specification:
- Package name only: `django` (gets latest version)
- Package with version: `django==4.2.0`

## Process

Run commands:

```bash
python3 scripts/list-deps.py <package spec> --format yaml --strip-markers
```

Example output:

```
asgiref>=3.6.0,<4
sqlparse>=0.3.1
argon2-cffi>=19.1.0
bcrypt
```

If ask to exclude specific extras, pass `-e` to the script:

```bash
python3 scripts/list-deps.py <package spec> --format yaml --strip-markers -e <extra name1> <extra name2> ...
```

## Output

Output the command output directly without change and summarization.

## Error Handling

- If script fails to list deps, it will report to stderr.
- Continue with remaining packages if processing multiple packages
