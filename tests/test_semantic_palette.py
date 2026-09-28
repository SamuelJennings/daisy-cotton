"""No component template names a literal colour (Article XII).

A literal Tailwind shade (``bg-neutral-900``), ``white``/``black`` or a hex
value ignores the project's active daisyUI theme. The check reads every
template's source, gallery examples included, since an example is markup a
reader copies. The pixels of an image a gallery example embeds, such as an
inline SVG placeholder, are that image's own and out of scope.
"""

import re
from pathlib import Path

import pytest

import daisy_cotton

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"

TEMPLATES = sorted(
    p.relative_to(COTTON_DIR).as_posix() for p in COTTON_DIR.rglob("*.html")
)

UTILITIES = (
    "bg|text|border|ring|outline|fill|stroke|from|via|to|divide|shadow|"
    "accent|caret|decoration|placeholder"
)
PALETTE = (
    "slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|"
    "teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose"
)
LITERAL_COLOUR = re.compile(
    rf"(?<![\w-])(?:[\w-]+:)*(?:{UTILITIES})-(?:(?:{PALETTE})-\d{{2,3}}|white|black)\b"
    r"|#[0-9a-fA-F]{3,8}\b"
)


class TestSemanticPalette:
    def test_the_pattern_catches_a_literal_shade(self):
        assert LITERAL_COLOUR.search('class="text-white bg-neutral-900"')
        assert LITERAL_COLOUR.search('class="hover:bg-red-500"')
        assert LITERAL_COLOUR.search('style="color: #ff0000"')

    def test_the_pattern_allows_semantic_roles(self):
        assert not LITERAL_COLOUR.search(
            'class="bg-base-100 text-base-content btn-neutral divider-primary"'
        )

    @pytest.mark.parametrize("relpath", TEMPLATES)
    def test_template_uses_only_semantic_colours(self, relpath):
        source = (COTTON_DIR / relpath).read_text()

        assert LITERAL_COLOUR.findall(source) == []
