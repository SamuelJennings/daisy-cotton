"""``<c-mask>`` and ``<c-stack>``: a shaped image or container, and a pile of children."""

from html.parser import HTMLParser
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

COTTON = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"

SHAPES = [
    "circle",
    "decagon",
    "diamond",
    "heart",
    "hexagon",
    "hexagon-2",
    "pentagon",
    "squircle",
    "star",
    "star-2",
    "triangle",
    "triangle-2",
    "triangle-3",
    "triangle-4",
]
PLACEMENTS = ["top", "bottom", "start", "end"]


class _RootAttrs(HTMLParser):
    """Every attribute name on the first start tag, duplicates included."""

    def __init__(self):
        super().__init__()
        self.names = None

    def handle_starttag(self, tag, attrs):
        if self.names is None:
            self.names = [name for name, _ in attrs]


def root_attribute_names(html):
    parser = _RootAttrs()
    parser.feed(html)
    return parser.names


def mask(soup):
    return soup.find(class_="mask")


def stack(soup):
    return soup.find(class_="stack")


class TestMaskImage:
    def test_a_src_gives_an_img_with_the_shape_and_alt(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mask shape="squircle" src="me.jpg" alt="Profile photo" />'
        )

        img = mask(soup)
        assert img.name == "img"
        assert img["class"] == ["mask", "mask-squircle"]
        assert img["src"] == "me.jpg"
        assert img["alt"] == "Profile photo"

    @pytest.mark.parametrize("shape", SHAPES)
    def test_each_shape_gives_its_class(self, cotton_render_string_soup, shape):
        soup = cotton_render_string_soup(f'<c-mask shape="{shape}" src="me.jpg" />')

        assert mask(soup)["class"] == ["mask", f"mask-{shape}"]

    def test_a_src_without_alt_still_writes_an_empty_alt(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-mask shape="circle" src="me.jpg" />')

        assert mask(soup).has_attr("alt")
        assert mask(soup)["alt"] == ""

    @pytest.mark.parametrize("half", ["1", "2"])
    def test_half_gives_its_class(self, cotton_render_string_soup, half):
        soup = cotton_render_string_soup(
            f'<c-mask shape="squircle" half="{half}" src="me.jpg" />'
        )

        assert mask(soup)["class"] == ["mask", "mask-squircle", f"mask-half-{half}"]

    def test_class_is_merged_into_one_class_attribute(self, cotton_render_string):
        html = cotton_render_string(
            '<c-mask shape="star" src="me.jpg" class="w-24" data-x="1" />'
        )

        assert root_attribute_names(html).count("class") == 1
        assert "w-24" in html
        assert 'data-x="1"' in html


class TestMaskContainer:
    def test_no_src_gives_a_div_around_the_slot(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mask shape="hexagon"><span>Inside</span></c-mask>'
        )

        box = mask(soup)
        assert box.name == "div"
        assert box["class"] == ["mask", "mask-hexagon"]
        assert box.find("span").get_text() == "Inside"
        assert box.find("img") is None

    def test_a_div_has_no_src_or_alt(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-mask shape="heart">x</c-mask>')

        assert not mask(soup).has_attr("src")
        assert not mask(soup).has_attr("alt")


class TestMaskEdgeCases:
    def test_no_shape_gives_only_mask(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-mask src="me.jpg" />')

        assert mask(soup)["class"] == ["mask"]

    def test_an_unknown_shape_adds_nothing(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-mask shape="blob" src="me.jpg" />')

        assert mask(soup)["class"] == ["mask"]

    def test_an_unknown_half_adds_nothing(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mask shape="circle" half="3" src="me.jpg" />'
        )

        assert mask(soup)["class"] == ["mask", "mask-circle"]

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string('<c-mask shape="circle" src="me.jpg" />')

        assert "<script" not in html
        assert " on" not in html.replace("\n", " ").split(">")[0]

    def test_page_context_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-mask />",
            {"shape": "star", "half": "1", "src": "x.jpg", "alt": "Leaked"},
        )

        assert mask(soup).name == "div"
        assert mask(soup)["class"] == ["mask"]
        assert not mask(soup).has_attr("alt")


class TestStack:
    THREE = "<div>A</div><div>B</div><div>C</div>"

    def test_the_root_is_a_stack_with_all_children_visible(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(f"<c-stack>{self.THREE}</c-stack>")

        assert stack(soup)["class"] == ["stack"]
        children = stack(soup).find_all(recursive=False)
        assert [c.get_text() for c in children] == ["A", "B", "C"]
        assert not any(c.has_attr("aria-hidden") for c in children)
        assert not stack(soup).has_attr("aria-hidden")

    @pytest.mark.parametrize("placement", PLACEMENTS)
    def test_placement_gives_its_class(self, cotton_render_string_soup, placement):
        soup = cotton_render_string_soup(
            f'<c-stack placement="{placement}">{self.THREE}</c-stack>'
        )

        assert stack(soup)["class"] == ["stack", f"stack-{placement}"]

    def test_an_unknown_placement_adds_nothing(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-stack placement="left" />')

        assert stack(soup)["class"] == ["stack"]

    def test_class_is_merged_into_one_class_attribute(self, cotton_render_string):
        html = cotton_render_string('<c-stack class="w-24" data-x="1" />')

        assert root_attribute_names(html).count("class") == 1
        assert "w-24" in html
        assert 'data-x="1"' in html

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string(f"<c-stack>{self.THREE}</c-stack>")

        assert "<script" not in html
        assert " on" not in html.replace("\n", " ").split(">")[0]

    def test_page_context_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-stack />", {"placement": "top"})

        assert stack(soup)["class"] == ["stack"]


class TestMaskAnnotations:
    @pytest.fixture
    def parsed(self):
        return AnnotationParser().parse((COTTON / "mask.html").read_text())

    def test_shape_is_required_and_offers_the_fourteen_shapes(self, parsed):
        prop = next(p for p in parsed.props if p.clean_name == "shape")

        assert prop.required
        assert not prop.default
        assert prop.type == "select"
        assert list(prop.options) == SHAPES

    def test_half_offers_one_and_two(self, parsed):
        prop = next(p for p in parsed.props if p.clean_name == "half")

        assert prop.type == "select"
        assert list(prop.options) == ["1", "2"]

    def test_src_alt_and_class_are_documented(self, parsed):
        assert {"src", "alt", "class"} <= {p.clean_name for p in parsed.props}

    def test_the_default_slot_is_an_image_with_alt_text(self, parsed):
        assert len(parsed.slots) == 1
        content = parsed.slots[0].content
        assert "<img" in content
        assert 'alt="' in content
        assert 'alt=""' not in content


class TestStackAnnotations:
    @pytest.fixture
    def parsed(self):
        return AnnotationParser().parse((COTTON / "stack.html").read_text())

    def test_placement_offers_the_four_sides(self, parsed):
        prop = next(p for p in parsed.props if p.clean_name == "placement")

        assert prop.type == "select"
        assert list(prop.options) == PLACEMENTS

    def test_class_is_documented(self, parsed):
        assert "class" in {p.clean_name for p in parsed.props}

    def test_the_default_slot_holds_three_cards(self, parsed):
        assert len(parsed.slots) == 1
        assert parsed.slots[0].content.count("card") >= 3
