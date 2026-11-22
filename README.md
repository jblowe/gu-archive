# gu-archive

Website for the GU Department of Linguistics Language Repository: About,
Collections (a jukebox of remote MP3s), Contribute and Contact pages, published
on GitHub Pages at <https://jblowe.github.io/gu-archive/>.

## Files

- `template.html` – shared page shell (banner, nav bar, footer), styled after gauhati.ac.in
- `pages/*.html` – the content of each page; plain HTML, edit by hand
- `tracks.csv` – tab-delimited, header row `title<TAB>media`, one recording per line; fills the jukebox on the Collections page
- `assets/` – logos (copied to `site/assets/`)
- `build_pages.py` – wraps each page in the template and writes `site/` (Python 3, no dependencies). The nav order and labels are the `PAGES` list at the top.
- `deploy_pages.sh` – force-pushes `site/` to the `gh-pages` branch (needs `git` and `gh`)

## Usage

Edit a page in `pages/` or add a line to `tracks.csv`, then:

```bash
python3 build_pages.py     # build site/
./deploy_pages.sh          # publish to GitHub Pages
```

To preview locally: `python3 -m http.server -d site 8000`

To add a page: create `pages/<slug>.html` and add `("<slug>", "Nav label")` to `PAGES` in `build_pages.py`.
