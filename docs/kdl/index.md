# KDL config language

OpenLych stores each flow as a [KDL](https://kdl.dev) document. It is friendly,
positional, and hand-writable, and it is exactly what the **Text** view of the
Config editor edits. The **Blocks** view and the KDL text are two views of the
same config, so you can switch between them at any time.

## Shape of a file

A config file is an optional leading `meta` block followed by the flow's steps,
one node per step, top to bottom:

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
parse "csrf"  lr "name=\"csrf\" value=\"" "\"" use-regex=#false

if {
    status 200
    then { result "valid" }
    else { result "invalid" }
}
```

## Syntax notes

- **Arguments are positional.** `request GET "url"` is a node `request` with two
  arguments. Strings are quoted; numbers are bare.
- **Options are properties** written `key=value`. Booleans use KDL's keyword
  form: `follow-redirects=#false`, `capture=#true`.
- **Children** go in `{ ... }` blocks. Separate nodes on one line with `;`.
- **Escaping**: use `\"` for a quote inside a string, `\\` for a backslash.

## The step nodes

| Node | Purpose |
|------|---------|
| `request` | Make an HTTP request. |
| `parse` | Pull value(s) out of the last response into a variable. |
| `set` | Bind a variable to a literal or templated value. |
| `key-check` | Flag the item into a bucket when a condition holds. |
| `if` | Branch on a condition, with `then` and optional `else`. |
| `repeat` | Loop a block a fixed number of times or over a file. |
| `result` | Put the item in a named outcome bucket and stop. |

See [Steps](steps.md) for every option, [Conditions](conditions.md) for what
`key-check` and `if` test, and [Variables](variables.md) for templating.

!!! note "Older files still load"
    Earlier node names (`assert`, `extract`, `branch`/`when`/`otherwise`,
    `finish`, `loop`, `status_is`) and the old 2-argument
    `parse "v" "$.path"` form still parse, so pre-existing `.kdl` files keep
    working. New files use the names documented here.
