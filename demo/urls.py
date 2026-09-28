"""URL configuration for the demo project."""

from django.conf import settings
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # The demo serves the component gallery and nothing else: there is no
    # page of its own to land on, so the root URL hands the visitor straight
    # to the gallery's index.
    path(
        "",
        RedirectView.as_view(pattern_name="django_cotton_gallery:index"),
        name="home",
    ),
    path("__reload__/", include("django_browser_reload.urls")),
]

# DEBUG only: the gallery serves component source, so it is never a public route.
if settings.DEBUG:
    urlpatterns += [path("", include("django_cotton_gallery.urls"))]
