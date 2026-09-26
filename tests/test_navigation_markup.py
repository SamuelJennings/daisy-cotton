"""The navigation components carry no script of their own.

Submenus, radio tabs and megamenu panels open through native HTML — a
``<details>`` disclosure, radio inputs sharing a name, the ``popover``
attribute — and daisyUI's CSS. A ``<script>`` element or an inline event
handler in one of these templates would make that promise false for every
project that installs the package, and nothing in a rendered test would
notice, because the markup around it still looks right.

The rule is read out of the template source rather than a rendered page, so a
handler sitting in a branch no test happens to render is still caught.
Annotation comments are ignored: a gallery example may show how a project
wires its own script to a component.
"""

import re
from pathlib import Path

import pytest

import daisy_cotton

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"

NAVIGATION_TEMPLATES = [
    *sorted(
        path
        for group in ("breadcrumbs", "dock", "menu", "tabs", "steps", "megamenu")
        for path in (COTTON_DIR / group).glob("*.html")
    ),
    COTTON_DIR / "link.html",
    COTTON_DIR / "navbar.html",
]

INLINE_COMMENT = re.compile(r"\{#.*?#\}")
COMMENT_BLOCK = re.compile(r"\{%\s*comment\b.*?%\}.*?\{%\s*endcomment\s*%\}", re.DOTALL)
SCRIPT_ELEMENT = re.compile(r"<script\b", re.IGNORECASE)
EVENT_HANDLER = re.compile(r"(?<![\w-])(?:on[a-z]+|@[a-z][\w.:-]*|x-on:[\w.:-]+)\s*=")


class ScriptRules:
    """Where a template's markup, outside its comments, runs a script."""

    @staticmethod
    def markup(source):
        source = COMMENT_BLOCK.sub("", source)
        return "\n".join(INLINE_COMMENT.sub("", line) for line in source.splitlines())

    @classmethod
    def problems(cls, source):
        markup = cls.markup(source)
        found = []
        if SCRIPT_ELEMENT.search(markup):
            found.append("contains a <script> element")
        found += [
            f"inline event handler {match.group(0).rstrip('= ')!r}"
            for match in EVENT_HANDLER.finditer(markup)
        ]
        return found


class TestScriptRules:
    """The rule catches what it is for, and nothing else."""

    def test_script_element_is_a_problem(self):
        assert ScriptRules.problems("<ul><script>go()</script></ul>")

    def test_on_attribute_is_a_problem(self):
        assert ScriptRules.problems('<button onclick="go()">Go</button>')

    def test_alpine_handler_is_a_problem(self):
        assert ScriptRules.problems('<button @click="open = true">Go</button>')

    def test_handler_in_an_annotation_is_not_a_problem(self):
        source = '{# @trigger <button onclick="go()">Open</button> — how #}\n<ul></ul>'
        assert ScriptRules.problems(source) == []

    def test_plain_markup_is_not_a_problem(self):
        source = '<button type="button" popovertarget="m-1" data-one="x">Go</button>'
        assert ScriptRules.problems(source) == []


class TestNavigationTemplatesRunNoScript:
    """No template in the navigation group ships a script (SC-005)."""

    def test_the_group_is_all_here(self):
        names = {
            path.relative_to(COTTON_DIR).as_posix() for path in NAVIGATION_TEMPLATES
        }
        assert {
            "link.html",
            "navbar.html",
            "menu/index.html",
            "tabs/tab.html",
            "steps/step.html",
            "megamenu/item.html",
            "dock/item.html",
            "breadcrumbs/item.html",
        } <= names

    @pytest.mark.parametrize(
        "path",
        NAVIGATION_TEMPLATES,
        ids=[p.relative_to(COTTON_DIR).as_posix() for p in NAVIGATION_TEMPLATES],
    )
    def test_template_runs_no_script(self, path):
        assert ScriptRules.problems(path.read_text()) == []
