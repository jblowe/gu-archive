// Search, filter and paginate the items table on the Collections page.
// The rows are plain HTML in the page (so it works without JS); this only hides/shows them.
(function () {
  var rows = Array.prototype.slice.call(document.querySelectorAll("#items tbody tr"));
  if (!rows.length) return;
  var q = document.getElementById("items-q"),
      lang = document.getElementById("items-lang"),
      type = document.getElementById("items-type"),
      size = document.getElementById("items-size"),
      count = document.getElementById("items-count"),
      pager = document.getElementById("items-pages");
  var page = 1, matches = rows;

  function fill(select, key) {                       // option list from the data
    var seen = {};
    rows.forEach(function (r) { seen[r.dataset[key]] = 1; });
    Object.keys(seen).sort().forEach(function (v) {
      var o = document.createElement("option"); o.value = o.textContent = v; select.appendChild(o);
    });
  }
  fill(lang, "lang"); fill(type, "type");

  function pageItem(label, target, opts) {
    var li = document.createElement("li"), a = document.createElement("a");
    li.className = "page-item" + (opts.active ? " active" : "") + (opts.disabled ? " disabled" : "");
    a.className = "page-link"; a.href = "#"; a.textContent = label;
    if (opts.active) a.setAttribute("aria-current", "page");
    a.addEventListener("click", function (e) { e.preventDefault(); if (!opts.disabled) { page = target; render(); } });
    li.appendChild(a); pager.appendChild(li); return li;
  }

  function render() {
    var n = parseInt(size.value, 10), pages = Math.max(1, Math.ceil(matches.length / n));
    page = Math.min(Math.max(page, 1), pages);
    var from = (page - 1) * n, to = from + n;
    rows.forEach(function (r) { r.hidden = true; });
    matches.slice(from, to).forEach(function (r) { r.hidden = false; });
    count.textContent = matches.length
      ? "Showing " + (from + 1) + "–" + Math.min(to, matches.length) + " of " + matches.length
      : "No matching items";

    pager.innerHTML = "";
    if (pages < 2) return;
    pageItem("‹", page - 1, { disabled: page === 1 });
    var shown = [];                                   // first, last, and a window around the current page
    for (var p = 1; p <= pages; p++) if (p === 1 || p === pages || Math.abs(p - page) <= 1) shown.push(p);
    shown.forEach(function (p, i) {
      if (i && p - shown[i - 1] > 1) pageItem("…", p, { disabled: true });
      pageItem(String(p), p, { active: p === page });
    });
    pageItem("›", page + 1, { disabled: page === pages });
  }

  function filter() {
    var words = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    matches = rows.filter(function (r) {
      return (!lang.value || r.dataset.lang === lang.value) &&
             (!type.value || r.dataset.type === type.value) &&
             words.every(function (w) { return r.dataset.text.indexOf(w) !== -1; });
    });
    page = 1; render();
  }

  q.addEventListener("input", filter);
  lang.addEventListener("change", filter);
  type.addEventListener("change", filter);
  size.addEventListener("change", function () { page = 1; render(); });
  render();
})();
