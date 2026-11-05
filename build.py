#!/usr/bin/env python3
"""Build the static HTML index page from directory.md.

Parses the directory markdown into categories and entries, validates the
schema (every entry: title, https link, One-liner, Inspects), then renders
a self-contained index.html with inline CSS and no external assets.
"""

import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
MD_PATH = HERE / "directory.md"
OUT_PATH = HERE / "index.html"

TITLE = "Freebie Directory: DIY Privacy Checkup"
TAGLINE = (
    "Free tools and services for a do-it-yourself privacy checkup — "
    "explained like a friend would, no scraping, nothing creepy."
)
FINDER = (
    "A friendly guide from Asdale Dynamics, LLC. "
    "Links verified live before this page was built. "
    "Nothing here needs an account for its core check unless noted."
)

SECTION_ANCHORS = {
    "password-strength checkers": "passwords",
    "have-i-been-pwned-style breach checkers": "breaches",
    "email aliasing": "aliasing",
    "browser privacy tests": "browser",
    "dns resolvers (with honest privacy policies)": "dns",
    "router checks": "router",
    "phone-settings walkthroughs": "phone",
}

SECTION_BLURBS = {
    "password-strength checkers": "See how a password would hold up before you use it for real.",
    "have-i-been-pwned-style breach checkers": "Find out which leaks your email has already been part of.",
    "email aliasing": "Give every service a different address; turn off the noisy ones.",
    "browser privacy tests": "See how unique — and visible — your browser really is.",
    "dns resolvers (with honest privacy policies)": "Stop your ISP from keeping a diary of the sites you look up.",
    "router checks": "Check your front door from the outside, like a stranger would.",
    "phone-settings walkthroughs": "Plain-English walkthroughs of the settings worth reviewing.",
}


class BuildError(Exception):
    pass


Entry = dict


def parse_directory(text: str) -> tuple[str, list[str], list[tuple[str, list[Entry]]]]:
    """Return (intro_text, intro_lines, [(category_title, entries)])."""
    h2_splits = re.split(r"^## ", text, flags=re.MULTILINE)
    if len(h2_splits) < 2:
        raise BuildError("no '## ' category headings found")

    intro = h2_splits[0]
    # Drop H1 and horizontal rules, then join hard-wrapped lines into paragraphs.
    raw_intro = [
        line for line in intro.splitlines()
        if line.strip() and not line.startswith("# ")
        and not re.fullmatch(r"-{3,}", line.strip())
    ]
    intro_lines = []
    paragraph: list[str] = []
    for line in raw_intro:
        paragraph.append(line.strip())
        if line.rstrip().endswith((".", "!", "?", '"', ")")):
            intro_lines.append(" ".join(paragraph))
            paragraph = []
    if paragraph:
        intro_lines.append(" ".join(paragraph))

    categories = []
    for chunk in h2_splits[1:]:
        title, _, body = chunk.partition("\n")
        title = title.strip()
        if title.startswith("Two-minute cheat sheet") or title.startswith("Two-Minute Cheat Sheet"):
            continue
        entries = parse_entries(body)
        if not entries:
            raise BuildError(f"category '{title}' has no entries")
        categories.append((title, entries))
    if not categories:
        raise BuildError("no categories parsed")
    return intro, intro_lines, categories


def parse_entries(body: str) -> list[Entry]:
    entries = []
    parts = re.split(r"^### ", body, flags=re.MULTILINE)
    for chunk in parts[1:]:
        header, _, rest = chunk.partition("\n")
        match = re.fullmatch(r"\[(.+?)]\((https://[^\s)]+)\)", header.strip())
        if not match:
            raise BuildError(f"bad entry header: {header!r}")
        entry = {
            "title": match.group(1),
            "url": match.group(2),
        }
        one = re.search(r"^- \*\*One-liner:\*\*\s*(.+)$", rest, flags=re.MULTILINE)
        insp = re.search(r"^- \*\*Inspects:\*\*\s*(.+)$", rest, flags=re.MULTILINE)
        if not one:
            raise BuildError(f"entry '{entry['title']}' missing One-liner")
        if not insp:
            raise BuildError(f"entry '{entry['title']}' missing Inspects")
        entry["one_liner"] = one.group(1).strip()
        entry["inspects"] = insp.group(1).strip()
        notes = re.findall(r"^- \*\*Note:\*\*\s*(.+)$", rest, flags=re.MULTILINE)
        entry["notes"] = notes
        entries.append(entry)
    return entries


