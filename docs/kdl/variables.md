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
