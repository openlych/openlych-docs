# Steps

Every node below is one step in the flow. Options shown as `key=value` are KDL
properties; omit them for the default.

## request

```kdl
request GET "https://example.test/{{path}}"
```

With options and a body:

```kdl
request POST "https://example.test/login" follow-redirects=#false tls="1.2" {
    header "Content-Type" "application/json"
    basic-auth "{{USERNAME}}" "{{PASSWORD}}"
    body file "payload.json"
}
```

| Part | Meaning |
|------|---------|
| `GET` / `POST` / … | HTTP method (first argument). |
| `"url"` | Request URL (second argument), templated. |
| `follow-redirects=#false` | Turn off auto-redirect so the flow can inspect a 302's own headers. Default is on. |
| `tls="1.2"` or `tls="1.3"` | Minimum TLS version. Default negotiates normally. |
| `header "K" "V"` | A request header (repeatable). |
| `basic-auth "user" "pass"` | HTTP Basic auth, templated. |
| `body …` | Request body (see below). |

### body

```kdl
body text "user={{USERNAME}}&pass={{PASSWORD}}"
body file "payload.json"
body raw "{\"token\":\"{{t}}\"}" content-type="application/json"
body multipart {
    part "field" "value"
    part "upload" "avatar.png" file=#true
}
```

- `body text "..."` - inline body.
- `body file "path"` - read the body from a file.
- `body raw "..." content-type="..."` - send the body verbatim. The
  `content-type` property is optional; omit it to send no Content-Type header.
- `body multipart { ... }` - `multipart/form-data`; each `part` is text, or a
  file when `file=#true`.

The block editor exposes these as a **Request Type** selector (Standard, Basic
Auth, Multipart, Raw); in KDL the type is implied by which `body` and
`basic-auth` nodes you use.

Each list item runs in its own cookie jar, so a `Set-Cookie` from one request
is sent automatically on the item's later requests.

## tcp / udp

Raw socket: connect to `host port`, send a payload, and read the reply into the
last-response body (so `parse` and `key-check` work on it afterwards). The host
and payload are templated.

```kdl
tcp "127.0.0.1" 6379 "PING\r\n" read-timeout=500
udp "1.1.1.1" 53 "..."
```

`read-timeout` is in milliseconds (0 or omitted = the job's request timeout).
Plaintext only (no TLS on the socket) and replies are capped at 64 KiB.

## parse

Pulls value(s) out of the last response (or an overridable `source`) into a
variable. The mode is the second argument: `json`, `lr`, `css`, or `regex`.

```kdl
parse "token" json "$.auth.token" capture=#true
parse "csrf"  lr "name=\"csrf\" value=\"" "\"" use-regex=#true
parse "links" css "a.item" attr="href" recursive=#true
parse "id"    regex "id=(\\d+)" group=1 prefix="#"
```

| Mode | Arguments | Notes |
|------|-----------|-------|
| `json` | `"$.a.b[0]"` | JSON path. |
| `lr` | `"left" "right"` | Between two strings. `use-regex=#true` treats them as regex. |
| `css` | `"selector"` | Element text, or an attribute with `attr="href"`. |
| `regex` | `"pattern"` | `group=N` picks a capture group. |

Options shared by all modes:

| Option | Effect |
|--------|--------|
| `source="..."` | Parse this value instead of the last response. |
| `prefix="..."` / `suffix="..."` | Wrap the result. |
| `recursive=#true` | Return all matches, newline-joined. |
| `encode=#true` | URL-encode the result. |
| `capture=#true` | Mark this as a captured variable (what shows in results and the Hits DB). |
| `create-empty=#true` | Bind an empty variable on no match instead of failing. |

## set

Bind a variable to a literal or templated value.

```kdl
set "ua" "OpenLych/1.0"
set "auth" "Bearer {{token}}"
```

## function

Compute a value with a built-in operation and bind it to a variable. Add
`capture=#true` to surface it in results and the Hits DB.

```kdl
function "hash"  sha256 "{{PASSWORD}}"
function "token" uuid
function "now"   unix-time
function "pin"   random-int 1000 9999
function "nonce" random-string 16 capture=#true
function "enc"   base64-encode "{{USERNAME}}:{{PASSWORD}}"
```

| Operation | Argument(s) | Result |
|-----------|-------------|--------|
| `length` | `"input"` | Character count. |
| `to-upper` / `to-lower` | `"input"` | Upper / lower case. |
| `base64-encode` / `base64-decode` | `"input"` | Base64. |
| `url-encode` / `url-decode` | `"input"` | Percent-encoding. |
| `md5` / `sha256` | `"input"` | Lower-case hex digest. |
| `uuid` | (none) | Random UUID v4. |
| `unix-time` | (none) | Current Unix time (seconds). |
| `random-int` | `min max` | Random integer in `[min, max]`. |
| `random-string` | `length` | Random alphanumeric string. |

The `input` arguments are templated, so `{{var}}` and `<VAR>` expand first.
Random values use a non-cryptographic generator (fine for test data, not keys).

## delay

Pause the flow for a number of milliseconds (also accepts `sleep`).

```kdl
delay 500
```

## key-check

OpenBullet-style keychains. The block holds one or more `chain` nodes, checked
top to bottom; the first chain that matches fires its action and stops the
block. A chain's first argument is the action; its children are
[conditions](conditions.md).

```kdl
key-check {
    chain "valid"   { status 200; contains "Welcome back" }   // all must hold (default)
    chain "invalid" mode="or" { status 401; contains "wrong password" }  // any holds
    chain ban       { contains "temporarily blocked" }
    chain "invalid" { }   // no conditions = always matches (a default/catch-all)
}
```

Actions:

| Action | Effect |
|--------|--------|
| `"<name>"` | Finish the item into that bucket (e.g. `"valid"`, `"invalid"`, custom). |
| `retry` | Re-run the item (next proxy), up to the job's retry count, then the `retry` bucket. |
| `ban` | Same as `retry`; names the intent that the proxy is bad. |
| `none` | Do nothing and continue the flow. |

`mode="or"` makes a chain match when **any** condition holds; the default
(`and`) needs **all**. The older single-condition form (`key-check { status
200 }`) still loads.

## if

Branch on a condition. `then` runs when it holds; the optional `else` runs when
it does not.

```kdl
if {
    status-in 200 299
    then {
        parse "token" json "$.token" capture=#true
        result "valid"
    }
    else {
        result "invalid"
    }
}
```

## repeat

Loop a block a fixed number of times, or once per row of a file (binding each
row to a variable).

```kdl
repeat 3 {
    request GET "https://example.test/page/{{line}}"
}

repeat "users.csv" "row" {
    request GET "https://example.test/u/{{row}}"
}
```

## result

Put the item in a named outcome bucket and stop processing it.

```kdl
result "valid"
```

Common buckets are `valid`, `invalid`, and `custom`, but any name works and
becomes its own counter.
