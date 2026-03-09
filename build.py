#!/usr/bin/env python3
"""Build static wiki site from Obsidian markdown notes."""

import json
import re
import shutil
from pathlib import Path

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

ROOT = Path(__file__).parent
OUTPUT = ROOT / "docs"
NOTES_DIRS = ["noel", "adri"]
EXCLUDE_PARTS = {".git", ".obsidian", "tmp", "__pycache__", "docs", ".github", "memory", ".claude"}
SITE_TITLE = "Noel's Wiki"

# ─── helpers ──────────────────────────────────────────────────────────────────

def should_exclude(rel: Path) -> bool:
    return any(p in EXCLUDE_PARTS for p in rel.parts)


def collect_pages() -> list[Path]:
    pages = []
    for d in NOTES_DIRS:
        dp = ROOT / d
        if dp.exists():
            for f in sorted(dp.rglob("*.md")):
                if not should_exclude(f.relative_to(ROOT)):
                    pages.append(f)
    return pages


def page_url(page: Path) -> str:
    """Root-relative URL, e.g. noel/Docker/Flask%20app.html"""
    rel = page.relative_to(ROOT)
    parts = list(rel.parts)
    parts[-1] = parts[-1].replace(".md", ".html")
    return "/".join(p.replace(" ", "%20") for p in parts)


def root_prefix(page: Path) -> str:
    """Relative ../ prefix from page dir back to docs root."""
    rel = page.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else ""


def build_tree(pages: list[Path]) -> dict:
    """Build nested nav tree. Keys prefixed d: for dirs, f: for files."""
    tree: dict = {}
    for page in pages:
        rel = page.relative_to(ROOT)
        parts = list(rel.parts)
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(f"d:{part}", {})
        name = parts[-1].replace(".md", "")
        node[f"f:{name}"] = page_url(page)
    return tree


def _all_urls(tree: dict):
    for v in tree.values():
        if isinstance(v, str):
            yield v
        else:
            yield from _all_urls(v)


def tree_to_html(tree: dict, active_url: str, prefix: str) -> str:
    out = []
    files = sorted((k, v) for k, v in tree.items() if k.startswith("f:"))
    dirs = sorted((k, v) for k, v in tree.items() if k.startswith("d:"))

    for k, url in files:
        name = k[2:]
        css = ' class="active"' if url == active_url else ""
        out.append(f'<a href="{prefix}{url}"{css}>{name}</a>')

    for k, sub in dirs:
        name = k[2:]
        inner = tree_to_html(sub, active_url, prefix)
        is_open = "open" if active_url in set(_all_urls(sub)) else ""
        out.append(
            f'<details {is_open}><summary>{name}</summary>'
            f'<div class="nav-children">{inner}</div></details>'
        )

    return "\n".join(out)


def make_breadcrumb(page: Path) -> str:
    rel = page.relative_to(ROOT)
    parts = list(rel.parts)
    items = [f'<span class="bc-part">{p}</span>' for p in parts[:-1]]
    items.append(f'<span class="bc-current">{parts[-1].replace(".md", "")}</span>')
    return '<span class="bc-sep"> › </span>'.join(items)


def strip_html(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html).strip()


def convert_md(text: str) -> str:
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "codehilite", "toc", "nl2br", "sane_lists", "attr_list"],
        extension_configs={
            "codehilite": {"css_class": "highlight", "guess_lang": True},
            "toc": {"toc_depth": 3},
        },
    )
    return md.convert(text)


# ─── assets ───────────────────────────────────────────────────────────────────

