# STATUS.md — free-privacy-checkup-directory

Built November 5, 2026 by Asdale Dynamics, LLC.

## What was built

- `directory.md` — the markdown directory: **24 free tools across 7 categories**
  (password-strength checkers, have-i-been-pwned-style breach checkers, email
  aliasing, browser privacy tests, DNS resolvers, router checks, phone-settings
  walkthroughs). Every entry has:
  - a friend-style one-liner,
  - a plain-English "what it actually inspects" line,
  - an explicit note whenever the tool's core check needs a free account.
- `index.html` — static HTML index page generated from the markdown
  (single file, inline CSS, responsive, dark-mode aware, no JS, no external assets).
- `build.py` — build script: parses the markdown, validates the entry schema
  (https-only URLs, One-liner + Inspects required, unique URLs), renders the HTML.
- `check_links.py` — link verifier: GETs each link status-code-only (no scraping,
  no page reads); treats 403/406/429 bot-protection responses as "live" since the
  server answered; exits nonzero on any hard failure (404/5xx/timeout).
- `test_build.py` — 11 automated tests (stdlib unittest) covering the markdown
  schema, category presence, URL uniqueness, and HTML completeness/escaping.
- `README.md` — usage, extension format, scope notes.
- `LICENSE` — MIT, exact line: `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

```bash
python3 check_links.py   # verify all links live (needs network)
python3 test_build.py    # run the 11 tests
python3 build.py         # regenerate index.html from directory.md
```

Open `index.html` in any browser to read the directory. No server, no install,
no dependencies (Python 3.10+ standard library only).

## Verification results

- Link check: **24/24 links live** (HTTP 200 for all; Mozilla Monitor confirmed
  reachable, responds to plain automated clients and fine in browsers).
- Tests: **11/11 pass** (`Ran 11 tests ... OK`).
- Build: succeeds, writes `index.html` with 24 entries in 7 categories; the
  build re-aggregates entry counts in the footer and table of contents anchors.
- HTML: valid structure spot-checked (`<!doctype html>` … `</html>`), all entry
  text, URLs, and titles present after tag-stripping; no `<script>` tags.

## Known gaps

- Link liveness is checked at build time only; future link rot must be caught
  by re-running `python3 check_links.py`.
- `check_links.py` cannot distinguish bot-walled-but-live pages in every future
  case; it treats 403/406/429 as "live" since the server responded — a page
  could theoretically be entirely bot-walled and unreachable by humans
  (Mozilla Monitor was the one such case in practice, and it is fine in browsers).
- The page has no JavaScript; interactive extras (client-side search/filtering)
  are deliberately out of scope for a static, no-tracking page.
- No GitHub Pages workflow included (per instructions: never publish, never push).
- Entry coverage is intentionally curated (24 tools); more niche tools exist
  (e.g., dedicated camera/mic checkers) that could be added later.
