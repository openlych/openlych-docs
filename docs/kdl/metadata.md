# Metadata

An optional `meta` block at the top of a config carries information about it. It
is written only when non-default, and it is edited from the Config editor's
metadata form.

```kdl
meta {
    author "you"
    category "logins"
    suggested_bots 8
    allowed_wordlists "combo"
    additional_info "Targets the staging login endpoint."
    proxies #true
}
```

| Field | Type | Meaning |
|-------|------|---------|
| `author` | string | Who wrote the config. |
| `category` | string | Free-form grouping. |
| `suggested_bots` | integer | Default runner count for a new job. |
| `allowed_wordlists` | string | Which wordlist kinds this config expects. |
| `additional_info` | string | Notes shown with the config. |
| `proxies` | bool | Whether the config is intended to run through proxies. |

Everything after the `meta` block is the flow. If there is no metadata, the file
is just the steps.
