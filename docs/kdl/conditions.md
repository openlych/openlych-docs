# Conditions

A condition is the single node inside a `key-check` block or the leading node of
an `if` block. It tests the last response or a variable.

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
| `equals "var" "value"` | Variable equals the value (templated). |
| `has "var"` | Variable exists (was bound). |
| `contains "text"` | Response body contains this substring. |
| `not { <condition> }` | Inverts the condition inside. |

## Negation

Wrap any condition in `not` to invert it:

```kdl
if {
    not { contains "Invalid password" }
    then { result "valid" }
    else { result "invalid" }
}
```
