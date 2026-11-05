# Freebie Directory: Your Do-It-Yourself Privacy Checkup

Free tools and services you can use right now, no scraping and no accounts required for the
core checks, to give your digital life a friendly once-over. Each entry has a friend-style
one-liner and a plain-English note on what the tool actually inspects.

**How to use this directory:** pick a section, do the check, and move on. Nothing here is a
scanned-and-judged "test" you can fail — these are tools that show you your own data so you
can decide what to tighten. Links were verified live before this directory was built; see
`check_links.py` in this repo if you want to re-verify them yourself.

**Not included on purpose:** data-broker removal walkthroughs (see our separate guide),
step-by-step password and two-factor setup (separate guide), and the link-safety-inspector
CLI tool (separate tool). This directory is the *checkup*, not the *treatments*.

---

## Password-strength checkers

### [How Secure Is My Password (Security.org)](https://www.security.org/how-secure-is-my-password/)

- **One-liner:** Type a password, get a blunt-but-nice estimate of how long a cracker would need — in your browser tab, at zero cost, in about five seconds.
- **Inspects:** Length, character mix (upper/lower/digits/symbols), and dictionary/common-password patterns, then simulates brute-force crack time against typical offline attack speeds.
- **Safe to use?** Yes — it runs the estimate locally in your browser. Still, test *variations* of your password rather than the exact one you currently use, just as good etiquette.

### [Bitwarden Password Strength Testing Tool](https://bitwarden.com/password-strength/)

- **One-liner:** The same folks behind a popular password manager let you poke at a password with a real zxcvbn-style entropy score, no account needed.
- **Inspects:** Estimated entropy (guess attempts vs. offline-cracking scenarios) using common dictionary and keyboard-pattern matching — the modern "cleverness" scoring, not just "how many symbols did you add."

### [Google Password Manager's Password Checkup](https://passwords.google.com/)

