# OpenLych Docs

OpenLych is a local web-testing workbench. You define a staged web-request
**flow**, point a **job** at an input **list**, and run it with N parallel
**runners** while outcome counters update live.

These docs cover the **KDL configuration language** that flows are stored in on
disk, plus how to install and run the app.

!!! warning "Authorized use only"
    OpenLych is for security research and testing systems you own or are
    explicitly authorized to test. Never point it at unknown or third-party
    systems. You are responsible for how you use it and for complying with all
    applicable laws.

## Where to start

- [Getting started](getting-started.md) — prerequisites, build, and run.
- [KDL overview](kdl/index.md) — the config format, with a full annotated example.
- [Steps](kdl/steps.md) — every step type and its options.
- [Conditions](kdl/conditions.md) — what `key-check` and `if` test.
- [Variables](kdl/variables.md) — templating and where variables come from.

## How a flow runs

1. A **flow** is a top-to-bottom stack of steps: Request, Parse, Set, Key Check,
   If, Repeat, Result.
2. A **job** aims that flow at a wordlist or CSV and runs it across N runners
   pulling a shared queue.
3. Each list item runs in its own cookie-jar session, so a login's
   `Set-Cookie` carries through the item's later requests.
4. Results land in outcome buckets with per-item detail and captured values.
   Captured hits persist to the Hits DB (SQLite).

Configs are edited visually as stacked blocks or as KDL text, and stored as
`.kdl` files in `$OPENLYCH_DATA` (or `./data`).
