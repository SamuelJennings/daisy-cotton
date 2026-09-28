"""Tests for the <c-chat> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestChatRoot:
    def test_root_carries_chat_and_default_placement_start(self, cotton_render_string):
        div = parse(cotton_render_string("<c-chat>Hello</c-chat>")).div
        assert div["class"] == ["chat", "chat-start"]

    def test_message_lands_in_chat_bubble(self, cotton_render_string):
        html = cotton_render_string("<c-chat>Hello</c-chat>")
        bubble = parse(html).find(class_="chat-bubble")
        assert bubble.get_text() == "Hello"

    def test_placement_end_maps_to_chat_end(self, cotton_render_string):
        div = parse(cotton_render_string('<c-chat placement="end">Hi</c-chat>')).div
        assert div["class"] == ["chat", "chat-end"]

    def test_unknown_placement_adds_no_placement_class(self, cotton_render_string):
        div = parse(cotton_render_string('<c-chat placement="middle">Hi</c-chat>')).div
        assert div["class"] == ["chat"]

    def test_class_and_data_id_land_on_the_root(self, cotton_render_string):
        div = parse(
            cotton_render_string('<c-chat class="mt-2" data-id="7">Hi</c-chat>')
        ).div
        assert "mt-2" in div["class"]
        assert div["data-id"] == "7"


class TestChatVariant:
    def test_variant_primary_maps_to_chat_bubble_primary(self, cotton_render_string):
        html = cotton_render_string('<c-chat variant="primary">Hi</c-chat>')
        bubble = parse(html).find(class_="chat-bubble")
        assert bubble["class"] == ["chat-bubble", "chat-bubble-primary"]

    def test_every_daisyui_colour_maps_to_its_bubble_class(self, cotton_render_string):
        for colour in (
            "neutral",
            "primary",
            "secondary",
            "accent",
            "info",
            "success",
            "warning",
            "error",
        ):
            html = cotton_render_string(f'<c-chat variant="{colour}">Hi</c-chat>')
            bubble = parse(html).find(class_="chat-bubble")
            assert bubble["class"] == ["chat-bubble", f"chat-bubble-{colour}"]

    def test_unknown_variant_adds_no_class(self, cotton_render_string):
        html = cotton_render_string('<c-chat variant="rainbow">Hi</c-chat>')
        bubble = parse(html).find(class_="chat-bubble")
        assert bubble["class"] == ["chat-bubble"]

    def test_no_variant_adds_no_class(self, cotton_render_string):
        html = cotton_render_string("<c-chat>Hi</c-chat>")
        bubble = parse(html).find(class_="chat-bubble")
        assert bubble["class"] == ["chat-bubble"]


class TestChatNamedSlots:
    def test_image_header_footer_render_in_their_own_elements(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            "<c-chat>"
            '<c-slot name="image"><b>Avatar</b></c-slot>'
            '<c-slot name="header">Sam</c-slot>'
            '<c-slot name="footer">Delivered</c-slot>'
            "Hi</c-chat>"
        )
        soup = parse(html)
        assert soup.find(class_="chat-image").b.get_text() == "Avatar"
        assert soup.find(class_="chat-header").get_text() == "Sam"
        assert soup.find(class_="chat-footer").get_text() == "Delivered"

    def test_a_slot_not_given_emits_no_element(self, cotton_render_string):
        html = cotton_render_string(
            '<c-chat><c-slot name="header">Sam</c-slot>Hi</c-chat>'
        )
        soup = parse(html)
        assert soup.find(class_="chat-image") is None
        assert soup.find(class_="chat-footer") is None

    def test_every_named_slot_empty_emits_only_root_and_bubble(
        self, cotton_render_string
    ):
        html = cotton_render_string("<c-chat>Hi</c-chat>")
        soup = parse(html)
        divs = soup.find_all("div")
        assert len(divs) == 2
        assert divs[0]["class"] == ["chat", "chat-start"]
        assert divs[1]["class"] == ["chat-bubble"]

    def test_avatar_in_image_slot_is_drawn_inside_chat_image(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            "<c-chat>"
            '<c-slot name="image"><c-avatar src="a.jpg" alt="Sam" /></c-slot>'
            "Hi</c-chat>"
        )
        soup = parse(html)
        chat_image = soup.find(class_="chat-image")
        assert chat_image["class"] == ["chat-image"]
        avatar = chat_image.find(class_="avatar")
        assert avatar is not None
        assert avatar.img["src"] == "a.jpg"


class TestChatPageContext:
    def test_page_image_header_footer_and_variant_do_not_leak(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            "<c-chat>Hi</c-chat>",
            {
                "image": "<b>Leaked</b>",
                "header": "Leaked",
                "footer": "Leaked",
                "variant": "error",
            },
        )
        soup = parse(html)
        assert soup.find(class_="chat-image") is None
        assert soup.find(class_="chat-header") is None
        assert soup.find(class_="chat-footer") is None
        bubble = soup.find(class_="chat-bubble")
        assert bubble["class"] == ["chat-bubble"]
