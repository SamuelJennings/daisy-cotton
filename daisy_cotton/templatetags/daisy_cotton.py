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
