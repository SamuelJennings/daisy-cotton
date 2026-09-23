"""Template tags shared across daisy-cotton's own components."""

from django import template

register = template.Library()


@register.simple_tag
def responsive(var, klass):
    """Return a base class if ``var`` is True, a responsive variant if it is
    a breakpoint name.

    E.g. ``responsive(True, "divider-horizontal")`` -> ``"divider-horizontal"``
         ``responsive("md", "divider-horizontal")`` -> ``"md:divider-horizontal"``
    """
    if var is True:
        return klass
    elif isinstance(var, str) and var:
        return f"{var}:{klass}"

    return ""


@register.simple_tag
def variation(var, klass, allowed):
    """Return ``"{klass}-{var}"`` when ``var`` is one of ``allowed``.

    E.g. ``variation("sm", "btn", "sm,md,lg")`` -> ``"btn-sm"``
    """
    if isinstance(allowed, str):
        allowed = allowed.split(",")

    if var in allowed:
        return f"{klass}-{var}"

    return ""
