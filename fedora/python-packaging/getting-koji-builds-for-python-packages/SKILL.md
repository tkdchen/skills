---
name: getting-koji-builds-for-python-packages
description: Use when asked to get the latest RPM build for a Python package from koji, especially in Fedora packaging contexts
---

# Getting Koji Builds for Python Packages

## Overview

Python packages in Fedora use "python-" or "python3-" prefixes. Try prefixes in order, then bare name. If all fail and name starts with "py", remove it and retry.

**Core principle:** Strip extras first (e.g., `PyJWT[crypto]` → `PyJWT`), then try python-, python3-, bare name. For py-prefixed packages, try again without "py". Stop at 6 attempts max.

## Process

```bash
# Step 0: Strip extras if present (PyJWT[crypto] → PyJWT)
# Remove [...] and everything inside

# Standard 3-step (all packages)
koji latest-build <release> python-<package>
koji latest-build <release> python3-<package>
koji latest-build <release> <package>

# If all fail AND package starts with "py", remove "py" and repeat
koji latest-build <release> python-<package-without-py>
koji latest-build <release> python3-<package-without-py>
koji latest-build <release> <package-without-py>
```

**Stop at first match or after 6 attempts.** Release tags: rawhide, f45, f44, etc.

**Examples:** requests → python-requests, PyJWT[crypto] → python-jwt, pycparser → python-pycparser

## Special Cases

**Django with version:** "django 5" → `python-django5`, "django 6" → `python-django6`. Without version, use standard process.

## Rules

**Do:** Try python-, python3-, bare name. If all fail and starts with "py", remove it and repeat. Stop at first match.

**Don't:** Use wildcards, `koji list-pkgs`, `koji search`, guess version numbers, or try >6 attempts.

## Common Mistakes

- Use only `latest-build`
- Always python-, python3-, bare, then py-removal fallback
- Only 3 attempts for regular, 6 max for py-prefixed packages

## Example

**PyJWT[crypto] (extras + py-removal):**
```bash
# Strip extras: PyJWT[crypto] → PyJWT
koji latest-build rawhide python-pyjwt    # Not found
koji latest-build rawhide python3-pyjwt   # Not found
koji latest-build rawhide pyjwt           # Not found
# Starts with "py", remove it
koji latest-build rawhide python-jwt      # Found ✓
```
