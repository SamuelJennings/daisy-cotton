"""The demo project is the component gallery alone.

Only what the server renders is asserted here. The preview-only scoping of
the injected assets, theme switching and its persistence, and alert
dismissal are browser behaviours that a test client cannot observe through
an isolated preview iframe — they are checked in the live walkthrough.
"""

from django.conf import settings
from django.test import Client
from django.urls import reverse


class TestRootRedirectsToGallery:
    """`/` has no page of its own; it hands the visitor to the gallery."""

    def test_root_redirects_to_gallery_index(self, client: Client) -> None:
        response = client.get("/")
        assert response.status_code == 302
        assert response.url == reverse("django_cotton_gallery:index")


class TestPreviewAssetsScopedToRawPage:
    """The raw page is where a lone component renders with its full stack."""

    def test_raw_page_includes_the_head_partial_script(self, client: Client) -> None:
        response = client.get(
            reverse("django_cotton_gallery:component_raw", args=["button"])
        )
        assert response.status_code == 200
        html = response.content.decode()
        # daisyUI's CDN files are stylesheets served with `nosniff`, so a
        # browser refuses them as scripts: they must arrive as <link> tags.
        assert (
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5">'
            in html
        )
        assert (
            '<link rel="stylesheet" '
            'href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css">' in html
        )
        assert '<script src="https://cdn.jsdelivr.net/npm/daisyui' not in html
        assert "cdn.jsdelivr.net/npm/@tailwindcss/browser@4" in html
        assert "cdn.jsdelivr.net/npm/alpinejs@3" in html
        # The theme bootstrap runs before paint so a saved theme applies
        # without a flash of the default theme.
        assert "data-theme" in html


class TestGalleryHasNoExtraCssOrJs:
    """The demo's assets arrive only through the head/body partials (D1)."""

    def test_no_extra_css_configured(self) -> None:
        assert not getattr(settings, "DJANGO_COTTON_GALLERY_EXTRA_CSS", ())

    def test_no_extra_js_configured(self) -> None:
        assert not getattr(settings, "DJANGO_COTTON_GALLERY_EXTRA_JS", ())


class TestNoHostPackageInstalled:
    """django-mvp and its chain are gone from the running project."""

    def test_mvp_not_installed(self) -> None:
        assert "mvp" not in settings.INSTALLED_APPS

    def test_flex_menu_not_installed(self) -> None:
        assert "flex_menu" not in settings.INSTALLED_APPS

    def test_easy_icons_not_installed(self) -> None:
        assert "easy_icons" not in settings.INSTALLED_APPS

    def test_crispy_forms_not_installed(self) -> None:
        assert "crispy_forms" not in settings.INSTALLED_APPS

    def test_crispy_tailwind_not_installed(self) -> None:
        assert "crispy_tailwind" not in settings.INSTALLED_APPS
