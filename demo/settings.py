"""Settings for the demo project.

Demonstration target, never deployed. It runs on the development server so
components can be looked at in a browser while they are being built.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-demo-project-only"

DEBUG = True

# The development server is reached over the network by hostname, not only at
# localhost. DEBUG auto-allows localhost and nothing else, so a bare list here
# answers any other hostname with 400 Bad Request.
ALLOWED_HOSTS = ["*"]

# The development server speaks plain HTTP. A cookie marked Secure is discarded
# by the browser, which leaves GET pages rendering perfectly while every form
# post comes back 403.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Order matters twice over. "demo" sits above "mvp" so the demo's own templates
# win against the shell's, and "mvp" sits above "crispy_tailwind" so its
# help-text override wins against crispy's.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Above "demo" for the gallery's benefit, not for template resolution. The
    # gallery scans exactly one cotton/ directory: the first template root
    # that has one, in this order. Below "demo" it would index the demo's own
    # scaffolding components and never see the package's own.
    "daisy_cotton",
    "demo",
    "django_cotton",
    # Development only, and a dev dependency for that reason: the gallery
    # serves component source code, so urls.py mounts it under DEBUG alone.
    "django_cotton_gallery",
    # Reloads the browser on a change to a template, a stylesheet or Python.
    # It arrives with the shared development bundle rather than a pin of its
    # own, and its middleware removes itself from the chain unless DEBUG is on.
    "django_browser_reload",
    "easy_icons",
    "flex_menu",
    "mvp",
    "crispy_forms",
    "crispy_tailwind",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Last, because it rewrites the response body to insert its script tag and
    # anything that encodes or compresses the body has to run after it.
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "demo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mvp.context_processors.mvp_config",
            ],
        },
    },
]

WSGI_APPLICATION = "demo.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "demo.sqlite3",
    }
}

CRISPY_ALLOWED_TEMPLATE_PACKS = ["tailwind"]
CRISPY_TEMPLATE_PACK = "tailwind"

FLEX_MENUS = {
    "renderers": {
        "sidebar": "mvp.renderers.SidebarRenderer",
        "dock": "mvp.renderers.MobileFooterNavRenderer",
    }
}

EASY_ICONS = {
    "default": {
        "renderer": "easy_icons.renderers.ProviderRenderer",
        "config": {"tag": "i"},
        "packs": ["mvp.utils.BS5_ICONS"],
        "icons": {
            "home": "bi bi-house",
            "component": "bi bi-square",
            "gallery": "bi bi-grid-3x3-gap",
        },
    }
}

# The theme menu is the point of the demo shell, not decoration. A component
# is supposed to take its colours from whatever theme the project runs, and
# the only way to see whether that is true is to change the theme and watch.
# These are daisyUI's own themes, deliberately spanning light, dark and
# heavily tinted, because a component that only looks right on two of them is
# not finished.
MVP_CONFIG = {
    "theme": {
        "default": "light",
        "choices": [
            "light",
            "dark",
            "cupcake",
            "emerald",
            "corporate",
            "synthwave",
            "dracula",
            "business",
            "night",
            "winter",
        ],
    },
    "layout": {
        "sidebar": {
            "title": "daisy-cotton",
            "breakpoint": "lg",
            "collapse": "icons",
        },
        "navbar": {"desktop": {"end": ["actions.theme-controller"]}},
    },
}

STATIC_URL = "/static/"

USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = "en-us"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