- **One-liner:** If you're signed into a Google account, this quietly cross-checks all your saved passwords at once — reuse, weakness, and known breaches.
- **Inspects:** Every password in your Google-saved list against reuse, length/strength heuristics, and a continuously updated list of leaked credentials (via a privacy-preserving hash comparison).
- **Note:** Requires a Google account sign-in (that's the one in this section that does). There's a similar built-in check in Chrome's and Android's settings.

## Have-I-Been-Pwned-style breach checkers

### [Have I Been Pwned](https://haveibeenpwned.com/)

- **One-liner:** The granddaddy of free breach checks — pop in your email and find out which data leaks have contained it over the last decade.
- **Inspects:** Your email address (not much else) against hundreds of publicly grouped corporate and organizational data-breach dumps, listing service names and dates of exposure.

### [Mozilla Monitor](https://monitor.mozilla.org/)

- **One-liner:** Firefox's friendly take on the breach check — powered by the same leak databases, with ongoing monitoring if you're willing to make a (free) account later.
- **Inspects:** Email address exposure in the same public breach datasets, but presented with clear, low-panic next-step advice for each one.
- **Note:** This site politely refuses bare automated requests on principle; open it in a browser and it works exactly as expected.

## Email aliasing

### [Mozilla Firefox Relay](https://relay.firefox.com/)

- **One-liner:** Generate throwaway-but-still-routable email addresses on demand so each service gets its own alias, and your real inbox stays the only one you actually check.
- **Inspects:** Nothing sneaky — it forwards mail from each alias to your real address and lets you switch an alias off if a service starts spamming; the paid tier adds a mask for phone numbers too.
- **Note:** Core aliasing has a free tier; sign-up creates a Mozilla account (free).

### [DuckDuckGo Email Protection](https://duckduckgo.com/email/)

- **One-liner:** A free `@duck.com` address that secretly strips trackers from every email it forwards — basically Relay and a tiny privacy shield in one.
- **Inspects:** Incoming mail only, and only to remove tracking pixels and tracking redirects; it doesn't read or store your message contents beyond that.
- **Note:** Requires one free account setup, and the browser-extension route makes aliases a two-click affair while you're signing up for things.

### [addy.io](https://addy.io/)

- **One-liner:** A power-user-friendly alias maker with a very generous free tier — you can create a lot of aliases and even reply to them without revealing your real address.
- **Inspects:** It doesn't scan your mail; it simply forwards from a random-or-custom alias to your real inbox and lets you disable or delete aliases that start misbehaving.
- **Note:** Free tier covers the core aliasing; a free account is required to manage aliases.

### [SimpleLogin](https://simplelogin.io/)

- **One-liner:** The cleanest, most self-hostable aliasing service around — free tier included — with aliases, blur, and a searchable alias log.
- **Inspects:** Only what it must: which alias received mail and where to forward it (it logs delivery, not content). Proxies replies the same way so your real address never shows.
- **Note:** Free tier allows a small number of aliases; a free account is required.

## Browser privacy tests

### [EFF Cover Your Tracks](https://coveryourtracks.eff.org/)

- **One-liner:** See for yourself how unique your browser's fingerprint is — and whether your "do not track" setting is being politely ignored.
- **Inspects:** Canvas and WebGL fingerprinting, installed-font fingerprinting, HTTP-header traits, ad-blocker effectiveness, and whether Do Not Track signals are honored, then tells you how unique your combo is among its visitors.

### [AmIUnique](https://amiunique.org/)

- **One-liner:** A research-project-turned-tool from actual academics that shows which of your browser's quirks make you practically one-of-a-kind online.
- **Inspects:** A long list of readable browser traits (canvas, fonts, plugins, screen size, hardware hints) and compares your fingerprint against a large collected dataset to estimate your uniqueness.

### [BrowserLeaks](https://browserleaks.com/)

- **One-liner:** A pixel-perfect rundown of every browser feature that can leak data — canvas, WebGL, IP, WebRTC, geolocation API, and more, each with its own mini-test.
- **Inspects:** A wide battery of individual leak tests (canvas, WebGL, WebRTC, time zones, domains exposed to JavaScript, etc.) so you can spot exactly which single feature is the loud one after you tweak settings.

### [DNSLeakTest](https://www.dnsleaktest.com/)

- **One-liner:** Changed your DNS but not sure it took? This check shows which DNS servers your requests are actually using — including your ISP's if they're sneaking in.
- **Inspects:** Generates randomized test hostnames and observes which recursive resolvers answer them, revealing your real resolver set (and whether your VPN's DNS routing is honest).

### [IPLeak](https://ipleak.net/)

- **One-liner:** See your "public self" as the internet sees you: IP, DNS servers, WebRTC-exposed addresses, and rough geolocation, all on one friendly page.
- **Inspects:** Your apparent public IP as seen by the test's servers, plus DNS resolution paths and browser-exposed WebRTC addresses that could betray your real IP even behind a VPN.

## DNS resolvers (with honest privacy policies)

### [Quad9](https://quad9.net/)

- **One-liner:** A free, no-log DNS resolver (`9.9.9.9`) run by a not-for-profit that blocks known-malicious domains as a bonus — privacy and safety in one red herring-free box.
- **Inspects:** (While resolving) — it matches requested domains against malware/phishing blocklists; queries are not stored in a way that can identify you personally, per its published policy.

### [Cloudflare 1.1.1.1](https://one.one.one.one/)

- **One-liner:** Swap your ISP's logging DNS for one that promises to log almost nothing and erase it fast — and it genuinely feels faster.
- **Inspects:** (While resolving) — it processes every domain you look up; its policy says it discards identifying IP data quickly and sells nothing. Easy to set in seconds on most routers and phones.

## Router checks

### [RouterSecurity.org Checkup Guide](https://routersecurity.org/checklist.php)

- **One-liner:** A friendly, opinionated checklist that walks you through your router's settings like a patient friend who happens to know way too much about routers.
- **Inspects:** Nothing automatically — it walks you through *manually inspecting* admin passwords, Wi-Fi encryption (WPA3/WPA2 not WEP), firmware versions, remote administration, and UPnP behavior.

### [GRC ShieldsUP!](https://www.grc.com/shieldsup/)

- **One-liner:** The internet's longest-standing "knock on your front door" test — it probes your router's exposed ports from the outside and reports which ones answered.
- **Inspects:** Whether your network's common ports (and chosen ranges you pick) respond to unsolicited connections from the outside — the modern "is my router silently exposing something?" test.

### [YouGetSignal Open Port Check](https://www.yougetsignal.com/tools/open-ports/)

- **One-liner:** A dead-simple outside-in port tester: pick (or use) your IP, enter a port, and see whether anything on your network answered the door.
- **Inspects:** Whether a given TCP port on your public IP accepts connections, which is exactly how port-scanners and accidental ransomware find exposed devices.

## Phone-settings walkthroughs

### [Google Security Checkup](https://myaccount.google.com/security-checkup)

- **One-liner:** Google's own guided tour through your account's security: signs you in, shows recent device logins, third-party app access, and two-step status.
- **Inspects:** Signed-in devices, recent security events, compromised-password hints, app passwords, and third-party apps granted scopes on your Google account — all on Android or any browser, free.

### [Google Privacy Checkup](https://myaccount.google.com/intro/privacycheckup)

- **One-liner:** Ten-tips-in-one-screen: pulls up every "is Google saving this?" toggle (activity types, ad personalization, shared defaults) so you can flip each of them consciously.
- **Inspects:** Your current activity-saving and ad-personalization settings across all Google services on one screen, with plain explanations of what each toggle really controls.

### [Apple Personal Safety User Guide](https://support.apple.com/guide/personal-safety/welcome/web)

- **One-liner:** Apple's official step-by-step walkthrough of iPhone settings worth checking — safety-focused, calm, and written so a non-techie can follow every tap.
- **Inspects:** It walks you through *manually reviewing* sharing of location (Find My), app privacy reports, air tag/Tracker Detect checks, house-cleaning of message/plan subscriptions, and account recovery — as a checklist, not a scan.

### [Apple Privacy](https://www.apple.com/privacy/)

- **One-liner:** Not a test, a compass — Apple's plain-English summary of what its own devices collect, ideal as a companion while you poke around iPhone settings.
- **Inspects:** (Nothing — it's background reading.) Included because its app-tracking-transparency and privacy-feature summaries pair neatly with any phone-settings session.

### [NCSC Cyber Aware](https://www.ncsc.gov.uk/cyberaware/home)

- **One-liner:** The UK's cyber-security agency boiled personal security down to six actions — short, kind, and very doable on any phone.
- **Inspects:** (Nothing — it's a walkthrough.) Suggests manually reviewing passwords, screen-lock, two-step setup, software updates, and account recovery steps; no account or scan needed.

---

## Two-minute cheat sheet

New here and overwhelmed? This 2-minute pass hits the highest-value checks:

1. Run one password through a **strength checker** (Security.org works, 10 seconds).
2. Check one important email in **Have I Been Pwned** (10 seconds).
3. Open **EFF Cover Your Tracks** and just read the result — don't fix anything yet (30 seconds).
4. Set your DNS to **1.1.1.1** or **9.9.9.9** if you haven't already (90 seconds).

Done. That's an actual privacy checkup. The rest of this directory waits for when
you're in the mood.

---

*Directory maintained by Asdale Dynamics, LLC — we explain technology like a friend would.*