CSS = """\
:root {
  --base:     #1e1e2e;
  --mantle:   #181825;
  --crust:    #11111b;
  --s0:       #313244;
  --s1:       #45475a;
  --s2:       #585b70;
  --ov0:      #6c7086;
  --text:     #cdd6f4;
  --sub0:     #a6adc8;
  --sub1:     #bac2de;
  --blue:     #89b4fa;
  --lav:      #b4befe;
  --teal:     #94e2d5;
  --green:    #a6e3a1;
  --yellow:   #f9e2af;
  --peach:    #fab387;
  --red:      #f38ba8;
  --mauve:    #cba6f7;
  --pink:     #f5c2e7;
  --sky:      #89dceb;
  --sidebar:  280px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;scroll-behavior:smooth}
body{background:var(--base);color:var(--text);font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;line-height:1.65;min-height:100vh}
#layout{display:flex;min-height:100vh}

/* ── sidebar ── */
#sidebar{width:var(--sidebar);min-width:var(--sidebar);background:var(--mantle);border-right:1px solid var(--s0);display:flex;flex-direction:column;position:sticky;top:0;height:100vh;overflow-y:auto;overflow-x:hidden}
#sidebar-top{padding:1rem;border-bottom:1px solid var(--s0);position:sticky;top:0;background:var(--mantle);z-index:10}
#site-title{display:block;font-size:1.05rem;font-weight:700;color:var(--blue);text-decoration:none;margin-bottom:.75rem;letter-spacing:.02em}
#site-title:hover{color:var(--lav)}
#search-box{position:relative}
#search-input{width:100%;background:var(--s0);border:1px solid var(--s1);border-radius:6px;padding:.45rem .75rem;color:var(--text);font-family:inherit;font-size:.85rem;outline:none;transition:border-color .2s}
#search-input::placeholder{color:var(--ov0)}
#search-input:focus{border-color:var(--blue)}
#search-results{position:absolute;top:calc(100% + 4px);left:0;right:0;background:var(--s0);border:1px solid var(--s1);border-radius:6px;max-height:320px;overflow-y:auto;z-index:200;display:none;box-shadow:0 8px 32px rgba(0,0,0,.5)}
#search-results.show{display:block}
.sr{padding:.55rem .75rem;cursor:pointer;border-bottom:1px solid var(--s1);transition:background .1s}
.sr:last-child{border-bottom:none}
.sr:hover{background:var(--s1)}
.sr-title{font-weight:600;color:var(--blue);font-size:.85rem}
.sr-bc{font-size:.72rem;color:var(--sub0);margin-top:2px}
.sr-snippet{font-size:.75rem;color:var(--sub1);margin-top:3px;line-height:1.4}
.hl{color:var(--yellow);font-weight:600}
.no-results{padding:.75rem;color:var(--sub0);font-size:.85rem;text-align:center}

/* ── nav tree ── */
#nav-tree{padding:.6rem .4rem;font-size:.84rem}
#nav-tree a{display:block;padding:.28rem .75rem;color:var(--sub1);text-decoration:none;border-radius:4px;transition:all .12s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#nav-tree a:hover{background:var(--s0);color:var(--text)}
#nav-tree a.active{background:var(--s0);color:var(--blue);font-weight:600}
#nav-tree details{margin:1px 0}
#nav-tree summary{padding:.28rem .75rem;cursor:pointer;color:var(--sub0);font-weight:600;border-radius:4px;list-style:none;display:flex;align-items:center;gap:.4rem;transition:all .12s;user-select:none}
#nav-tree summary::-webkit-details-marker{display:none}
#nav-tree summary::before{content:"▶";font-size:.55rem;transition:transform .18s;flex-shrink:0}
#nav-tree details[open]>summary::before{transform:rotate(90deg)}
#nav-tree summary:hover{background:var(--s0);color:var(--text)}
.nav-children{padding-left:.9rem;border-left:1px solid var(--s0);margin-left:.75rem;margin-top:1px}

/* ── main ── */
#main{flex:1;min-width:0;display:flex;flex-direction:column}
#page-header{padding:.6rem 2rem;border-bottom:1px solid var(--s0);background:var(--mantle);font-size:.8rem;color:var(--sub0)}
.bc-sep{margin:0 .35rem;color:var(--s2)}
.bc-current{color:var(--sub1);font-weight:500}
#content{max-width:900px;width:100%;padding:2rem 2.5rem;margin:0 auto}

/* ── typography ── */
#content h1{font-size:1.9rem;font-weight:700;color:var(--text);margin-bottom:1rem;padding-bottom:.5rem;border-bottom:2px solid var(--s0)}
#content h2{font-size:1.35rem;font-weight:600;color:var(--text);margin-top:2rem;margin-bottom:.6rem;padding-bottom:.3rem;border-bottom:1px solid var(--s0)}
#content h3{font-size:1.1rem;font-weight:600;color:var(--sub1);margin-top:1.5rem;margin-bottom:.4rem}
#content h4,#content h5,#content h6{font-size:1rem;font-weight:600;color:var(--sub0);margin-top:1rem;margin-bottom:.4rem}
#content p{margin-bottom:1rem;color:var(--sub1)}
#content a{color:var(--blue);text-decoration:none}
#content a:hover{text-decoration:underline}
#content ul,#content ol{margin-bottom:1rem;padding-left:1.5rem;color:var(--sub1)}
#content li{margin-bottom:.2rem}
#content blockquote{border-left:3px solid var(--blue);padding:.5rem 1rem;margin:1rem 0;background:var(--mantle);border-radius:0 6px 6px 0;color:var(--sub0)}
#content table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.9rem}
#content th{background:var(--s0);color:var(--text);font-weight:600;padding:.55rem .75rem;text-align:left;border-bottom:2px solid var(--s1)}
#content td{padding:.45rem .75rem;border-bottom:1px solid var(--s0);color:var(--sub1)}
#content tr:hover td{background:var(--mantle)}
#content hr{border:none;border-top:1px solid var(--s0);margin:1.5rem 0}
#content img{max-width:100%;border-radius:8px;margin:.75rem 0;display:block}

/* ── code ── */
#content :not(pre)>code{font-family:'JetBrains Mono','Fira Code',monospace;font-size:.83em;background:var(--s0);color:var(--green);padding:.1em .4em;border-radius:4px}
#content pre{background:var(--crust)!important;border:1px solid var(--s0);border-radius:8px;padding:1.1rem 1.25rem;overflow-x:auto;margin:1rem 0}
#content pre code{background:none;padding:0;color:var(--text);font-size:.86rem;font-family:'JetBrains Mono','Fira Code',monospace}
.highlight{background:var(--crust)!important;border:1px solid var(--s0);border-radius:8px;margin:1rem 0;overflow:hidden;position:relative}
.highlight pre{background:none!important;border:none!important;border-radius:0!important;margin:0!important;padding:1rem 1.25rem}
.code-wrap{position:relative}
.copy-btn{position:absolute;top:.45rem;right:.45rem;background:var(--s1);border:none;border-radius:4px;color:var(--sub0);padding:.2rem .5rem;font-size:.72rem;cursor:pointer;transition:all .12s;font-family:inherit;z-index:5}
.copy-btn:hover{background:var(--s2);color:var(--text)}

/* pygments catppuccin-like */
.highlight .c,.highlight .ch,.highlight .cm,.highlight .c1,.highlight .cs,.highlight .cpf{color:var(--ov0);font-style:italic}
.highlight .cp{color:var(--yellow)}
.highlight .k,.highlight .kc,.highlight .kr{color:var(--mauve);font-weight:700}
.highlight .kd{color:var(--blue);font-weight:700}
.highlight .kn{color:var(--pink);font-weight:700}
.highlight .kt{color:var(--yellow)}
.highlight .o,.highlight .ow{color:var(--sky)}
.highlight .m,.highlight .mb,.highlight .mf,.highlight .mh,.highlight .mi,.highlight .mo,.highlight .il{color:var(--peach)}
.highlight .s,.highlight .s1,.highlight .s2,.highlight .sa,.highlight .sb,.highlight .sc,.highlight .sh,.highlight .sx{color:var(--green)}
.highlight .se{color:var(--peach);font-weight:700}
.highlight .si,.highlight .sr{color:var(--teal)}
.highlight .ss{color:var(--flamingo, #f2cdcd)}
.highlight .na{color:var(--blue)}
.highlight .nb{color:var(--text)}
.highlight .nc{color:var(--yellow)}
.highlight .nd{color:var(--blue)}
.highlight .ne,.highlight .no{color:var(--red)}
.highlight .nf,.highlight .fm{color:var(--blue)}
.highlight .nn{color:var(--yellow)}
.highlight .nt{color:var(--blue)}
.highlight .nv,.highlight .vc,.highlight .vg,.highlight .vi,.highlight .vm{color:var(--text)}
.highlight .err{color:var(--red)}
.highlight .gd{color:var(--red)}
.highlight .gi{color:var(--green)}
.highlight .gu,.highlight .gh,.highlight .gp{color:var(--blue);font-weight:700}

/* ── index page ── */
.idx-section{margin-bottom:2rem}
.idx-section h2{margin-bottom:.75rem}
.idx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.75rem}
.idx-card{display:block;background:var(--mantle);border:1px solid var(--s0);border-radius:8px;padding:.9rem 1rem;text-decoration:none;transition:all .15s}
.idx-card:hover{border-color:var(--blue);background:var(--s0)}
.idx-card-title{color:var(--blue);font-weight:500;font-size:.9rem;margin-bottom:.2rem}
.idx-card-path{color:var(--sub0);font-size:.75rem}

/* ── mobile ── */
#menu-btn{display:none;position:fixed;top:.75rem;left:.75rem;z-index:900;background:var(--s0);border:1px solid var(--s1);color:var(--text);width:2.4rem;height:2.4rem;border-radius:6px;cursor:pointer;font-size:1.1rem;align-items:center;justify-content:center}
@media(max-width:768px){
  #menu-btn{display:flex}
  #sidebar{position:fixed;left:-100%;top:0;height:100vh;z-index:800;transition:left .25s ease;box-shadow:4px 0 24px rgba(0,0,0,.6)}
  #sidebar.open{left:0}
  #content{padding:1.5rem 1.1rem}
  #page-header{padding:.6rem 1rem}
}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--mantle)}
::-webkit-scrollbar-thumb{background:var(--s1);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--s2)}
::selection{background:rgba(137,180,250,.25)}
.task-list-item{list-style:none}
.task-list-item input{margin-right:.5rem}
"""

