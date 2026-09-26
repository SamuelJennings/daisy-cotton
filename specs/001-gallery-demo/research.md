# Research: Make the component gallery the whole demo

## How the gallery takes a project's assets

django-cotton-gallery 1.x offers two extension points and uses both in its interface page (`base.html`), in the preview iframe it builds from a `<template id="cg-frame-head">` copy of the same content (`isolated-stage.js`, same-origin `srcdoc`), and in the standalone `raw/` page:

- `DJANGO_COTTON_GALLERY_EXTRA_CSS` / `_EXTRA_JS`: URL lists.
- `django_cotton_gallery/_extra_head.html` and `_extra_body.html`: partials, included when a project supplies them.

**Decision**: supply the two partials from the demo app, and set neither URL list.

**Why**: the URL lists load into the gallery's interface page as well as the previews, and daisyUI's base styles would restyle the gallery's own chrome. A script in `_extra_head.html` can tell a preview document (inside the iframe, or a `raw/`, `preview/` or `thumb/` page) from the interface page and load daisyUI, Tailwind's browser build and Alpine into previews only.

## Theme switching across frames

The preview iframe is same-origin, so the interface page can reach `frame.contentDocument` and a `storage` event reaches it too.

**Decision**: `_extra_head.html` sets `data-theme` on a preview document from `localStorage` before first paint. `_extra_body.html` holds only a script, because the gallery copies it into every preview frame and the raw page too. The script builds a `<select>` of the ten themes when it runs in the interface page and does nothing elsewhere. A change stores the choice and sets `data-theme` on every iframe document on the page. Frames created later read the stored value when they load.

**Rejected**: a query-string theme. The gallery rebuilds its URLs and would drop it between pages.

## The index-file defect

Recorded in `decisions.md`. The sidebar lists `card/index.html` as `card` and links to `/django-cotton-gallery/card/`, and the detail view resolves only `card.html`. Six links return 404 today. The test reads the links from the rendered index page, so it follows whatever the sidebar lists.

**Tracking**: an issue in this repository, filed during implementation. Nothing is filed with the gallery project.

## Test settings

The test settings imported the demo's django-mvp configuration and removed the gallery from `INSTALLED_APPS` to keep its startup notice out of test output. The sidebar-link test needs the gallery installed and routed.

**Decision**: test settings keep borrowing the demo's app list, gallery included, and the gallery's startup notice is accepted in test output unless it turns out to be noisy, in which case it is silenced in the test settings rather than by removing the app.

## CDN pins

daisyUI 5 (`daisyui@5` and `daisyui@5/themes.css`), Tailwind's browser build 4 (`@tailwindcss/browser@4`) and Alpine 3 (`alpinejs@3`), each from jsDelivr and pinned to a major version. The demo is a development target. A minor release changing a preview is visible immediately and costs nothing.
