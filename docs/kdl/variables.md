# Variables

Request fields are templated. Two forms expand a variable, and an unknown name
is left literal (so stray braces do not break a request):

- `{{name}}` - native form.
- `<NAME>` - OpenBullet-style form.

```kdl
request POST "https://example.test/login" {
    body text "user={{USERNAME}}&pass=<PASSWORD>"
}
```

## Where variables come from

### From each list item

Every wordlist line seeds:

| Variable | Value |
|----------|-------|
| `line` | The raw line. |
| `INPUT` | The raw line (alias). |
| `USERNAME` / `PASSWORD` | Split of a `user:pass` combo on the first `:`. |

A CSV list seeds one variable per named column instead.

#### Wordlist type

A job's **List type** (in the job detail) changes how each line is read and
drops lines that don't fit:

| Type | Binds | Keeps lines that |
|------|-------|------------------|
| Default | `line`, `INPUT`, and `USERNAME`/`PASSWORD` if a `:` is present | always |
| Credentials | `USERNAME`, `PASSWORD` | are a `user:pass` combo |
| Numeric | `number` | are all digits |
| Email | `EMAIL`, `USERNAME`, `DOMAIN` | look like an email |
| URL | `URL` | start with `http://` / `https://` |

**Data rules** on the job filter the list further: a minimum length and a
regex the line must match. Both apply to text lists (not CSV).

### From the flow

- [`parse`](steps.md#parse) binds the value(s) it pulls out of a response.
- [`set`](steps.md#set) binds a literal or templated value.

A variable marked `capture=#true` on a `parse` step is what shows in the job
results and the Hits DB.

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
