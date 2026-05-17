# My Skills

Personal collection of AI agent skills for daily technical activities.

## Installation

```bash
npx skills@latest install tkdchen/skills
```

## Structure

```
skills/
├── python/
│   ├── list-python-package-dependencies/
│   └── python-coding-convention/
├── fedora/
│   ├── fedora-releases/
│   └── python-packaging/
│       ├── check-dependencies-match/
│       └── query-koji-builds-for-python-packages/
└── quayio/
    └── tags-processing/
```

## Skills

- `list-python-package-dependencies`: List dependencies of a Python package from PyPI by downloading the sdist and extracting from PKG-INFO.
- `python-coding-convention`: Enforce Sphinx-style docstrings, type annotations, logging, and error handling conventions.
- `fedora-releases`: Current Fedora releases, rawhide, and EOL status.
- `check-dependencies-match`: Check if an upstream Python package's dependencies are satisfied in Fedora. Orchestrates `fedora-releases`, `list-python-package-dependencies`, and `query-koji-builds-for-python-packages`.
- `query-koji-builds-for-python-packages`: Query the latest RPM build for a Python package across Fedora releases via Koji.
- `tags-processing`: List and filter image tags from Quay.io registries via REST API.

