# KDL config language

OpenLych stores each flow as a [KDL](https://kdl.dev) document. It is positional, hand-writable, and exactly what the **Text** view of the Config editor edits. The **Blocks** view and the KDL text are two views of the same config, so you can switch between them at any time.

## Shape of a file

A config file is an optional leading `meta` block followed by the flow's steps, one node per step, top to bottom:

```kdl
meta {
    author "you"
    category "examples"
    suggested_bots 8
}

request POST "https://example.test/login" {
    header "Content-Type" "application/x-www-form-urlencoded"
    body text "user={{USERNAME}}&pass={{PASSWORD}}"
}

parse "token" json "$.auth.token" capture=#true
set "auth" "Bearer {{token}}"

request GET "https://example.test/me" {
    header "Authorization" "{{auth}}"
}

key-check {
    chain "valid"   { status 200; contains "Welcome" }
    chain "invalid" { status 401 }
}
```

## Syntax notes

- **Arguments are positional.** `request GET "url"` is a node `request` with two arguments. Strings are quoted; numbers and booleans are bare.
- **Options are properties** written `key=value`. Booleans use KDL's keyword form: `follow-redirects=#false`, `capture=#true`.
- **Children** go in `{ ... }` blocks. Separate nodes on one line with `;`.
- **Escaping**: use `\"` for a quote inside a string, `\\` for a backslash, `\n` for a newline.
- Simple values can also be written unquoted when they contain no spaces or special characters (`into=mx` and `into="mx"` are the same). The editor emits the unquoted form when it can.

## The step nodes

| Node | Purpose |
|------|---------|
| `request` | Make an HTTP request. |
| `parse` | Pull value(s) out of the last response into a variable. |
| `set` | Bind a variable to a literal or templated value. |
| `key-check` | Route the item into a bucket when keychain conditions hold. |
| `if` | Branch on a condition, with `then` and optional `else`. |
| `repeat` | Loop a block a fixed number of times or over a file. |
| `result` | Put the item in a named outcome bucket and stop. |
| `function` | Compute a value with a built-in operation (hashes, crypto, JWT, captcha, and more). |
| `utility` | List, dictionary, and file operations. |
| `tcp` / `udp` | One-shot raw socket: connect, send, read. |
| `net` | Stateful protocols with named handles: WebSocket, DNS, POP3, FTP, SMTP, IMAP, SSH, raw TCP. |
| `script` | Run inline JavaScript, Python, or shell. |
| `browser` | Drive headless Chromium: navigate, click, type, screenshot. |
| `delay` | Pause the flow for a number of milliseconds. |

Reference pages:

- [Steps](steps.md) for the core nodes and their options.
- [Conditions](conditions.md) for what `key-check` and `if` test.
- [Variables](variables.md) for templating.
- [Function blocks](functions.md), [Utility blocks](utility.md), [Protocols](protocols.md), [Browser blocks](browser.md), and [Script blocks](script.md) for the node-specific references.

## Buckets

Every list item ends in exactly one bucket: `valid`, `invalid`, `custom`, `retry`, `ban`, `error`, or `none`, or a custom name declared with a `result` step or a `key-check` chain action. The bucket drives the job's counters and the Hits DB's type filter.

!!! note "Older files still load"
    Earlier node names (`assert`, `extract`, `branch`/`when`/`otherwise`, `finish`, `loop`, `status_is`) and the old 2-argument `parse "v" "$.path"` form still parse, so pre-existing `.kdl` files keep working. New files use the names documented here.
