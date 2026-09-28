"""App configuration for daisy-cotton."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DaisyCottonConfig(AppConfig):
    """Django app config for the daisy-cotton component library."""

    name = "daisy_cotton"
    label = "daisy_cotton"
    verbose_name = _("Daisy Cotton components")
