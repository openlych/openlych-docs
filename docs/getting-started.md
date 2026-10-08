# Getting started

## Prerequisites

- Rust (cargo) and Node + npm.
- On Linux: WebKitGTK. Arch package names: `webkit2gtk-4.1`, `gtk3`, `libsoup3`.

## Build and run

```sh
# build the frontend once (re-run after frontend changes)
cd frontend && npm install && npm run build && cd ..

# desktop window (default)
cargo run

# headless / browser mode, then open http://127.0.0.1:3000
cargo run -- --headless
```

### Live frontend dev loop

```sh
cargo run                      # terminal 1: core on :3000
cd frontend && npm run dev     # terminal 2: Vite on :5173, proxies /api + /ws
# open http://localhost:5173
```

## Where data lives

Configs, wordlists, settings, and the Hits DB live in `$OPENLYCH_DATA`, or
`./data` if that variable is not set. Configs are stored as `.kdl` files.

## Your first flow

In the **Configs** tab, open **Stacker** and either drag in blocks or switch to
**Text** and paste KDL. A minimal health check:

```kdl
request GET "http://127.0.0.1:3000/api/health"
if {
    status 200
    then { result "valid" }
    else { result "invalid" }
}
```

Save it, then in the **Jobs** tab create a job that points the config at a list
and press **Start**. See the [KDL overview](kdl/index.md) for the full language.

## Proxies

The **Proxies** tab holds named proxy lists, one proxy per line:

```
1.2.3.4:8080
1.2.3.4:8080:user:pass
socks5://1.2.3.4:1080
# lines starting with # are ignored
```

Plain `host:port` defaults to HTTP; use a `socks5://` / `socks4://` prefix for
SOCKS. Attach a list to a job in its detail view (the **Proxies** dropdown),
then Start. Bots rotate through the pool, and a retry picks the next proxy, so
a dead proxy is swapped out. The proxy used is recorded on each hit.

## Debugging a config

While building a config in the **Stacker**, press **Debug** in the top bar to
open the debugger panel on the right. Type one data line (for example
`user:pass`), press **Start**, and the flow runs once against just that line.
Nothing is saved to the Hits DB.

Three tabs show the result:

- **Log**: each step and its outcome (request status, key-check pass/fail,
  parsed values, the final result bucket).
- **Data**: the variables the flow produced. Captured variables are highlighted.
- **HTML**: the last response body, rendered in a sandboxed frame.

This is the fast loop for getting a config right before you point it at a full
wordlist.
