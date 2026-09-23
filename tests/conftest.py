"""Shared fixtures for the test suite."""

import pytest
from django.template import Context, Template
from django.test import RequestFactory
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def _beautiful_soup():
    """Return the BeautifulSoup class, or raise with install instructions.

    beautifulsoup4 is not a runtime dependency of this package, so importing
    it at module level would break collection if it were ever missing. Only
    the ``*_soup`` fixtures need it, and only when actually requested.
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise ImportError(
            "The *_soup fixtures need beautifulsoup4: pip install beautifulsoup4"
        ) from exc
    return BeautifulSoup


@pytest.fixture
def cotton_render_string():
    """Compile and render a Django template string containing Cotton markup.

    Usage:
        def test_something(cotton_render_string):
            html = cotton_render_string("<c-badge text='Hi' />")
            assert "Hi" in html
    """
    factory = RequestFactory()

    def _render(template_string, context=None):
        if context is None:
            context = {}
        request = context.get("request") or factory.get("/")
        context["request"] = request

        compiled_template = compiler.process(template_string)
        django_template = Template(compiled_template)
        django_context = Context(context)
        # Tags such as {% querystring %} read context.request, the attribute
        # a RequestContext sets, rather than the "request" context variable.
        django_context.request = request
        return django_template.render(django_context)

    return _render


@pytest.fixture
def cotton_render_string_soup(cotton_render_string):
    """Like ``cotton_render_string``, parsed with BeautifulSoup for DOM
    traversal instead of substring assertions.

    Usage:
        def test_something(cotton_render_string_soup):
            soup = cotton_render_string_soup("<c-badge text='Hi' />")
            assert soup.find("div").get_text() == "Hi"
    """

    def _render(template_string, context=None):
        html = cotton_render_string(template_string, context)
        return _beautiful_soup()(html, "html.parser")

    return _render
