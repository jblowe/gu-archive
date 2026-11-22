# gu-archive

Website for the GU Department of Linguistics Language Repository: About,
Collections (a jukebox of remote MP3s), Contribute and Contact pages, published
on GitHub Pages at <https://jblowe.github.io/gu-archive/>.

## Files

- `template.html` – shared page shell (banner, nav bar, footer), styled after gauhati.ac.in
- `pages/*.html` – the content of each page; plain HTML, edit by hand
- `items.csv` – tab-delimited, one archive item per line (`title language type creator date duration description url media`); fills the searchable, paginated table on the Collections page. Currently a snapshot of the CoRSAL Boro (BLR) and Dimasa (DLR) collections.
- `assets/` – logos and `items.js` (table search/pagination), copied to `site/assets/`
- `build_pages.py` – wraps each page in the template and writes `site/` (Python 3, no dependencies). The nav order and labels are the `PAGES` list at the top.
- `deploy_pages.sh` – force-pushes `site/` to the `gh-pages` branch (needs `git` and `gh`)

## Usage

Edit a page in `pages/` or change `items.csv`, then:

```bash
python3 build_pages.py     # build site/
./deploy_pages.sh          # publish to GitHub Pages
```

To preview locally: `python3 -m http.server -d site 8000`

To add a page: create `pages/<slug>.html` and add `("<slug>", "Nav label")` to `PAGES` in `build_pages.py`.
