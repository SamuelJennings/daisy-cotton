"""Regression tests for issue #180 — modal positioning bugs.

Two failure modes, both stemming from the same fixed-width/no-height styling
on the modal box:

1. ``position="top"``/``"bottom"`` modals were always given a ``max-w-*``
   cap (``w-11/12`` plus a size class), which overrode daisyUI's own
   ``.modal-top``/``.modal-bottom`` full-width rule — the dialog never spanned
   the screen.
2. ``position="start"``/``"end"`` modals get ``height: 100vh`` on the outer
   ``.modal-box`` wrapper from daisyUI, but the inner ``<c-card>`` (the
   visible surface, since the wrapper itself is transparent) had no height
   utility and stayed sized to its content — it never stretched to fill that
   height.

Sources are compiled through the Cotton compiler (mirroring
``test_breadcrumbs_href_attribute.py``), which is what exercises ``<c-vars>``
and ``attrs`` extraction the way a real template invocation would. Full-width
and full-height are ultimately live-layout properties, so
``tests/test_e2e/test_modal_positioning.py`` pairs this with a real-browser
bounding-box assertion; this module is the part of the guard that runs
everywhere.
"""

from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


class TestModalPositionWidth:
    """Top/bottom positioned modals must not be capped to a max-width."""

    def test_top_position_spans_full_width(self):
        html = render('<c-modal id="m" position="top">Body</c-modal>')
        assert "w-full" in html
        assert "max-w-none" in html
        assert "max-w-2xl" not in html
        assert "w-11/12" not in html

    def test_bottom_position_spans_full_width(self):
        html = render('<c-modal id="m" position="bottom">Body</c-modal>')
        assert "w-full" in html
        assert "max-w-none" in html
        assert "max-w-2xl" not in html
        assert "w-11/12" not in html

    def test_default_centred_position_keeps_the_size_cap(self):
        """No position set: the original centred-dialog sizing is unchanged."""
        html = render('<c-modal id="m">Body</c-modal>')
        assert "w-11/12" in html
        assert "max-w-2xl" in html

    def test_start_and_end_keep_the_size_cap(self):
        """Side panels still size by ``size``, only their height changes."""
        for position in ["start", "end"]:
            html = render(f'<c-modal id="m" position="{position}">Body</c-modal>')
            assert "w-11/12" in html
            assert "max-w-2xl" in html


class TestModalCardHeight:
    """The inner card must be able to stretch to the wrapper's full height."""

    def test_card_gets_full_height_utility(self):
        html = render('<c-modal id="m" position="start">Body</c-modal>')
        assert "h-full" in html


class TestModalCardContent:
    """Title, icon, actions, footer and footer_end forward into the inner card,
    adjusted to the card's new structure (plan "The modal", research R7)."""

    def test_title_and_icon_render_in_the_cards_title_heading(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-modal id="m" title="Confirm" icon="bi bi-info-circle">Body</c-modal>'
        )

        heading = soup.find("h2", class_="card-title")
        assert heading is not None
        assert heading.find("i", class_="bi bi-info-circle") is not None
        assert "Confirm" in heading.get_text()

    def test_icon_never_reaches_the_card_as_a_raw_attribute(self, cotton_render_string):
        html = cotton_render_string(
            '<c-modal id="m" icon="bi bi-info-circle">Body</c-modal>'
        )

        assert "icon=" not in html

    def test_a_title_only_modal_draws_no_empty_icon(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-modal id="m" title="Confirm">Body</c-modal>'
        )

        heading = soup.find("h2", class_="card-title")
        assert heading is not None
        assert heading.find("i") is None

    def test_footer_and_footer_end_render(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-modal id="m">'
            '<c-slot name="footer"><span>Left</span></c-slot>'
            '<c-slot name="footer_end"><span>Right</span></c-slot>'
            "Body</c-modal>"
        )

        assert soup.find("span", string="Left") is not None
        assert soup.find("span", string="Right") is not None

    def test_actions_render_in_card_actions(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-modal id="m"><c-slot name="actions"><button>Save</button></c-slot>Body</c-modal>'
        )

        actions = soup.find("div", class_="card-actions")
        assert actions is not None
        assert actions.find("button").get_text() == "Save"
