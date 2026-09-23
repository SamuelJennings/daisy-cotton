from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DaisyCottonConfig(AppConfig):
    name = "daisy_cotton"
    label = "daisy_cotton"
    verbose_name = _("Daisy Cotton components")