def inline_md(text: str) -> str:
    """Very small subset: `code`, **bold**, *italic*."""
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"<em>\1</em>", text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def render_entry(entry: Entry) -> str:
    parsed_url = urlparse(entry["url"])
    slug = (parsed_url.netloc.removeprefix("www.") + parsed_url.path).strip("/. ")
    slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-") or "entry"
    entry_id = f"{slug}-{entry['title'].lower()}"
    entry_id = re.sub(r"[^a-z0-9-]+", "-", entry_id).strip("-")
    display_host = parsed_url.netloc.removeprefix("www.")
    notes = ""
    if entry["notes"]:
        notes = "".join(
            f'<p class="note">Note: {inline_md(n)}</p>' for n in entry["notes"]
        )
    return f"""\
<article class="entry" id="{html.escape(entry_id)}">
  <h4><a href="{html.escape(entry['url'])}" rel="noopener">{html.escape(entry['title'])}</a></h4>
  <p class="host">{html.escape(display_host)}</p>
  <p class="one-liner">{inline_md(entry['one_liner'])}</p>
  <p class="inspects"><strong>What it actually inspects:</strong> {inline_md(entry['inspects'])}</p>
  {notes}
</article>"""


def render_section(title: str, entries: list[Entry]) -> str:
    anchor = SECTION_ANCHORS.get(title.lower(), "misc")
    blurb = SECTION_BLURBS.get(title.lower(), "")
    blurb_html = f'<p class="blurb">{blurb}</p>' if blurb else ""
    cards = "\n".join(render_entry(e) for e in entries)
    title_attr = html.escape(f"{len(entries)} entries")
    return f"""\
<section id="{anchor}">
  <h3>{html.escape(title)} <a class="count" title="{title_attr}">({len(entries)})</a></h3>
  {blurb_html}
  {cards}
</section>"""


CSS = """\
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0 1rem 3rem;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  line-height: 1.55; color: #1f2430; background: #f7f6f2;
}
main { max-width: 52rem; margin: 0 auto; }
header.hero {
  padding: 2.5rem 1.5rem 1.5rem; text-align: center;
}
header.hero h1 { font-size: 1.9rem; margin: 0 0 .5rem; }
header.hero p.tagline { font-size: 1.05rem; color: #4a5060; margin: 0 auto .5rem; max-width: 40rem; }
header.hero p.finder { font-size: .9rem; color: #6a7180; margin: 0; }
nav.toc {
  display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center;
  padding: 1rem 0 2rem;
}
nav.toc a {
  background: #fff; border: 1px solid #ddd8cc; border-radius: 999px;
  padding: .35rem .85rem; font-size: .9rem; text-decoration: none; color: #2451b3;
}
nav.toc a:hover { background: #eef2ff; }
section { margin: 2rem 0; scroll-margin-top: 1rem; }
section h3 { font-size: 1.3rem; margin: 0 0 .2rem; }
section h3 .count { font-size: .85rem; color: #8a90a0; text-decoration: none; font-weight: normal; }
section p.blurb { margin: 0 0 1rem; color: #4a5060; }
article.entry {
  background: #fff; border: 1px solid #e3ded2; border-radius: .8rem;
  padding: 1rem 1.2rem; margin: 0 0 1rem;
}
article.entry h4 { margin: 0 0 .1rem; font-size: 1.08rem; }
article.entry h4 a { color: #2451b3; text-decoration: none; }
article.entry h4 a:hover { text-decoration: underline; }
article.entry p.host {
  margin: 0 0 .5rem; font-size: .82rem; color: #8a90a0;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}
article.entry p.one-liner { margin: .3rem 0; }
article.entry p.inspects { margin: .3rem 0; font-size: .95rem; color: #33384a; }
article.entry p.note { margin: .35rem 0 0; font-size: .88rem; color: #6a5a2a; background: #fdf6df; border-radius: .4rem; padding: .35rem .6rem; display: inline-block; }
article.entry code { background: #f0eee8; padding: .05rem .3rem; border-radius: .25rem; font-size: .9em; }
section#cheat { background: #eef2ff; border: 1px solid #d6def5; border-radius: .8rem; padding: 1rem 1.5rem; }
section#cheat ol { margin: .5rem 0 0; padding-left: 1.4rem; }
footer { max-width: 52rem; margin: 3rem auto 0; text-align: center; font-size: .85rem; color: #8a90a0; }
@media (prefers-color-scheme: dark) {
  body { background: #171a21; color: #e8e6df; }
  header.hero p.tagline, section p.blurb { color: #b7bcc9; }
  header.hero p.finder, article.entry p.host, section h3 .count, footer { color: #8d93a3; }
  article.entry, nav.toc a { background: #20242e; border-color: #343949; color: #e8e6df; }
  article.entry h4 a, nav.toc a, article.entry h4 a { color: #9db6ff; }
  nav.toc a:hover { background: #262c3c; }
  article.entry code { background: #2a2f3c; }
  article.entry p.note { color: #d8c68a; background: #2b2717; }
  article.entry p.inspects { color: #cfd3de; }
  section#cheat { background: #20242e; border-color: #343949; }
}
"""


