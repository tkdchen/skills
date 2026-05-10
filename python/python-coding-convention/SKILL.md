---
name: python-coding-convention
description: Python coding skill for writing, refactoring, and organizing Python code. Use when the user asks to write Python scripts, create Python functions, or work with Python code.
---

# Coding Conventions

## General

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

Do not wrap lines of Python code unless they exceed the max line length.

Prefer using `logging` module to calling `print()`.

## Error handling

- Do not call `sys.exit` from inside low level method calls.

- Handle raised errors at higher level method call, inside `main()` generally.

- Code comparison. Bad smell:

    ```python
    def main():
        ...
        foo()
        ...

    def foo():
        ...
        bar()
        ...

    def bar():
        ...
        try:
            subprocess.run()
        except CalledProcessError as e:
            logger.error(...)
            sys.exit(1)
    ```

    Good smell:

    ```python
    def main():
        ...
        try:
            foo()
        except CalledProcessError as e:
            logger.error(...)
        ...
    ```
