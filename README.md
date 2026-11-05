# Freebie Directory: DIY Privacy Checkup

Free tools and services for a do-it-yourself privacy checkup, curated in the
friendly "like a friend would" style of [Asdale Dynamics, LLC](https://dylanasdale.github.io):

- password-strength checkers
- have-i-been-pwned-style breach checkers
- email aliasing services
- browser privacy tests (fingerprinting, DNS/WebRTC leaks)
- honest-privacy DNS resolvers
- router checks (outside-in port tests, manual router checklist)
- phone-settings walkthroughs (Google, Apple, NCSC)

Every entry has a friend-style one-liner and a plain-English note on what the
tool **actually inspects**. No scraping, and no accounts needed for the core
checks unless explicitly flagged in the entry's note. All 24 links were
verified live (status-code checks only, no content scraping) before this
directory was built.

## Contents

| File | What it is |
|---|---|
| `directory.md` | The directory itself: 24 free tools across 7 categories |
| `index.html` | Static HTML index page, generated from the markdown |
| `build.py` | Build script: parses `directory.md`, validates the schema, writes `index.html` |
| `check_links.py` | Link checker: verifies every link is live before you build |
| `test_build.py` | Test suite for the markdown schema and the generated HTML |
| `LICENSE` | MIT license |
| `STATUS.md` | What was built, verification results, and known gaps |

## Run it

```bash
# 1. Verify all links are live (network required)
python3 check_links.py

# 2. Run the tests
python3 test_build.py

# 3. (Re)build the static HTML page
python3 build.py
```

Then open `index.html` in any browser — it is a single self-contained file
(inline CSS, no external assets, no JavaScript).

## How to extend it

Edit `directory.md`. Entry format:

```markdown
## Category Title

### [Tool Name](https://tool.example.com/)

- **One-liner:** a friendly sentence a real person would say.
- **Inspects:** what the tool actually looks at, in plain English.
- **Note:** free-tier/account caveats, if any.
```

The build validates that every entry has a title, an https URL, a `One-liner`,
and an `Inspects` line, and the tests enforce category presence, unique URLs,
and that the generated HTML contains every entry.

## Scope (on purpose)

This is the *checkup* directory. It intentionally does **not** include:

- step-by-step data-broker opt-out walkthroughs (see
  `data-broker-removal-walkthrough-guide`)
- password manager + two-factor setup instructions (see
  `password-and-two-step-guide`)
- a CLI tool that checks links before you click them (see
  `link-safety-inspector-cli`)

These are sibling projects; this directory links to free checks, not opt-out
procedures or tool installs.

## Privacy of this repo

No secrets, API keys, or personal data are stored in any file. Examples in
`directory.md` discuss tool categories, never sample emails or addresses.

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Asdale Dynamics, LLC. Built by Asdale Dynamics, LLC —
we explain technology like a friend would.