def render_html(
    intro_lines: list[str],
    categories: list[tuple[str, list[Entry]]],
) -> str:
    nav_links = []
    for title, entries in categories:
        anchor = SECTION_ANCHORS.get(title.lower(), "misc")
        nav_links.append(f'<a href="#{anchor}">{html.escape(title)}</a>')
    nav_html = "\n".join(nav_links)
    sections = "\n".join(render_section(t, e) for t, e in categories)
    intro_html = "\n".join(f"<p>{inline_md(line)}</p>" for line in intro_lines)
    total = sum(len(e) for _, e in categories)

    return f"""\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} — Asdale Dynamics, LLC</title>
<meta name="description" content="{html.escape(TAGLINE)}">
<style>{CSS}</style>
</head>
<body>
<main>
<header class="hero">
  <h1>{html.escape(TITLE)}</h1>
  <p class="tagline">{html.escape(TAGLINE)}</p>
  <p class="finder">{html.escape(FINDER)}</p>
</header>
<nav class="toc" aria-label="Categories">
{nav_html}
</nav>
{intro_html}
{sections}
<section id="cheat">
  <h3>Two-minute cheat sheet</h3>
  <p>No time for the whole page? This pass hits the highest-value checks:</p>
  <ol>
    <li>Run one password through a <a href="https://www.security.org/how-secure-is-my-password/">strength checker</a> (10 seconds).</li>
    <li>Check one important email in <a href="https://haveibeenpwned.com/">Have I Been Pwned</a> (10 seconds).</li>
    <li>Open <a href="https://coveryourtracks.eff.org/">EFF Cover Your Tracks</a> and just read the result (30 seconds).</li>
    <li>Set your DNS to <a href="https://one.one.one.one/">1.1.1.1</a> or <a href="https://quad9.net/">9.9.9.9</a> (90 seconds).</li>
  </ol>
</section>
</main>
<footer>
  {total} free tools across {len(categories)} categories &middot;
  Maintained by <strong>Asdale Dynamics, LLC</strong> &middot;
  <a href="https://dylanasdale.github.io">dylanasdale.github.io</a> &middot; MIT License
</footer>
</body>
</html>
"""


def main() -> int:
    if not MD_PATH.exists():
        print(f"missing {MD_PATH}", file=sys.stderr)
        return 2
    text = MD_PATH.read_text(encoding="utf-8")
    try:
        _, intro_lines, categories = parse_directory(text)
    except BuildError as exc:
        print(f"build error: {exc}", file=sys.stderr)
        return 1
    html_text = render_html(intro_lines, categories)
    OUT_PATH.write_text(html_text, encoding="utf-8")
    total = sum(len(e) for _, e in categories)
    print(f"built {OUT_PATH.name}: {total} entries in {len(categories)} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
