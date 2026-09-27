"""Render-smoke test: every packaged Cotton component template must render.

Renders each template under daisy_cotton/templates/cotton/ directly with a
request context and permissive (mostly-empty) variables. This catches missing
{% load %} tags, references to non-existent subcomponents, and broken template
syntax — the failure modes that silently break components until a page uses
them.

It does NOT validate component attribute APIs; it is a floor, not a spec.
"""

import re
from pathlib import Path

import pytest
from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import RequestFactory

import daisy_cotton

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"

TEMPLATES = sorted(
    p.relative_to(COTTON_DIR).as_posix() for p in COTTON_DIR.rglob("*.html")
)


class TestComponentRenderSmoke:
    """Every packaged Cotton component template renders."""

    def test_inventory_is_nonempty(self):
        assert {"button.html", "card/index.html", "mockup/code/line.html"} <= set(
            TEMPLATES
        ), "cotton template discovery looks broken"

    @pytest.mark.django_db
    @pytest.mark.parametrize("relpath", TEMPLATES)
    def test_component_template_renders(self, relpath):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        # `name` satisfies c-icon, the one component whose only attribute is
        # genuinely required. Everything else must survive an empty context.
        render_to_string(f"cotton/{relpath}", {"name": "bi bi-house"}, request=request)


class TestActionComponentsShipNoScript:
    """SC-003: the action components render no script and no inline handler."""

    @pytest.mark.parametrize(
        "source",
        [
            '<c-button icon="x" text="Save" href="/a" disabled />',
            '<c-modal id="m" title="T" closable open><c-slot name="actions">A</c-slot>Body</c-modal>',
            '<c-dropdown text="Options" placement="top end">Menu</c-dropdown>',
            '<c-swap label="L" rotate checked><c-slot name="on">1</c-slot><c-slot name="off">0</c-slot>'
            '<c-slot name="indeterminate">?</c-slot></c-swap>',
            '<c-fab aria-label="A" flower><c-slot name="close">X</c-slot>'
            '<c-slot name="main_action">M</c-slot><c-button aria-label="B" /></c-fab>',
        ],
    )
    def test_no_script_and_no_on_attribute(self, cotton_render_string, source):
        html = cotton_render_string(source)
        assert "<script" not in html
        assert not re.search(r"\son[a-z]+=", html)
