"""``<c-mockup.code>`` and ``<c-mockup.code.line>``.

``<c-mockup.code.line>``'s prompt character is the ``prefix`` attribute, and a
line has no prefix unless the caller gives one: a caller asking for ``$``, ``>``
for a Windows shell or ``#`` for a root prompt writes it, and output lines
carry none. The line writes ``data-prefix`` only when there is a prefix.

``text`` is declared so the component's declaration describes the interface the
demo uses. Both components merge a caller's ``class`` into their root and pass
further attributes to it, and the code block is keyboard-focusable so a box
that overflows can be scrolled with the arrow keys.
"""

from html.parser import HTMLParser


class _RootAttrs(HTMLParser):
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


class TestCodeLinePrefix:
    def test_a_line_has_no_prefix_by_default(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code.line text="Successfully installed" />'
        )

        assert not soup.find("pre").has_attr("data-prefix")

    def test_a_caller_asks_for_a_shell_dollar(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code.line prefix="$" text="pip install requests" />'
        )

        assert soup.find("pre")["data-prefix"] == "$"

    def test_a_caller_chooses_the_prompt(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code.line prefix="#" text="apt install python3" />'
        )

        assert soup.find("pre")["data-prefix"] == "#"

    def test_the_prompt_can_be_emptied(self, cotton_render_string_soup):
        """Output lines in a terminal mockup carry no prompt at all."""
        soup = cotton_render_string_soup(
            '<c-mockup.code.line prefix="" text="Successfully installed" />'
        )

        assert not soup.find("pre").has_attr("data-prefix")

    def test_the_line_renders_its_text(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code.line text="python manage.py runserver" />'
        )

        assert soup.find("code").get_text() == "python manage.py runserver"

    def test_a_page_prefix_does_not_leak_into_the_line(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code.line text="Done" />', {"prefix": "#", "text": "Leaked"}
        )

        assert not soup.find("pre").has_attr("data-prefix")
        assert soup.find("code").get_text() == "Done"


class TestCodeLineRoot:
    def test_class_is_merged_into_the_pre(
        self, cotton_render_string, cotton_render_string_soup
    ):
        source = '<c-mockup.code.line class="text-success" text="ok" />'

        assert "text-success" in cotton_render_string_soup(source).find("pre")["class"]
        assert root_attribute_names(cotton_render_string(source)).count("class") == 1

    def test_an_extra_attribute_reaches_the_pre(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code.line id="first" data-x="1" text="ok" />'
        )

        assert soup.find("pre")["id"] == "first"
        assert soup.find("pre")["data-x"] == "1"


class TestCodeBlock:
    def test_the_block_is_keyboard_focusable(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-mockup.code>Hi</c-mockup.code>")

        assert soup.find("div")["tabindex"] == "0"

    def test_a_caller_tabindex_replaces_the_default_once(self, cotton_render_string):
        html = cotton_render_string(
            '<c-mockup.code tabindex="-1"><c-mockup.code.line text="ls" /></c-mockup.code>'
        )

        assert root_attribute_names(html).count("tabindex") == 1
        assert 'tabindex="-1"' in html

    def test_class_is_merged_into_the_root(
        self, cotton_render_string, cotton_render_string_soup
    ):
        source = '<c-mockup.code class="my-4">Hi</c-mockup.code>'

        assert {"mockup-code", "my-4"} <= set(
            cotton_render_string_soup(source).find("div")["class"]
        )
        assert root_attribute_names(cotton_render_string(source)).count("class") == 1

    def test_an_extra_attribute_reaches_the_root(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code id="term" data-x="1">Hi</c-mockup.code>'
        )

        assert soup.find("div")["id"] == "term"
        assert soup.find("div")["data-x"] == "1"

    def test_the_lines_are_rendered(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.code><c-mockup.code.line prefix="$" text="ls" />'
            '<c-mockup.code.line text="a.txt" /></c-mockup.code>'
        )

        assert [pre.get_text() for pre in soup.find_all("pre")] == ["ls", "a.txt"]
