"""Tests for the <c-card> component's outer surface.

The card's root element is the daisyUI ``.card`` surface itself: one element
carrying the surface classes, the caller's ``class`` and any further
attributes, with ``.card-body`` directly inside it.
"""

import re

from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


def root_tag(html):
    """The first opening tag in the rendered output."""
    return re.search(r"<[a-z][^>]*>", html).group(0)


class TestCardSurface:
    """The root element is the card surface, with body directly inside."""

    def test_root_carries_the_surface_classes(self):
        root = root_tag(render("<c-card>Body</c-card>"))
        assert root.startswith("<div")
        assert re.search(r'class="card bg-base-100 shadow-sm\s*"', root)

    def test_caller_class_joins_the_surface_classes(self):
        root = root_tag(render('<c-card class="w-96">Body</c-card>'))
        assert re.search(r'class="card bg-base-100 shadow-sm w-96"', root)
        assert root.count("class=") == 1

    def test_extra_attributes_reach_the_root(self):
        root = root_tag(render('<c-card id="summary">Body</c-card>'))
        assert 'id="summary"' in root

    def test_body_sits_directly_inside_the_surface(self):
        html = render("<c-card>Body</c-card>")
        assert re.match(r'\s*<div[^>]*>\s*<div class="card-body', html)
        assert html.count('class="card ') == 1
