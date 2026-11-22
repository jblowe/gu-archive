#!/usr/bin/env python3
"""
build_pages.py -- build the GU archive site.

Each nav item is its own page. The content of every page lives in
pages/<slug>.html (plain HTML, edit by hand); this script wraps each one in
template.html and writes it to <site_dir>. The first page (About) becomes
index.html; the others become <slug>.html.

The jukebox rows come from tracks.csv (tab-delimited: title <TAB> url, with a
header row) and replace {{JUKEBOX}} wherever it appears in a page.
assets/ (logos) is copied alongside.

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
TRACKS = os.path.join(HERE, "tracks.csv")
TITLE = "GU Department of Linguistics Language Repository"

# (slug, nav label) in nav order; the first is the home page (index.html)
PAGES = [
    ("about", "About"),
    ("collections", "Collections"),
    ("contribute", "Contribute"),
    ("contact", "Contact"),
]

ROW = """\
      <tr>
        <td>{title}</td>
        <td>
          <div class="d-flex align-items-center gap-2">
            <audio controls preload="none" class="flex-grow-1" style="min-width: 250px" src="{url}"></audio>
            <a href="{url}" class="small text-nowrap">MP3</a>
          </div>
        </td>
      </tr>"""


def read_tracks(path):
    """Return [(title, url), ...] from a tab-delimited file with a header row."""
    with open(path, encoding="utf-8", newline="") as fh:
        rows = csv.reader(fh, delimiter="\t")
        next(rows, None)  # header
        return [(r[0].strip(), r[1].strip()) for r in rows
                if len(r) >= 2 and r[1].strip()]


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
    tracks = read_tracks(TRACKS)
    rows = "\n".join(
        ROW.format(title=html.escape(t), url=html.escape(u, quote=True))
        for t, u in tracks
    ) or '      <tr><td colspan="2">No recordings yet.</td></tr>'

    os.makedirs(out_dir, exist_ok=True)
    shutil.copytree(ASSETS, os.path.join(out_dir, "assets"), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".DS_Store"))

    for i, (slug, label) in enumerate(PAGES):
        with open(os.path.join(PAGES_DIR, f"{slug}.html"), encoding="utf-8") as fh:
            content = fh.read().replace("{{JUKEBOX}}", rows)
        page_title = TITLE if i == 0 else f"{label} – {TITLE}"
        page = (template
                .replace("{{PAGE_TITLE}}", html.escape(page_title))
                .replace("{{TITLE}}", html.escape(TITLE))
                .replace("{{NAV}}", nav_items(slug))
                .replace("{{CONTENT}}", content))
        with open(os.path.join(out_dir, filename(i, slug)), "w", encoding="utf-8") as fh:
            fh.write(page)
    print(f"built {len(PAGES)} pages in {out_dir} ({len(tracks)} track(s))")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Build the GU archive site.")
    p.add_argument("site_dir", nargs="?", default=os.path.join(HERE, "site"))
    build(p.parse_args().site_dir)
