"""The package installs and exposes what a consuming project needs from it."""

from pathlib import Path

from django.apps import apps

import daisy_cotton


class TestPackagedApp:
    """What a host project gets after installing and adding it to INSTALLED_APPS."""

    def test_app_is_installed(self) -> None:
        assert apps.is_installed("daisy_cotton")

    def test_component_directory_is_where_cotton_looks_for_it(self) -> None:
        """Cotton resolves `<c-button>` to `cotton/button.html`.

        Components sit at the top of `cotton/` rather than under a directory
        of their own, so a tag reads `<c-button>` and not
        `<c-daisy-cotton.button>`. Moving them breaks every tag at once, and
        does so silently — a component Cotton cannot find renders as empty
        output rather than raising.
        """
        components = Path(daisy_cotton.__file__).parent / "templates" / "cotton"
        assert components.is_dir()
