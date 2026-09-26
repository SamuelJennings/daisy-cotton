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
    # The endpoint an open page holds to hear that something on disk changed.
    path("__reload__/", include("django_browser_reload.urls")),
]

# The component gallery, under DEBUG only. It serves the source of every
# component it indexes, so it is a development tool and never a public route —
# which is also why it is a dev dependency rather than a runtime one. Its own
# routes are all under the /django-cotton-gallery/ prefix, so including it at
# the root adds nothing else.
if settings.DEBUG:
    urlpatterns += [path("", include("django_cotton_gallery.urls"))]
