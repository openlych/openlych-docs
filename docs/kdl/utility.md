# Utility blocks

A `utility` step works on list and dictionary variables, or on files inside the data dir. The result binds to the step's variable.

```kdl
utility "<into>" <operation> <arguments...> [capture=#true]
```

List-valued variables hold multiple items; `split` and the file-readers create them, and most list operations below consume and produce them. Predicates bind `true` or `false`; mutating list operations bind the new list. All value arguments are templated.

```kdl
utility items split "delta,alpha,charlie" ","
utility sorted list-sort items
utility joined list-join sorted "\n" capture=#true
```

## Lists

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `list-length` | list | Number of items. |
| `list-join` | list sep | The items joined with `sep` (a plain string). |
| `list-sort` | list [numeric] [descending] | Sorted list. `numeric` compares items as numbers. |
| `list-reverse` | list | Reversed list. |
| `list-dedupe` | list | Duplicates removed, first occurrence kept. |
| `list-random` | list | One random item. |
| `list-shuffle` | list | Shuffled list. |
| `list-add` | list item | List with `item` appended. |
| `list-remove-at` | list index | List without that index (out of range leaves it unchanged). |
| `list-remove-value` | list item | List without every item equal to `item`. |
| `list-concat` | a b | `a`'s items then `b`'s. |
| `list-index-of` | list item | First index of `item`, or -1. |
| `list-min` / `list-max` | list | Smallest / largest item compared as numbers. Empty list gives an empty string. |
| `list-of-numbers` | start count step | `count` numbers from `start`, stepping by `step`. |
| `zip-lists` | a b sep | Pairs of `a[i]` and `b[i]` joined with `sep`. |
| `split` | input sep | Split a string into a list. |
| `list-const` | item item ... | A list from literal arguments. |

## Dictionaries

Dictionary variables hold `key=value` pairs and are read with the operations below. `{{dict}}` in a template renders a summary (`{N keys}`), so use `dict-get` to pull values out.

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `dict-const` | key=value ... | A dictionary from literal `key=value` properties. |
| `dict-add` | dict key value | The dictionary with `key` set to `value`. |
| `dict-get` | dict key | The value for `key` (empty if absent). |
| `dict-remove` | dict key | The dictionary without `key`. |
| `list-to-dict` | keys values | A dictionary from two parallel lists. |

## Files and folders

File operations are sandboxed to the data dir's `files/` folder: every path is relative to it and cannot escape it. `""` names the `files/` root.

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `file-read` | path | The file as a string. |
| `file-read-lines` | path | The file's lines as a list. |
| `file-write` | path content | Overwrite the file. |
| `file-append` | path content | Append to the file (created if absent). |
| `file-write-lines` | path list | Overwrite the file, one item per line. |
| `file-append-lines` | path list | Append the items, one per line. |
| `file-exists` / `folder-exists` | path | `true` or `false`. |
| `file-delete` / `folder-delete` | path | Delete it (no error if absent; folders delete their contents). |
| `folder-create` | path | Create the folder, and the `files/` root if needed. |
| `files-in-folder` | path | The file names directly inside the folder, as a list. |
| `file-copy` | from to | Copy within the sandbox. |
| `file-move` | from to | Move or rename within the sandbox. |
| `readable-size` | path | Human-readable size such as `1.5 KB`; `0 B` when missing. |

## Byte arrays

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `bytes-const` | hex | A constant hex byte array (whitespace ignored). |
