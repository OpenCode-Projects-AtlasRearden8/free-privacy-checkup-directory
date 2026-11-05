#!/usr/bin/env python3
"""Verify every external link in directory.md is live.

No scraping: single GET with a byte-range/empty read, status code only.
Bot-blocked responses (403/406/429) count as "live" because the server
answered over HTTPS; hard failures (404/5xx/timeout) must be fixed.
"""

import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
MD = HERE / "directory.md"

BOT_BLOCKED = {403, 406, 429}
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def extract_urls(md_text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\]\((https?://[^)\s]+)\)", md_text)))


def check(url: str, timeout: float = 25.0) -> tuple[str, int | None]:
    """Return (status_word, http_code_or_None)."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            code = resp.getcode()
            resp.read(1)
            return ("live", code)
    except urllib.error.HTTPError as exc:
        code = exc.code
        if code in BOT_BLOCKED:
            return ("live-bot-blocked", code)
        return ("fail", code)
    except Exception:
        return ("fail", None)


def main() -> int:
    if not MD.exists():
        print(f"missing {MD}", file=sys.stderr)
        return 2
    urls = extract_urls(MD.read_text(encoding="utf-8"))
    non_https = [u for u in urls if not u.startswith("https://")]
    if non_https:
        print("non-https links found:", *non_https, sep="\n  ", file=sys.stderr)
        return 2

    failures = []
    warnings = []
    print(f"checking {len(urls)} links (status-code only, no scraping)\n")
    for url in urls:
        status, code = check(url)
        print(f"{status:>18}  {code if code else '---'}  {url}")
        if status == "fail":
            failures.append((url, code))
        elif status == "live-bot-blocked":
            warnings.append((url, code))

    print(f"\nlive: {len(urls) - len(failures)}/{len(urls)}")
    if warnings:
        print("reachable but bot-blocked (fine in a browser):")
        for url, code in warnings:
            print(f"  {code}  {url}")
    if failures:
        print("FAILURES:")
        for url, code in failures:
            print(f"  {code}  {url}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
