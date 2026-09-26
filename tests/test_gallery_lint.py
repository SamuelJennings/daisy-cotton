"""The gallery's own linter finds nothing to fix in the package's components.

The gallery documents each component from its ``{# @prop … #}`` annotations and
its linter checks them against ``<c-vars>``. That check used to be run by hand,
so annotations drifted from the templates without anyone being told. This suite
runs the same linter over the package's ``cotton/`` directory and fails on any
error or warning, so an undocumented or mis-documented component fails the
build. Hints are advice, not faults, and never block.

Only the gallery's pure modules are imported. The gallery app itself is not in
``INSTALLED_APPS``, so its start-up notice never prints during the suite.
"""

from pathlib import Path

import pytest
from django_cotton_gallery.core.catalog.scanner import scan
from django_cotton_gallery.core.linter import lint_catalog
from django_cotton_gallery.core.schemas import CatalogConfig

import daisy_cotton

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"

BLOCKING = ("error", "warning")


class GalleryLint:
    """Discover a cotton directory the gallery's way and lint it as one catalog."""

    @staticmethod
    def discover(cotton_dir):
        """``(component path, source)`` pairs, exactly as the gallery names them."""
        config = CatalogConfig(cotton_dir=cotton_dir)
        return [(component.path, component.source) for component in scan(config)]

    @classmethod
    def report(cls, cotton_dir):
        return lint_catalog(cls.discover(cotton_dir))

    @staticmethod
    def blocking(component_report):
        """Findings that fail the suite: errors and warnings, never hints."""
        return [i for i in component_report.issues if i.severity in BLOCKING]

    @staticmethod
    def describe(issue):
        return f"{issue.component_path} L{issue.line} {issue.rule}: {issue.message}"

    @classmethod
    def blocking_by_component(cls, report):
        return {c.path: cls.blocking(c) for c in report.components}


def write_catalog(tmp_path, sources):
    cotton_dir = tmp_path / "cotton"
    for name, source in sources.items():
        path = cotton_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
    return cotton_dir


class TestGalleryLintRules:
    """The check can fail: each blocking case is proven on a scratch catalog."""

    def test_undocumented_cvars_name_blocks_with_component_line_rule_and_message(
        self, tmp_path
    ):
        cotton_dir = write_catalog(
            tmp_path,
            {
                "thing.html": (
                    "{# @description A thing. #}\n"
                    '<c-vars size="md" />\n'
                    '<div class="{{ size }}"></div>\n'
                )
            },
        )

        found = GalleryLint.blocking_by_component(GalleryLint.report(cotton_dir))

        [issue] = found["thing"]
        assert issue.severity in BLOCKING
        assert issue.component_path == "thing"
        assert issue.line is not None
        assert issue.rule
        assert issue.message
        assert GalleryLint.describe(issue).startswith(f"thing L{issue.line} ")

    def test_call_to_component_outside_the_catalog_blocks(self, tmp_path):
        cotton_dir = write_catalog(
            tmp_path,
            {"thing.html": "{# @description A thing. #}\n<c-does-not-exist />\n"},
        )

        found = GalleryLint.blocking_by_component(GalleryLint.report(cotton_dir))

        assert [i.rule for i in found["thing"]] == ["unknown-component"]
        assert found["thing"][0].severity == "error"

    def test_call_to_component_inside_the_catalog_passes(self, tmp_path):
        cotton_dir = write_catalog(
            tmp_path,
            {
                "thing.html": "{# @description A thing. #}\n<c-other />\n",
                "other.html": "{# @description Another. #}\n<div></div>\n",
            },
        )

        found = GalleryLint.blocking_by_component(GalleryLint.report(cotton_dir))

        assert found == {"thing": [], "other": []}

    def test_hints_alone_never_block(self, tmp_path):
        cotton_dir = write_catalog(
            tmp_path,
            {
                "thing.html": (
                    "{# @description A thing. #}\n<div>{{ undeclared }}</div>\n"
                )
            },
        )

        report = GalleryLint.report(cotton_dir)

        assert report.total_hints > 0
        assert GalleryLint.blocking_by_component(report) == {"thing": []}

    def test_template_added_to_the_directory_is_discovered(self, tmp_path):
        cotton_dir = write_catalog(
            tmp_path, {"first.html": "{# @description One. #}\n<div></div>\n"}
        )
        before = {path for path, _ in GalleryLint.discover(cotton_dir)}

        write_catalog(
            tmp_path, {"nested/second.html": "{# @description Two. #}\n<p></p>\n"}
        )
        after = {path for path, _ in GalleryLint.discover(cotton_dir)}

        assert before == {"first"}
        assert after == {"first", "nested/second"}


# One lint over the whole catalog: `lint_component` on its own skips the
# unknown-component rule unless it is handed the catalog's known tags.
PACKAGE_FINDINGS = GalleryLint.blocking_by_component(GalleryLint.report(COTTON_DIR))


@pytest.mark.parametrize("component", sorted(PACKAGE_FINDINGS))
class TestPackageComponentsLintClean:
    """Every component the package ships has no errors or warnings."""

    def test_has_no_blocking_findings(self, component):
        findings = [GalleryLint.describe(i) for i in PACKAGE_FINDINGS[component]]
        assert not findings, "\n".join(findings)


class TestPackageCatalog:
    """The catalog the lint runs over is not empty."""

    def test_components_were_discovered(self):
        assert PACKAGE_FINDINGS, f"no components found under {COTTON_DIR}"
