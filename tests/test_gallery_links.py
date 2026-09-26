"""Every link the gallery sidebar renders opens its component's page.

Cases come from the sidebar itself — collected once from the rendered gallery
index — so a component added later is covered without editing this file. A
folder component (``<name>/index.html`` exists, ``<name>.html`` does not) is
skipped while the installed gallery still 404s it: the gallery's catalog
scanner lists it under its folder name but its detail view looks only for
``<name>.html`` and never falls back to ``<name>/index.html`` the way Cotton
does (specs/001-gallery-demo/decisions.md). The skip reason names this
repository's tracking issue rather than asserting the failure, so a case that
starts passing once a fixed gallery release lands is not skipped.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.test import Client
from django.urls import reverse

import daisy_cotton

FOLDER_COMPONENT_ISSUE = "https://github.com/SamuelJennings/daisy-cotton/issues/96"

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"


def _is_folder_component(component_path: str) -> bool:
    """True when Cotton would resolve ``component_path`` to ``<path>/index.html``.

    Mirrors Cotton's own resolution order: a flat ``<path>.html`` wins when
    both exist (Edge Cases, spec.md) — no such component exists today, so
    the two are mutually exclusive in practice.
    """
    return (
        not (COTTON_DIR / f"{component_path}.html").is_file()
        and (COTTON_DIR / component_path / "index.html").is_file()
    )


def _collect_sidebar_links() -> list[tuple[str, str]]:
    """(component_path, href) for every component link the sidebar renders.

    Collected from the rendered gallery index rather than the catalog
    scanner directly, so this test exercises what a visitor actually gets:
    a link the sidebar never renders can't be covered here, and a link it
    does render is checked against the page it actually points to.
    """
    client = Client()
    response = client.get(reverse("django_cotton_gallery:index"))
    soup = BeautifulSoup(response.content.decode(), "html.parser")
    links = []
    prefix = "/django-cotton-gallery/"
    for anchor in soup.select("a[data-cg-component]"):
        href = anchor["href"]
        assert href.startswith(prefix) and href.endswith("/")
        component_path = href[len(prefix) : -1]
        links.append((component_path, href))
    return links


SIDEBAR_LINKS = _collect_sidebar_links()


class TestGallerySidebarLinks:
    """Every sidebar link opens its component, or is skipped with a reason."""

    def test_sidebar_renders_at_least_one_component_link(self) -> None:
        # An empty collection would make every parametrized case below
        # vacuously "pass" by never running — that must fail loudly instead.
        assert SIDEBAR_LINKS, "the gallery sidebar rendered no component links"

    @pytest.mark.parametrize(
        "component_path,href", SIDEBAR_LINKS, ids=[path for path, _ in SIDEBAR_LINKS]
    )
    def test_sidebar_link_opens_its_component(self, component_path, href) -> None:
        if _is_folder_component(component_path):
            client = Client()
            response = client.get(href)
            if response.status_code != 200:
                pytest.skip(
                    f"{component_path}: gallery index-file defect, "
                    f"see {FOLDER_COMPONENT_ISSUE}"
                )
            # A gallery release that fixed the defect: fall through to the
            # same assertion every other case gets, so this case starts
            # passing rather than staying skipped.

        client = Client()
        response = client.get(href)
        assert response.status_code == 200
        assert component_path.rsplit("/", 1)[-1] in response.content.decode()
