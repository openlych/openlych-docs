# OpenLych Docs

OpenLych is a local workbench for request flows. You define a staged flow of steps, point a **job** at an input list, and run it across N parallel runners while outcome counters update live.

These docs cover how to use the app and the **KDL configuration language** that flows are stored in on disk.

!!! warning "Authorized use only"
    OpenLych is for testing systems you own or are explicitly authorized to test: load testing, QA automation, API checks, scraping your own data, security assessments under contract. Never point it at third-party systems without permission. You are responsible for how you use it and for complying with all applicable laws.

## Where to start

- [Getting started](getting-started.md): prerequisites, build, run, and a first flow.
- [Jobs](usage/jobs.md): creating and controlling jobs, list types, data rules, resume.
- [Proxies](usage/proxies.md): proxy lists, the checker, ban handling.
- [Hits and outputs](usage/hits.md): the Hits DB, export, webhooks, Telegram.
- [Settings](usage/settings.md): every setting and what it does.
- [OpenBullet import](usage/ob-import.md): bring OB1/OB2 configs in, send configs back out.

## The KDL language

- [Overview](kdl/index.md): the config format, with a full annotated example.
- [Steps](kdl/steps.md): request, parse, set, key-check, if, repeat, result.
- [Conditions](kdl/conditions.md): what `key-check` and `if` test.
- [Variables](kdl/variables.md): templating and where variables come from.
- [Metadata](kdl/metadata.md): the `meta` block and custom inputs.
- [Function blocks](kdl/functions.md): 60+ built-in operations (hashes, crypto, JWT, captcha, and more).
- [Utility blocks](kdl/utility.md): lists, dictionaries, and sandboxed files.
- [Protocols](kdl/protocols.md): raw TCP/UDP plus WebSocket, DNS, POP3, FTP, SMTP, IMAP, and SSH steps.
- [Browser blocks](kdl/browser.md): headless Chromium automation from inside a flow.
- [Script blocks](kdl/script.md): inline JavaScript, Python, and shell.

## How a flow runs

1. A **flow** is a top-to-bottom stack of steps: request, parse, compute, branch, loop, or drive a protocol or browser.
2. A **job** aims that flow at a wordlist or CSV and runs it across N runners pulling from a shared queue.
3. Each list item runs in its own cookie-jar session, so a login's `Set-Cookie` carries through the item's later requests.
4. Results land in outcome buckets with per-item detail and captured values. Captured hits persist to the Hits DB (SQLite).

Configs are edited visually as stacked blocks or as KDL text, and stored as `.kdl` files in `$OPENLYCH_DATA` (or `./data`). Seven sample configs ship in `data/configs/` and double as syntax examples.
