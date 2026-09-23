from mvp.views import MVPTemplateView


class HomeView(MVPTemplateView):
    """What this package is, for somebody arriving at the demo cold."""

    template_name = "demo/home.html"
    page_title = "daisy-cotton"
    page_subtitle = "Base daisyUI-styled components for django-cotton"
