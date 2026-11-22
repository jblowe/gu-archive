#!/usr/bin/env python3
"""
build_pages.py -- build the GU archive site.

Each nav item is its own page. The content of every page lives in
pages/<slug>.html (plain HTML, edit by hand); this script wraps each one in
template.html and writes it to <site_dir>. The first page (About) becomes
index.html; the others become <slug>.html.

The table rows come from items.csv (tab-delimited, with a header row; see
ITEM_COLUMNS) and replace {{ITEMS}} wherever it appears in a page. They are
plain HTML; assets/items.js adds search and pagination in the browser.
assets/ (logos, items.js) is copied alongside.

Template placeholders:
    {{PAGE_TITLE}}  text for <title>      {{TITLE}}    site title
    {{NAV}}         the nav bar links     {{CONTENT}}  the page's own HTML

Usage:
    python3 build_pages.py [site_dir]        (default: site)
"""

import argparse
import csv
import html
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template.html")
PAGES_DIR = os.path.join(HERE, "pages")
ASSETS = os.path.join(HERE, "assets")          # copied to <site_dir>/assets
ITEMS = os.path.join(HERE, "items.csv")
TITLE = "GU Department of Linguistics Language Repository"

# (slug, nav label) in nav order; the first is the home page (index.html)
PAGES = [
    ("about", "About"),
    ("collections", "Collections"),
    ("contribute", "Contribute"),
    ("contact", "Contact"),
]

ITEM_COLUMNS = ["title", "language", "type", "creator", "date", "duration",
                "description", "url", "media"]

ROW = """\
        <tr data-lang="{language}" data-type="{type}" data-text="{text}">
          <td><a href="{url}" target="_blank" rel="noopener">{title}</a></td>
          <td>{language}</td>
          <td>{type}</td>
          <td>{creator}</td>
          <td class="text-nowrap">{date}</td>
          <td>{play}</td>
        </tr>"""

AUDIO = """\
<div class="d-flex align-items-center gap-2">
            <audio controls preload="none" class="flex-grow-1" style="min-width: 250px" src="{media}"></audio>
            <span class="small text-nowrap">{duration}</span>
          </div>"""


def read_items(path):
    """Return a list of dicts from a tab-delimited file with a header row."""
    with open(path, encoding="utf-8", newline="") as fh:
        return [r for r in csv.DictReader(fh, delimiter="\t") if r.get("title")]


def item_row(item):
    e = {k: html.escape(item.get(k, ""), quote=True) for k in ITEM_COLUMNS}
    if item["type"] == "Sound" and item["media"]:
        e["play"] = AUDIO.format(**e)
    elif item["type"] == "Video" and item["media"]:
        d = f' <span class="small">({e["duration"]})</span>' if e["duration"] else ""
        e["play"] = f'<a href="{e["media"]}" target="_blank" rel="noopener">Watch video</a>{d}'
    else:
        e["play"] = f'<a href="{e["url"]}" target="_blank" rel="noopener">View</a>'
    text = " ".join(item.get(k, "") for k in ("title", "language", "type", "creator", "date", "description"))
    e["text"] = html.escape(text.lower(), quote=True)
    return ROW.format(**e)


def filename(i, slug):
    return "index.html" if i == 0 else f"{slug}.html"


def nav_items(active):
    items = []
    for i, (slug, label) in enumerate(PAGES):
        cur = ' active" aria-current="page' if slug == active else ""
        items.append(f'<li class="nav-item"><a class="nav-link{cur}" '
                     f'href="{filename(i, slug)}">{html.escape(label)}</a></li>')
    return "\n        ".join(items)


def build(out_dir):
    with open(TEMPLATE, encoding="utf-8") as fh:
        template = fh.read()
    items = read_items(ITEMS)
    rows = "\n".join(item_row(i) for i in items) \
        or '        <tr><td colspan="6">No items yet.</td></tr>'

    os.makedirs(out_dir, exist_ok=True)
    shutil.copytree(ASSETS, os.path.join(out_dir, "assets"), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".DS_Store"))

    for i, (slug, label) in enumerate(PAGES):
        with open(os.path.join(PAGES_DIR, f"{slug}.html"), encoding="utf-8") as fh:
            content = fh.read().replace("{{ITEMS}}", rows)
        page_title = TITLE if i == 0 else f"{label} – {TITLE}"
        page = (template
                .replace("{{PAGE_TITLE}}", html.escape(page_title))
                .replace("{{TITLE}}", html.escape(TITLE))
                .replace("{{NAV}}", nav_items(slug))
                .replace("{{CONTENT}}", content))
        with open(os.path.join(out_dir, filename(i, slug)), "w", encoding="utf-8") as fh:
            fh.write(page)
    print(f"built {len(PAGES)} pages in {out_dir} ({len(items)} item(s))")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Build the GU archive site.")
    p.add_argument("site_dir", nargs="?", default=os.path.join(HERE, "site"))
    build(p.parse_args().site_dir)
