# Conditions

A condition tests the last response or a variable. Inside a `key-check` keychain, each [chain](steps.md#key-check) holds a group of conditions; in an `if` step, the condition is the leading node of the block.

```kdl
key-check { status 200 }

if {
    status-in 200 299
    then { result "valid" }
}
```

| Condition | Tests |
|-----------|-------|
| `status 200` | Response status equals this code. |
| `status-in 200 299` | Status falls in the inclusive range `min max`. |
| `equals "var" "value"` | Variable equals the value (both templated). |
| `has "var"` | Variable exists (was bound). |
| `contains "text"` | Response body contains this substring. |
| `matches "regex"` | Response body matches this regular expression. |
| `header-contains "name" "value"` | A response header (case-insensitive name) contains the value. |
| `greater "a" "b"` | `a > b` as numbers (both templated; false if either is not a number). |
| `less "a" "b"` | `a < b` as numbers. |
| `not { <condition> }` | Inverts the condition inside. |

To compare lengths, pair a [`function`](functions.md#strings) `length` with `greater` or `less`:

```kdl
function "n" length "{{token}}"
key-check { greater "{{n}}" "20" }
```

## Negation

Wrap any condition in `not` to invert it:

```kdl
if {
    not { contains "Invalid password" }
    then { result "valid" }
    else { result "invalid" }
}
```

Conditions read the **last response**: the status, headers, and body of the most recent `request`, `tcp`, or `udp` step. The `net` and `browser` steps bind their results into variables instead, so test those with `equals`, `has`, or `greater`/`less` on the variable, and pass the variable to `parse` with `source="..."` when you need to extract from it.
