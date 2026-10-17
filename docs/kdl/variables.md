# Variables

Request fields are templated. Two forms expand a variable, and an unknown name is left literal (so stray braces do not break a request):

- `{{name}}`: native form.
- `<NAME>`: OpenBullet-style form.

```kdl
request POST "https://example.test/login" {
    body text "user={{USERNAME}}&pass=<PASSWORD>"
}
```

Templating applies everywhere a step takes a value: URLs, headers, bodies, parse sources, function and utility arguments, protocol fields, browser fields, and script code.

## Where variables come from

### From each list item

Every wordlist line seeds:

| Variable | Value |
|----------|-------|
| `line` | The raw line. |
| `INPUT` | The raw line (alias). |
| `USERNAME` / `PASSWORD` | Split of a `user:pass` combo on the first `:` (Default type only, and only when a `:` is present). |

A CSV list seeds one variable per named column instead.

#### Wordlist type

A job's **List type** (in the job detail) changes how each line is read and drops lines that do not fit:

| Type | Binds | Keeps lines that |
|------|-------|------------------|
| Default | `line`, `INPUT`, and `USERNAME`/`PASSWORD` if a `:` is present | always |
| Credentials | `USERNAME`, `PASSWORD` | are a `user:pass` combo |
| Numeric | `number` | are all digits |
| Email | `EMAIL`, `USERNAME`, `DOMAIN` | look like an email |
| URL | `URL` | start with `http://` / `https://` |

**Data rules** on the job filter the list further: a minimum length and a regex the line must match. Both apply to text lists (not CSV).

### From config metadata

[Custom inputs](metadata.md#custom-inputs) declared in the `meta` block are filled in at job creation and seeded as a variable on every item of that run.

### From the flow

- [`parse`](steps.md#parse) binds what it pulls out of a response.
- [`set`](steps.md#set) binds a literal or templated value.
- [`function`](functions.md) and [`utility`](utility.md) bind their computed result.
- [Protocol](protocols.md) and [browser](browser.md) steps bind into their `into` field.
- [`script`](script.md) binds the outputs it declares.

A variable marked `capture=#true` on a `parse`, `function`, or `utility` step is what shows in the job results and the Hits DB.

### List and dictionary variables

Some [`utility`](utility.md) operations produce lists (joined by newlines when templated) or dictionaries (rendered as a summary string). Use `list-join` or `dict-get` to pull a plain value out before templating it into a request.

## Example

```kdl
request POST "https://example.test/login" {
    body text "user={{USERNAME}}&pass={{PASSWORD}}"
}
parse "token" json "$.auth.token" capture=#true
set "auth" "Bearer {{token}}"
request GET "https://example.test/me" {
    header "Authorization" "{{auth}}"
}
```
