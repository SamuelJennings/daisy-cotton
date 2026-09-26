"""Every component carries the annotations the gallery's catalog reads.

The gallery builds a component's page from its ``{# @… #}`` annotations, and the
linter only checks ``@prop`` against ``<c-vars>``. Three other things it cannot
see are easy to get wrong and silent when they are: a component with no
``@description`` (or two) has no summary, a template that renders the default
slot with no ``@slot``, or with one the gallery reads no description from,
documents a slot nobody is told about, and a ``{#`` that
does not close on its own line is not a Django comment at all, so its text is
printed into the page. A prop that takes one of a fixed set of values and is
typed ``text`` shows a free-text box where the gallery could offer a dropdown
of the values that work.

The rules are read out of the template source, not a rendered page: a missing
annotation leaves nothing in the output to assert against. Named slots and
``@trigger`` are left to review; only these four things are checked.
"""

import re
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"

TEMPLATES = sorted(COTTON_DIR.rglob("*.html"))

INLINE_COMMENT = re.compile(r"\{#.*?#\}")
COMMENT_BLOCK = re.compile(r"\{%\s*comment\b.*?%\}.*?\{%\s*endcomment\s*%\}", re.DOTALL)
DESCRIPTION = re.compile(r"\{#\s*@description\b")
DEFAULT_SLOT_ANNOTATION = re.compile(r"\{#\s*@slot(?!:)")
DEFAULT_SLOT_EXPRESSION = re.compile(r"\{\{\s*slot\s*(?:\|[^}]*)?\}\}")

# Props whose value is always one of a fixed set of daisyUI modifier names.
FIXED_CHOICE_PROPS = frozenset({"variant", "align", "position", "placement"})


class AnnotationRules:
    """The four checks, each returning a list of problems (empty when it passes)."""

    @staticmethod
    def description_problems(source):
        found = len(DESCRIPTION.findall(source))
        if found == 1:
            return []
        return [f"expected exactly one @description, found {found}"]

    @staticmethod
    def renders_default_slot(source):
        """Whether ``{{ slot }}`` is read outside ``{# #}`` and ``{% comment %}``.

        Inline comments are blanked per line, the way Django's lexer reads them,
        so a ``{#`` left open cannot swallow the lines below it.
        """
        source = COMMENT_BLOCK.sub("", source)
        lines = (INLINE_COMMENT.sub("", line) for line in source.splitlines())
        return any(DEFAULT_SLOT_EXPRESSION.search(line) for line in lines)

    @classmethod
    def slot_problems(cls, source):
        if not cls.renders_default_slot(source):
            return []
        if not DEFAULT_SLOT_ANNOTATION.search(source):
            return ["renders {{ slot }} but has no default {# @slot #}"]
        slots = AnnotationParser().parse(source).slots
        if any(slot.name is None and slot.description for slot in slots):
            return []
        return [
            "default {# @slot #} has no description; write `{# @slot — description #}`"
        ]

    @staticmethod
    def choice_problems(source):
        """A fixed-choice prop is a ``select`` listing its values."""
        problems = []
        for prop in AnnotationParser().parse(source).props:
            if prop.clean_name not in FIXED_CHOICE_PROPS:
                continue
            if prop.type != "select" or not prop.options:
                problems.append(
                    f"@prop {prop.clean_name} takes a fixed set of values; "
                    "type it select['…'] listing them"
                )
        return problems

    @staticmethod
    def comment_problems(source):
        problems = []
        for number, line in enumerate(source.splitlines(), start=1):
            if "{#" in INLINE_COMMENT.sub("", line):
                problems.append(
                    f"line {number}: {{# does not close with #}} on the same line"
                )
        return problems


