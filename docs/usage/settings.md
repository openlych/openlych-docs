# Settings

The **Settings** tab edits the app settings, which persist server-side in the data dir (`data/settings.json`). Changes apply immediately; engine defaults apply to jobs created or started afterwards.

## Appearance

| Setting | Meaning |
|---------|---------|
| Theme | Dark, light, or follow the system. |
| UI scale | Zoom for the whole interface, 80 to 150 percent. |
| Accent colour | The `#RRGGBB` highlight colour used across the UI. |
| Density | Spacing of tables and forms (comfortable or compact). |
| Mono font | The monospace font for the text editor and tables. |

## Engine defaults

Defaults for new jobs. Each job can override most of them in its detail view.

| Setting | Default | Meaning |
|---------|---------|---------|
| Bots | 1 | Runner count for a new job. |
| Max bots | 200 | Upper bound a job's bot count is clamped to. |
| Request timeout | 30 s | Per-request timeout, 1 to 600 seconds. |
| Retries | 0 | Whole-item retries on error, 0 to 10. |
| Hit retention | 0 days | Auto-purge hits older than this at startup. 0 keeps everything. |

## Behaviour

- **Confirm destructive actions**: ask before delete and purge actions in the UI.
- **Notify on finish**: desktop notification when a job finishes.
- **Sounds**: play a sound file (from the data dir's `sounds/` folder) when a hit lands and when a job finishes.
- **Remember last tab**: restore the last-open tab on launch.

## Hit outputs

See [Hits and outputs](hits.md). Webhook URL, JSONL output file, and Telegram bot token + chat id; each is off when blank.

## Captcha

- **Provider**: which service the [captcha function ops](../kdl/functions.md#captcha-solving) use: 2captcha or CapMonster.
- **API key** for the chosen provider. Blank disables solving (those ops return an empty string).

## Browser

Options for the [browser blocks](../kdl/browser.md):

| Setting | Meaning |
|---------|---------|
| Headless | Run the automation browser without a visible window. Turn off to watch a run. |
| Executable | Path to a Chrome/Chromium binary. Blank auto-downloads a managed Chromium. |
| Revision | Pin the Chromium revision the auto-downloader fetches. Blank uses the default. |
| No sandbox | Launch Chromium with `--no-sandbox`. Needed to run headless as root or in a container where user namespaces are unavailable; leave off on a normal desktop. |

## Global keys

Two lists of substrings, matched against **every response body** of every job:

- **Ban keys**: a match bans the item's proxy and retries the item on the next one. Commonly a "too many requests" page.
- **Retry keys**: a match retries the item (next proxy), up to the job's retry count.

A ban key wins over a retry key on the same response. Both are off when empty. See [Proxies](proxies.md#ban-handling).

## Data tools

Export settings to a file, import them back, or clear hits and run history in bulk. Exports are plain JSON and can be edited before import.
