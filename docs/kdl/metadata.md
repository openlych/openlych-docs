# Metadata

An optional `meta` block at the top of a config carries information about it. It is written only when non-default, and it is edited from the Config editor's metadata form.

```kdl
meta {
    author "you"
    category "logins"
    suggested_bots 8
    allowed_wordlists "combo"
    additional_info "Targets the staging login endpoint."
    proxies #true
    save_empty_captures #true
    ignore_response_errors #true
    custom_input "api_key" "The API key to test" "demo-key"
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
| `save_empty_captures` | bool | Record a hit even when the item produced no captures. Default off: capture-less items are not recorded. |
| `ignore_response_errors` | bool | Treat a network or timeout error as a `none` outcome instead of the `error` bucket. Default off. |
| `continue_on_custom` | bool | Kept for OpenBullet import fidelity; this engine uses explicit `result` steps instead. |

## Custom inputs

A `custom_input` node declares one named value the config needs from the operator: its name, a human description, and a default value. When a job is created from this config, the job form asks for each declared input, and the values are seeded as variables (available as `{{name}}` / `<NAME>`) on every item of the run.

```kdl
meta {
    custom_input "base_url" "Environment to test against" "https://staging.example.test"
    custom_input "api_key" "The API key under test" ""
}

request GET "{{base_url}}/v1/check?key={{api_key}}"
```

Everything after the `meta` block is the flow. If there is no metadata, the file is just the steps.
