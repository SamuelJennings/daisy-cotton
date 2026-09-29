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
def count_range(value: object, default: int) -> range:
    """Return ``range(n)`` for looping a template ``n`` times.

    Args:
        value: The count, as an integer or a numeric string. Anything that is
            not a positive whole number is ignored.
        default: The count to use when ``value`` is not a positive whole
            number.

    Returns:
        ``range(n)`` where ``n`` is ``value`` as a positive integer, or
        ``default`` when it is not one.

    Example:
        ``count_range("3", 6)`` -> ``range(0, 3)``
        ``count_range("many", 6)`` -> ``range(0, 6)``
    """
    try:
        count = int(str(value).strip())
    except ValueError:
        count = 0

    return range(count if count > 0 else default)


@register.simple_tag
def filter_options(options: object, value: object) -> list[dict[str, object]]:
    """Return the radio options for a filter, one dict per entry.

    Args:
        options: An iterable whose entries are a bare value, used as its own
            label, or a list or tuple of two, a ``(value, label)`` pair such
            as a Django field's ``choices``. A string, or anything that is not
            iterable, is treated as empty, so ``options="a,b"`` written without
            the colon renders no options rather than one per character.
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
    if isinstance(options, str):
        return []
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


@register.simple_tag
def rating_items(
    highest: object, half: object, value: object
) -> list[dict[str, object]]:
    """Return the items of a rating, one dict per radio or read-only shape.

    Args:
        highest: The highest rating, the component's ``max``, as an integer
            or a numeric string. Anything that is not a positive whole number
            gives five.
        half: Truthy to give two items per whole value, one for each half
            step, from 0.5 up to ``highest``.
        value: The rating to check, compared as a number, so ``7``, ``"7"``
            and ``"7.0"`` all match. Empty, not a number, out of range or off
            the step checks nothing.

    Returns:
        A list of ``{"value", "half", "whole", "checked"}`` dicts in order.
        Whole values are ints, because ``{% blocktrans count %}`` needs a
        number; half values are strings such as ``"1.5"``. ``half`` is ``1``
        or ``2`` alternating on a half rating and ``0`` otherwise, and
        ``whole`` is true on whole values.

    Example:
        ``rating_items(2, True, "1.5")`` ->
        ``[{"value": "0.5", "half": 1, "whole": False, "checked": False},
        {"value": 1, "half": 2, "whole": True, "checked": False},
        {"value": "1.5", "half": 1, "whole": False, "checked": True},
        {"value": 2, "half": 2, "whole": True, "checked": False}]``
    """
    top = len(count_range(highest, 5))
    try:
        chosen = float(str(value).strip())
    except ValueError:
        chosen = None

    if half:
        steps = [
            (step / 2, step % 2 == 0, 2 if step % 2 == 0 else 1)
            for step in range(1, top * 2 + 1)
        ]
    else:
        steps = [(number, True, 0) for number in range(1, top + 1)]

    return [
        {
            "value": int(number) if whole else str(number),
            "half": half_class,
            "whole": whole,
            "checked": chosen == number,
        }
        for number, whole, half_class in steps
    ]


@register.filter
def checked_value(items: list[dict[str, object]]) -> object:
    """Return the value of the checked item from ``rating_items``.

    Args:
        items: The list ``rating_items`` returned.

    Returns:
        The checked item's ``value``, or ``""`` when no item is checked,
        such as for a value out of range, off the step or not a number.

    Example:
        ``checked_value(rating_items(5, False, "3"))`` -> ``3``
    """
    for item in items:
        if item["checked"]:
            return item["value"]

    return ""
