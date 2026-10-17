# Proxies

The **Proxies** tab holds named proxy lists, one proxy per line:

```
1.2.3.4:8080
1.2.3.4:8080:user:pass
socks5://1.2.3.4:1080
# lines starting with # are ignored
```

Plain `host:port` defaults to HTTP; use a `socks5://` or `socks4://` prefix for SOCKS. `host:port:user:pass` carries credentials for HTTP proxies.

## Attaching proxies to a job

Attach a list to a job in the job detail view (the **Proxies** dropdown), then start the job. Runners rotate through the pool round-robin, so no two bots share a proxy at the same time.

## Ban handling

Two things take a proxy out of rotation:

- A `ban` action on a [key-check](../kdl/steps.md#key-check) chain, when the response looks like the proxy is blocked.
- A global **Ban key** in [Settings](settings.md#global-keys): a substring that, if found in any response body, bans the proxy and retries the item on the next one.

**Max proxy uses** in the job detail retires a proxy after a fixed number of items even if it stays healthy. The proxy used is recorded on each hit, so a bad pool shows up fast in the results.

## The checker

Press **Check** on a proxy list to test every entry. The core opens a request through each proxy and reports `alive / total`. **Keep alive** filters the list down to the proxies that answered, so you can save the file with only the working entries.

The check runs through the app's own HTTP client, so it tests the same path a flow would take.