JS = """\
const ROOT = typeof ROOT_URL !== 'undefined' ? ROOT_URL : './';
let idx = null;

async function loadIndex() {
  try {
    const r = await fetch(ROOT + 'search_index.json');
    idx = await r.json();
  } catch(e) { console.warn('search index unavailable', e); }
}

const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function hl(text, q) {
  if (!q) return esc(text);
  return esc(text).replace(new RegExp('(' + q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&') + ')', 'gi'),
    '<span class="hl">$1</span>');
}

function doSearch(q) {
  if (!idx || !q || q.length < 2) return [];
  const ql = q.toLowerCase();
  return idx
    .map(item => {
      const tScore = item.title.toLowerCase().includes(ql) ? 2 : 0;
      const cIdx = item.content.toLowerCase().indexOf(ql);
      const cScore = cIdx >= 0 ? 1 : 0;
      if (!tScore && !cScore) return null;
      let snippet = '';
      if (cScore) {
        const s = Math.max(0, cIdx - 60), e = Math.min(item.content.length, cIdx + 120);
        snippet = (s > 0 ? '…' : '') + item.content.slice(s, e) + (e < item.content.length ? '…' : '');
      }
      return { ...item, snippet, score: tScore + cScore };
    })
    .filter(Boolean)
    .sort((a, b) => b.score - a.score)
    .slice(0, 12);
}

const inp = document.getElementById('search-input');
const res = document.getElementById('search-results');

function renderResults(q) {
  const results = doSearch(q);
  if (!q || q.length < 2) { res.innerHTML = ''; res.classList.remove('show'); return; }
  if (!results.length) {
    res.innerHTML = '<div class="no-results">No results found</div>';
    res.classList.add('show'); return;
  }
  res.innerHTML = results.map(r => {
    const url = ROOT + r.url;
    return `<div class="sr" onclick="location.href='${url}'">
      <div class="sr-title">${hl(r.title, q)}</div>
      <div class="sr-bc">${esc(r.breadcrumb)}</div>
      ${r.snippet ? `<div class="sr-snippet">${hl(r.snippet, q)}</div>` : ''}
    </div>`;
  }).join('');
  res.classList.add('show');
}

inp.addEventListener('input', () => renderResults(inp.value.trim()));
inp.addEventListener('keydown', e => { if (e.key === 'Escape') { res.classList.remove('show'); inp.blur(); }});
document.addEventListener('click', e => { if (!e.target.closest('#search-box')) res.classList.remove('show'); });
document.addEventListener('keydown', e => {
  if ((e.key === '/' || (e.ctrlKey && e.key === 'k')) && document.activeElement !== inp) {
    e.preventDefault(); inp.focus(); inp.select();
  }
});

// mobile sidebar
const menuBtn = document.getElementById('menu-btn');
const sidebar = document.getElementById('sidebar');
if (menuBtn) {
  menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
  document.addEventListener('click', e => {
    if (!sidebar.contains(e.target) && e.target !== menuBtn) sidebar.classList.remove('open');
  });
}

// copy buttons
document.querySelectorAll('.highlight, pre').forEach(block => {
  if (block.closest('.highlight') && !block.classList.contains('highlight')) return;
  const wrap = document.createElement('div');
  wrap.className = 'code-wrap';
  block.parentNode.insertBefore(wrap, block);
  wrap.appendChild(block);
  const btn = document.createElement('button');
  btn.className = 'copy-btn'; btn.textContent = 'Copy';
  wrap.appendChild(btn);
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(block.innerText).then(() => {
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = 'Copy', 2000);
    });
  });
});

loadIndex();
"""

PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title} — {site_title}</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📓</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}static/style.css">
</head>
<body>
  <button id="menu-btn" aria-label="Toggle sidebar">☰</button>
  <div id="layout">
    <nav id="sidebar">
      <div id="sidebar-top">
        <a href="{prefix}index.html" id="site-title">📓 {site_title}</a>
        <div id="search-box">
          <input id="search-input" type="text" placeholder="Search… (/ or Ctrl+K)" autocomplete="off">
          <div id="search-results"></div>
        </div>
      </div>
      <div id="nav-tree">{nav_html}</div>
    </nav>
    <main id="main">
      <header id="page-header">{breadcrumb}</header>
      <article id="content">{content}</article>
    </main>
  </div>
  <script>const ROOT_URL = "{prefix}";</script>
  <script src="{prefix}static/app.js"></script>
</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{site_title}</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📓</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="static/style.css">
</head>
<body>
  <button id="menu-btn" aria-label="Toggle sidebar">☰</button>
  <div id="layout">
    <nav id="sidebar">
      <div id="sidebar-top">
        <a href="index.html" id="site-title">📓 {site_title}</a>
        <div id="search-box">
          <input id="search-input" type="text" placeholder="Search… (/ or Ctrl+K)" autocomplete="off">
          <div id="search-results"></div>
        </div>
      </div>
      <div id="nav-tree">{nav_html}</div>
    </nav>
    <main id="main">
      <header id="page-header"><span class="bc-current">Home</span></header>
      <article id="content">
        <h1>{site_title}</h1>
        <p>Personal knowledge base. Use the sidebar or search to navigate.</p>
        {index_body}
      </article>
    </main>
  </div>
  <script>const ROOT_URL = "./";</script>
  <script src="static/app.js"></script>
