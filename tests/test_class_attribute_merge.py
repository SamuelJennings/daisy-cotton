"""Regression tests for issue #121 (django-mvp): components that hardcode a
literal ``class="..."`` on their root element *and* also spread ``{{ attrs }}``
on that same element must declare ``class`` as a ``<c-vars>`` variable and
merge it into the hardcoded string.

Without that, an undeclared ``class`` passed by the caller is not stripped
from ``{{ attrs }}`` by Cotton, so the element ends up with **two**
``class="..."`` attributes. Per the HTML spec a duplicate attribute is
ignored and the browser keeps only the first, so the caller's classes are
silently dropped with no error.

Sources are compiled through the Cotton compiler so the tests exercise each
component exactly as a template invocation would — rendering the component's
own template file directly, as ``test_render_all.py`` does, never triggers
Cotton's c-vars / ``attrs`` extraction and would not reproduce this bug.
"""

from html.parser import HTMLParser

from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first `<tag>` start tag.

    A regex over `[^>]*` is not safe here: some components embed Alpine.js
    expressions (e.g. `x-init="... => ..."`) with a literal `>` inside a
    quoted attribute value, which truncates a naive regex match before the
    real end of the opening tag. HTMLParser respects quoting, so it finds
    the tag's true boundary and — unlike a browser — reports every
    occurrence of a repeated attribute rather than silently dropping it,
    which is exactly what this bug needs to be caught.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def class_attrs_on(html, tag):
    """Every ``class="..."`` value found on the first ``<tag ...>`` open tag."""
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return [value for name, value in parser.attrs if name == "class"]


class TestClassAttributeMerge:
    """A caller-supplied ``class`` merges into the built-in classes instead
    of producing a second, browser-ignored ``class`` attribute."""

    def test_text_merges_caller_class(self):
        html = render('<c-text class="dac-prose">hi</c-text>')
        attrs = class_attrs_on(html, "p")
        assert len(attrs) == 1, f"expected one class attribute, found {attrs}"
        assert "dac-prose" in attrs[0]
        assert "text-base" in attrs[0]

    def test_divider_merges_caller_class(self):
        html = render('<c-divider class="my-8">Order lines</c-divider>')
        attrs = class_attrs_on(html, "div")
        assert len(attrs) == 1, f"expected one class attribute, found {attrs}"
        assert "my-8" in attrs[0]
        assert "divider" in attrs[0]

    def test_dock_item_toggle_variant_merges_caller_class(self):
        html = render('<c-dock.item toggle="sidebar-toggle" class="my-dock-item" />')
        attrs = class_attrs_on(html, "label")
        assert len(attrs) == 1, f"expected one class attribute, found {attrs}"
        assert "my-dock-item" in attrs[0]

    def test_dock_item_href_variant_merges_caller_class(self):
        html = render('<c-dock.item href="/" class="my-dock-item" />')
        attrs = class_attrs_on(html, "a")
        assert len(attrs) == 1, f"expected one class attribute, found {attrs}"
        assert "my-dock-item" in attrs[0]

    def test_dock_item_button_variant_merges_caller_class(self):
        html = render('<c-dock.item class="my-dock-item" />')
        attrs = class_attrs_on(html, "button")
        assert len(attrs) == 1, f"expected one class attribute, found {attrs}"
        assert "my-dock-item" in attrs[0]