class TestAnnotationRules:
    """The four rules, proven against scratch sources."""

    def test_one_description_passes(self):
        source = "{# @description A thing. #}\n<div></div>\n"
        assert AnnotationRules.description_problems(source) == []

    def test_no_description_fails(self):
        problems = AnnotationRules.description_problems("<div></div>\n")
        assert problems == ["expected exactly one @description, found 0"]

    def test_two_descriptions_fail(self):
        source = "{# @description One. #}\n{# @description Two. #}\n"
        problems = AnnotationRules.description_problems(source)
        assert problems == ["expected exactly one @description, found 2"]

    def test_default_slot_rendered_without_annotation_fails(self):
        source = "{# @description A thing. #}\n<div>{{ slot }}</div>\n"
        problems = AnnotationRules.slot_problems(source)
        assert problems == ["renders {{ slot }} but has no default {# @slot #}"]

    def test_default_slot_rendered_with_annotation_passes(self):
        source = (
            "{# @description A. #}\n{# @slot — The body. #}\n<div>{{ slot }}</div>\n"
        )
        assert AnnotationRules.slot_problems(source) == []

    def test_default_slot_with_empty_description_fails(self):
        source = "{# @description A. #}\n{# @slot The body. #}\n<div>{{ slot }}</div>\n"
        problems = AnnotationRules.slot_problems(source)
        assert problems == [
            "default {# @slot #} has no description; write `{# @slot — description #}`"
        ]

    def test_default_slot_with_leading_dash_passes(self):
        source = (
            "{# @description A. #}\n{# @slot — The body. #}\n<div>{{ slot }}</div>\n"
        )
        assert AnnotationRules.slot_problems(source) == []

    def test_default_slot_with_sample_and_description_passes(self):
        source = (
            "{# @description A. #}\n{# @slot Hi — The body. #}\n<div>{{ slot }}</div>\n"
        )
        assert AnnotationRules.slot_problems(source) == []

    def test_named_slot_alone_does_not_satisfy_the_default_slot(self):
        source = "{# @slot:actions Buttons. #}\n<div>{{ slot }}</div>\n"
        assert AnnotationRules.slot_problems(source) != []

    def test_no_rendered_slot_needs_no_annotation(self):
        source = "{# @description A. #}\n<div>{{ title }}</div>\n"
        assert AnnotationRules.slot_problems(source) == []

    def test_slot_with_filter_counts_as_rendered(self):
        source = "{# @description A. #}\n<div>{{ slot|default:'x' }}</div>\n"
        assert AnnotationRules.slot_problems(source) != []

    @pytest.mark.parametrize(
        "expression", ["{{ slots }}", "{{ slot_x }}", "{{ my_slot }}"]
    )
    def test_similarly_named_variable_is_not_the_default_slot(self, expression):
        source = f"{{# @description A. #}}\n<div>{expression}</div>\n"
        assert AnnotationRules.slot_problems(source) == []

    def test_slot_only_inside_comment_block_does_not_count(self):
        source = "{% comment %}\n{{ slot }}\n{% endcomment %}\n<div></div>\n"
        assert AnnotationRules.slot_problems(source) == []

    def test_slot_only_inside_comment_block_with_note_does_not_count(self):
        source = '{% comment "why" %}\n{{ slot }}\n{% endcomment %}\n<div></div>\n'
        assert AnnotationRules.slot_problems(source) == []

    def test_slot_only_inside_inline_comment_does_not_count(self):
        source = "{# renders {{ slot }} later #}\n<div></div>\n"
        assert AnnotationRules.slot_problems(source) == []

    def test_slot_after_inline_comment_on_same_line_counts(self):
        source = "{# note #}<div>{{ slot }}</div>\n"
        assert AnnotationRules.slot_problems(source) != []

    def test_fixed_choice_prop_typed_select_passes(self):
        source = "{# @prop variant:select['primary','error'] #}\n"
        assert AnnotationRules.choice_problems(source) == []

    @pytest.mark.parametrize("name", sorted(FIXED_CHOICE_PROPS))
    def test_fixed_choice_prop_typed_text_fails(self, name):
        source = f'{{# @prop {name}:text | description:"x" #}}\n'
        assert AnnotationRules.choice_problems(source) == [
            f"@prop {name} takes a fixed set of values; type it select['…'] listing them"
        ]

    def test_select_without_options_fails(self):
        source = "{# @prop variant:select #}\n"
        assert AnnotationRules.choice_problems(source) != []

    def test_other_text_props_are_not_checked(self):
        source = '{# @prop href:text | description:"x" #}\n'
        assert AnnotationRules.choice_problems(source) == []

    def test_single_line_annotations_pass(self):
        source = "{# @description A. #}\n{# @prop a:text #}\n"
        assert AnnotationRules.comment_problems(source) == []

    def test_unclosed_comment_names_its_line(self):
        source = "{# @description A. #}\n{# @prop a:text\n | description:'x' #}\n"
        problems = AnnotationRules.comment_problems(source)
        assert problems == ["line 2: {# does not close with #} on the same line"]

    def test_second_comment_on_a_line_is_checked_too(self):
        source = "{# fine #} {# never closed\n"
        problems = AnnotationRules.comment_problems(source)
        assert problems == ["line 1: {# does not close with #} on the same line"]


def template_id(path):
    return path.relative_to(COTTON_DIR).as_posix()


@pytest.mark.parametrize("path", TEMPLATES, ids=template_id)
class TestPackageTemplateAnnotations:
    """Every template the package ships passes all four rules."""

    def test_has_exactly_one_description(self, path):
        problems = AnnotationRules.description_problems(path.read_text())
        assert not problems, f"{template_id(path)}: {problems}"

    def test_documents_the_default_slot_it_renders(self, path):
        problems = AnnotationRules.slot_problems(path.read_text())
        assert not problems, f"{template_id(path)}: {problems}"

    def test_fixed_choice_props_list_their_values(self, path):
        problems = AnnotationRules.choice_problems(path.read_text())
        assert not problems, f"{template_id(path)}: {problems}"

    def test_annotations_close_on_their_own_line(self, path):
        problems = AnnotationRules.comment_problems(path.read_text())
        assert not problems, f"{template_id(path)}: {problems}"


class TestPackageTemplates:
    """The templates the rules run over are not empty."""

    def test_templates_were_discovered(self):
        assert TEMPLATES, f"no templates found under {COTTON_DIR}"