</body>
</html>
"""

# ─── index body ───────────────────────────────────────────────────────────────

def build_index_body(pages: list[Path]) -> str:
    sections: dict[str, list[Path]] = {}
    for p in pages:
        rel = p.relative_to(ROOT)
        top = rel.parts[0]
        sections.setdefault(top, []).append(p)

    out = []
    for section, ps in sorted(sections.items()):
        out.append(f'<div class="idx-section"><h2>{section}</h2><div class="idx-grid">')
        for p in ps:
            url = page_url(p)
            name = p.stem
            rel = p.relative_to(ROOT)
            path_str = " / ".join(rel.parts[:-1])
            out.append(
                f'<a href="{url}" class="idx-card">'
                f'<div class="idx-card-title">{name}</div>'
                f'<div class="idx-card-path">{path_str}</div>'
                f'</a>'
            )
        out.append('</div></div>')
    return "\n".join(out)


# ─── main build ───────────────────────────────────────────────────────────────

def build():
    pages = collect_pages()
    print(f"Found {len(pages)} pages")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    (OUTPUT / "static").mkdir()
    (OUTPUT / ".nojekyll").write_text("")

    # Write static assets
    (OUTPUT / "static" / "style.css").write_text(CSS)
    (OUTPUT / "static" / "app.js").write_text(JS)

    # Build nav tree
    tree = build_tree(pages)

    # Build search index
    search_index = []

    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        html = convert_md(text)
        plain = strip_html(html)
        url = page_url(page)
        rel = page.relative_to(ROOT)
        breadcrumb = " › ".join(rel.parts[:-1]) + " › " + rel.parts[-1].replace(".md", "")

        search_index.append({
            "title": page.stem,
            "url": url,
            "breadcrumb": breadcrumb,
            "content": plain[:2000],
        })

        prefix = root_prefix(page)
        nav_html = tree_to_html(tree, url, prefix)
        bc = make_breadcrumb(page)

        rendered = PAGE_TEMPLATE.format(
            title=page.stem,
            site_title=SITE_TITLE,
            prefix=prefix,
            nav_html=nav_html,
            breadcrumb=bc,
            content=html,
        )

        out_path = OUTPUT / url.replace("%20", " ")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"  {url}")

    # Write search index
    (OUTPUT / "search_index.json").write_text(
        json.dumps(search_index, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    # Write index page
    nav_html = tree_to_html(tree, "", "")
    index_body = build_index_body(pages)
    (OUTPUT / "index.html").write_text(
        INDEX_TEMPLATE.format(
            site_title=SITE_TITLE,
            nav_html=nav_html,
            index_body=index_body,
        ),
        encoding="utf-8",
    )

    print(f"\nBuild complete → {OUTPUT}/")
    print(f"  {len(pages)} pages | search index ready")


if __name__ == "__main__":
    build()
