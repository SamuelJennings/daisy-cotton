"""Tests for <c-avatar> and <c-avatar.group>: daisyUI's avatar markup — a
photo, initials, or a silhouette when neither is given, with an optional
online/offline indicator, and a group that overlaps several avatars.

The silhouette is a placeholder too (D4): with no ``src`` the root always
carries ``avatar-placeholder`` and the frame takes the neutral placeholder
colours, whether the frame shows initials or the silhouette.
"""

from html.parser import HTMLParser


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser — which is what a duplicate
    ``class`` attribute needs to be caught.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _attrs_on(html, tag):
    """The raw ``(name, value)`` attribute list of the first ``<tag ...>`` open tag."""
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return parser.attrs


def _attr_value(attrs, name):
    """The value of the first attribute named ``name``, or ``None`` if absent."""
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


def _class_attrs_on(html, tag):
    """Every ``class="..."`` value found on the first ``<tag ...>`` open tag."""
    return [
        name_value[1] for name_value in _attrs_on(html, tag) if name_value[0] == "class"
    ]


class TestAvatarRoot:
    """FR-021, AS1: a root carrying ``avatar``, an image frame, and an
    ``<img>`` with the given source and alt text."""

    def test_root_carries_avatar_and_image_renders_in_the_frame(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-avatar src="/p.jpg" alt="Ada Lovelace" />')

        root = soup.find("div", class_="avatar")
        assert root is not None

        img = root.find("img")
        assert img is not None
        assert img.get("src") == "/p.jpg"
        assert img.get("alt") == "Ada Lovelace"

    def test_avatar_with_src_carries_no_avatar_placeholder(self, cotton_render_string):
        html = cotton_render_string('<c-avatar src="/p.jpg" alt="Ada" />')

        root_classes = _class_attrs_on(html, "div")
        assert "avatar-placeholder" not in root_classes[0]


class TestAvatarAltDefault:
    """FR-022, AS2: ``alt`` defaults to empty."""

    def test_src_with_no_alt_renders_empty_alt(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-avatar src="/p.jpg" />')

        img = soup.find("img")
        assert img is not None
        assert img.get("alt") == ""


class TestAvatarPlaceholder:
    """FR-021, AS3: given ``placeholder`` and no ``src``, the root carries
    ``avatar-placeholder`` and the frame shows the placeholder text."""

    def test_placeholder_text_renders_with_avatar_placeholder_on_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-avatar placeholder="AL" />')

        root = soup.find("div", class_="avatar")
        assert root is not None
        assert "avatar-placeholder" in root.get("class")

        span = root.find("span")
        assert span is not None
        assert span.get_text(strip=True) == "AL"
        assert root.find("img") is None
        assert root.find("svg") is None


class TestAvatarSilhouette:
    """FR-021, AS4: given neither ``src`` nor ``placeholder``, the frame
    shows a silhouette hidden from assistive technology."""

    def test_silhouette_renders_hidden_from_assistive_technology(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-avatar />")

        root = soup.find("div", class_="avatar")
        assert root is not None
        assert "avatar-placeholder" in root.get("class")

        svg = root.find("svg")
        assert svg is not None
        assert svg.get("aria-hidden") == "true"
        assert svg.get("focusable") == "false"
        assert root.find("img") is None
        assert root.find("span") is None


class TestAvatarOnlineOffline:
    """FR-022, AS5: ``online``/``offline`` map to ``avatar-online``/``avatar-offline``."""

    def test_online_adds_avatar_online(self, cotton_render_string):
        html = cotton_render_string('<c-avatar src="/p.jpg" online />')
        assert "avatar-online" in _class_attrs_on(html, "div")[0]

    def test_offline_adds_avatar_offline(self, cotton_render_string):
        html = cotton_render_string('<c-avatar src="/p.jpg" offline />')
        assert "avatar-offline" in _class_attrs_on(html, "div")[0]


class TestAvatarFrameContentClass:
    """FR-023, AS6: the frame defaults to ``w-12 rounded-full``, plus
    ``bg-neutral text-neutral-content`` with no ``src``; ``content_class``
    replaces those defaults entirely."""

    def test_frame_defaults_with_src(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-avatar src="/p.jpg" />')

        frame = soup.find("div", class_="avatar").find("div", recursive=False)
        classes = frame.get("class")
        assert "w-12" in classes
        assert "rounded-full" in classes
        assert "bg-neutral" not in classes
        assert "text-neutral-content" not in classes

    def test_frame_defaults_with_no_src_add_placeholder_colours(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-avatar placeholder="AL" />')

        frame = soup.find("div", class_="avatar").find("div", recursive=False)
        classes = frame.get("class")
        for token in ("w-12", "rounded-full", "bg-neutral", "text-neutral-content"):
            assert token in classes

    def test_silhouette_frame_also_gets_placeholder_colours(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-avatar />")

        frame = soup.find("div", class_="avatar").find("div", recursive=False)
        classes = frame.get("class")
        assert "bg-neutral" in classes
        assert "text-neutral-content" in classes

    def test_content_class_replaces_the_defaults(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-avatar src="/p.jpg" content_class="w-24 rounded-xl" />'
        )

        frame = soup.find("div", class_="avatar").find("div", recursive=False)
        classes = frame.get("class")
        assert "w-24" in classes
        assert "rounded-xl" in classes
        assert "w-12" not in classes
        assert "rounded-full" not in classes

    def test_content_class_replaces_the_placeholder_defaults_too(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-avatar placeholder="AL" content_class="w-24 rounded-xl" />'
        )

        frame = soup.find("div", class_="avatar").find("div", recursive=False)
        classes = frame.get("class")
        assert "w-24" in classes
        assert "rounded-xl" in classes
        assert "bg-neutral" not in classes
        assert "text-neutral-content" not in classes


class TestAvatarClassAndAttrs:
    """``class`` merges into the root's single class list, and other
    attributes reach the root."""

    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-avatar src="/p.jpg" class="ring ring-primary" data-test="x" />'
        )

        root_classes = _class_attrs_on(html, "div")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "avatar" in root_classes[0]
        assert "ring" in root_classes[0]
        assert "ring-primary" in root_classes[0]

        attrs = _attrs_on(html, "div")
        assert _attr_value(attrs, "data-test") == "x"


class TestAvatarPageContextDoesNotLeak:
    """A page variable sharing a declared name never fills an empty avatar."""

    def test_page_context_src_alt_and_placeholder_do_not_leak_in(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-avatar />",
            context={
                "src": "/leaked.jpg",
                "alt": "Leaked",
                "placeholder": "LK",
            },
        )

        root = soup.find("div", class_="avatar")
        assert root is not None
        assert root.find("img") is None
        assert root.find("span") is None

        svg = root.find("svg")
        assert svg is not None
