"""Tests for <c-skeleton>: a placeholder shape or placeholder text, hidden
from assistive technology unless it carries text.
"""


class TestSkeletonShape:
    def test_shape_renders_a_div_carrying_skeleton_and_its_classes_hidden(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-skeleton class="h-32 w-full" />')

        div = soup.find("div")
        assert div is not None
        assert "skeleton" in div["class"]
        assert "h-32" in div["class"]
        assert "w-full" in div["class"]
        assert div["aria-hidden"] == "true"

    def test_no_text_renders_the_default_slot_as_content(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-skeleton class="h-4 w-4 rounded-full"><span>Shape</span></c-skeleton>'
        )

        div = soup.find("div")
        assert div.get("aria-hidden") == "true"
        assert div.find("span") is not None


class TestSkeletonText:
    def test_text_as_a_string_adds_skeleton_text_and_renders_it_as_content(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-skeleton text="Loading data…" />')

        div = soup.find("div")
        assert "skeleton" in div["class"]
        assert "skeleton-text" in div["class"]
        assert div.get_text() == "Loading data…"
        assert div.get("aria-hidden") is None

    def test_bare_text_with_slot_content_renders_the_same_as_a_string(
        self, cotton_render_string_soup
    ):
        string_soup = cotton_render_string_soup('<c-skeleton text="Loading data…" />')
        bare_soup = cotton_render_string_soup(
            "<c-skeleton text>Loading data…</c-skeleton>"
        )

        assert sorted(bare_soup.div["class"]) == sorted(string_soup.div["class"])
        assert bare_soup.div.get_text() == string_soup.div.get_text()
        assert bare_soup.div.get("aria-hidden") == string_soup.div.get("aria-hidden")


class TestSkeletonClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-skeleton class="h-4" data-test="x" />')

        div = soup.div
        assert "h-4" in div["class"]
        assert "skeleton" in div["class"]
        assert div["data-test"] == "x"


class TestSkeletonPageContextDoesNotLeak:
    def test_page_context_does_not_leak_into_the_skeleton(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-skeleton />",
            context={"text": "Leaked"},
        )

        div = soup.div
        assert "skeleton-text" not in div["class"]
        assert div.get("aria-hidden") == "true"
        assert div.get_text() == ""
