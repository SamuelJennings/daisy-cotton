"""Confirms <c-form.field> is gone with no alias or stub (FR-022)."""

import pytest
from django import template
from django.template.context import Context
from django.test import override_settings
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


class TestFormFieldRemoved:
    @override_settings(DEBUG=False)
    def test_rendering_raises_template_does_not_exist(self):
        with pytest.raises(template.TemplateDoesNotExist, match="form/field"):
            render("<c-form.field />")


class TestOldFlatInputNameRemoved:
    @override_settings(DEBUG=False)
    def test_rendering_raises_template_does_not_exist(self):
        with pytest.raises(template.TemplateDoesNotExist, match="input"):
            render("<c-input />")
