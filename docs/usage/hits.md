# Hits and outputs

A hit is a list item that finished in a bucket worth keeping, together with its captured values. Every hit lands in the local Hits DB; optional outputs forward each hit to other systems as it arrives.

## The Hits DB

Hits persist in SQLite (`data/openlych.db`), so they survive restarts. The **Hits DB** tab lists them with:

- Filters by config and outcome type.
- A search box over captured values.
- The data line, the config, the bucket, the proxy used, and the timestamp for each hit.

The toolbar can export the current view, delete duplicate hits (same config + data + captures), delete the hits matching the current filters, or purge everything. **Hit retention** in [Settings](settings.md#engine-defaults) auto-purges hits older than a number of days at startup; 0 keeps everything.

A config that produces no captures is not recorded as a hit unless its metadata sets `save_empty_captures #true` (see [Metadata](../kdl/metadata.md)).

## Hit outputs

In **Settings -> Hit outputs**, three optional forwarders fire for every hit as it lands. Leave a field blank to disable it.

### Webhook URL

Each hit is POSTed as JSON with a Discord/Slack-style `content` string plus structured fields (`config`, `type`, `data`, `captures`, `proxy`), so it works with a Discord or Slack webhook or any custom endpoint that accepts JSON.

### Output file

Each hit is appended as one JSON object per line (JSONL) to the given path. Good for feeding results into other tooling.

### Telegram

With a bot token and a chat or channel id set, each hit is sent through the Telegram Bot API. The token is stored in the local settings file, so use a dedicated bot.
