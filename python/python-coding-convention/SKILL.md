---
name: python-coding-convention
description: Python coding skill for writing, refactoring, and organizing Python code. Use when the user asks to write Python scripts, create Python functions, or work with Python code.
---

Prefer sphinx-style docstring.

Docstring describes method and class itself, arguments, return value and exceptions. Don't include examples code.

Docstring must also describe the types of arguments and return value.

Always annotate types, arguments and return value.

Prefer type union operator `|` to `Optional`.

Prefer data class defined by `attrs.define` to `NamedTuple`.

Prefer argparse to fetch CLI arguments from `sys.argv`.

Prefer using standard Collections as generic types rather to importing `List` and `Dict`.

Code must pass flake8 check with default rules. Max line length is 100.

Code must pass black check with default rules. Max line length is 100.

