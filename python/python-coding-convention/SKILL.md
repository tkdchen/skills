---
name: python-coding-convention
description: Use when writing, refactoring, or organizing Python code. Enforces conventions for docstrings (Sphinx-style), type annotations (builtin generics not typing imports), logging (not print), error handling (exceptions to main not sys.exit in helpers). Triggers on Python scripts, modules, CLI tools, or mentions of style, conventions, formatting, flake8, black.
---

# Coding Conventions

## General

Prefer sphinx-style docstring.

Docstring describes method and class itself, arguments, return value and exceptions. Don't include examples code.

Docstring must also describe the types of arguments and return value. Prefer `type` field line. Example:

```python
def send_message(sender: str, recipient: str, message_body: str, priority: int | None = None) -> int:
    """Send a message to a recipient

    :param sender: The person sending the message
    :type sender: str
    :param recipient: The recipient of the message
    :type recipient: str
    :param message_body: The body of the message
    :type message_body: str
    :param priority: The priority of the message, can be a number 1-5
    :type priority: int | None
    :return: The message id
    :rtype: int
    :raises ValueError: if the message_body exceeds 160 characters
    :raises TypeError: if the message_body is not a str
    """
```

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

## References

- [Sphinx Python Domain - Info fields](https://www.sphinx-doc.org/en/master/usage/domains/python.html#info-field-lists)
