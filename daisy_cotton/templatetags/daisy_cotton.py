"""Template tags shared across daisy-cotton's own components."""

import uuid
from collections.abc import Sequence

from django import template

register = template.Library()

BREAKPOINTS = ("sm", "md", "lg", "xl", "2xl")


@register.simple_tag
def responsive(var: object, klass: str) -> str:
    """Return a class name, plain or breakpoint-prefixed, from a variant flag.

    Args:
        var: ``True`` for the unprefixed class, a breakpoint name (one of
            ``BREAKPOINTS``) for a responsive variant, or anything else to
            suppress output.
        klass: The class name to return, with or without a breakpoint prefix.

    Returns:
        ``klass`` if ``var`` is ``True``, ``"{var}:{klass}"`` if ``var`` is a
        breakpoint name, or ``""`` otherwise.

    Example:
        ``responsive(True, "divider-horizontal")`` -> ``"divider-horizontal"``
        ``responsive("md", "divider-horizontal")`` -> ``"md:divider-horizontal"``
    """
    if var is True:
        return klass
    elif isinstance(var, str) and var in BREAKPOINTS:
        return f"{var}:{klass}"

    return ""


@register.simple_tag
def variation(var: object, klass: str, allowed: str | Sequence[str]) -> str:
    """Return a modifier class built from ``klass`` and ``var``.

    Args:
        var: The variant name to test against ``allowed``.
        klass: The base class name to prefix the variant onto.
        allowed: The variant names that produce output, as a list or a
            comma-separated string.

    Returns:
        ``"{klass}-{var}"`` when ``var`` is one of ``allowed``, otherwise
        ``""``.

    Example:
        ``variation("sm", "btn", "sm,md,lg")`` -> ``"btn-sm"``
    """
    if isinstance(allowed, str):
        allowed = allowed.split(",")

    if var in allowed:
        return f"{klass}-{var}"

    return ""


@register.simple_tag
def unique_id(prefix: str) -> str:
    """Return a random id string prefixed with ``prefix``.

    Args:
        prefix: The string to prefix the generated id with.

    Returns:
        ``"{prefix}-"`` plus eight lowercase hex characters, different on
        every call.

    Example:
        ``unique_id("dropdown")`` -> ``"dropdown-3fa2b91c"``
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


@register.simple_tag
def filter_options(options: object, value: object) -> list[dict[str, object]]:
    """Return the radio options for a filter, one dict per entry.

    Args:
        options: An iterable whose entries are a bare value, used as its own
            label, or a list or tuple of two, a ``(value, label)`` pair such
            as a Django field's ``choices``. Anything that is not iterable is
            treated as empty.
        value: The value to check. Compared with each entry's value as a
            string, so ``2`` matches ``"2"``. ``None`` and ``""`` check
            nothing.

    Returns:
        A list of ``{"value", "label", "checked"}`` dicts in the order given,
        empty when ``options`` is empty or not iterable.

    Example:
        ``filter_options(["Open", ("c", "Closed")], "c")`` ->
        ``[{"value": "Open", "label": "Open", "checked": False},
        {"value": "c", "label": "Closed", "checked": True}]``
    """
    try:
        entries = list(options)  # type: ignore[call-overload]
    except TypeError:
        return []

    has_value = value is not None and value != ""
    result = []
    for entry in entries:
        if isinstance(entry, list | tuple) and len(entry) == 2:
            entry_value, label = entry
        else:
            entry_value = label = entry
        result.append(
            {
                "value": entry_value,
                "label": label,
                "checked": has_value and str(entry_value) == str(value),
            }
        )

    return result
