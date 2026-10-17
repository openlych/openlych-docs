# Jobs

A job binds one config to one wordlist and runs the flow once per list item across a number of parallel runners ("bots"). The **Jobs** tab lists every job instance with live counters; opening one shows its detail view.

## Creating a job

Press **New**, pick a config and a list, and set the bot count. Everything else has a sensible default and can be changed later in the job detail. If the config declares [custom inputs](../kdl/metadata.md#custom-inputs), the form asks for those values too and seeds them as variables on every item of the run.

Multiple jobs can run at the same time. **Start All** and **Stop All** act on every job in the list.

## Job controls

All controls live in the job detail view and apply while the job is stopped (the engine picks them up on the next start).

| Control | Range | Effect |
|---------|-------|--------|
| Start | 1-based line | Begin the run at this list line. **Resume** overrides it. |
| Bots | 1-200 | Parallel runners pulling from a shared queue. |
| Max proxy uses | 0 = off | Retire a proxy after this many items. |
| Timeout | 1-600 s | Per-request timeout, applied to every step that talks to the network. |
| Retries | 0-10 | Re-run an item after an error or a `retry`/`ban` key-check action, on the next proxy. |
| Max CPM | 0 = off | Throttle the whole job to at most this many checks per minute. |

## List type and data rules

The **List type** controls how each line of the wordlist is read and which variables it seeds; lines that do not fit the type are skipped:

| Type | Binds | Keeps lines that |
|------|-------|------------------|
| Default | `line`, `INPUT`, and `USERNAME`/`PASSWORD` if a `:` is present | always |
| Credentials | `USERNAME`, `PASSWORD` | are a `user:pass` combo |
| Numeric | `number` | are all digits |
| Email | `EMAIL`, `USERNAME`, `DOMAIN` | look like an email |
| URL | `URL` | start with `http://` / `https://` |

CSV lists seed one variable per named column and ignore the type selector.

**Data rules** filter a text list further before the run: a minimum line length and a regex the line must match. Useful for trimming junk from a large list without editing the file.

See [Variables](../kdl/variables.md) for the full seeding rules.

## Resume

Turn on **Resume** to skip list items already processed for that config + wordlist pair, so a stopped or finished run continues where it left off. Progress is saved per config + list when a run ends. **Reset progress** clears it; turning Resume off also runs the whole list again.

## Reading the detail view

The job detail shows:

- A header row with status, CPM, and progress.
- Live counters per outcome bucket (`valid`, `invalid`, `custom`, `retry`, `ban`, `error`, `none`).
- A live item table: each line, its current bucket, the proxy used, and captured values as they land.
- Per-runner activity, so you can see what each bot is doing right now.

Captures marked on `parse`, `function`, or `utility` steps (`capture=#true`) are the values that appear here and in the [Hits DB](hits.md).
