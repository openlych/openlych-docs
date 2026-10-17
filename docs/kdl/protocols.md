# Protocols

Beyond HTTP, flows can talk over raw sockets and several stateful protocols. There are two families of step:

- `tcp` / `udp`: a one-shot raw socket. Connect, send, read, done.
- `net`: stateful protocol operations with named connection handles. Open a connection once, then later steps reuse it by handle name.

```kdl
net pop3_auto_connect into=ok handle=m1 host="pop.example.test" port=995 tls="true" user="{{USERNAME}}" pass="{{PASSWORD}}"
net pop3_get_mails into=mails handle=m1
net pop3_quit into=_ handle=m1
```

## tcp / udp

A one-shot raw socket: connect to `host port`, send the payload, and read the reply into the last-response body, so `parse` and `key-check` work on it afterwards. The host and payload are templated.

```kdl
tcp "127.0.0.1" 6379 "PING\r\n" read-timeout=500
udp "1.1.1.1" 53 "..."
```

`read-timeout` is in milliseconds (0 or omitted means the job's request timeout). Plaintext only (no TLS on the socket), and replies are capped at 64 KiB. Omit the payload for a read-only connect.

## net steps

The node is `net`, the operation is the first positional argument, and every field is a `key=value` property with the exact field names below (underscores included). All fields are templated. Most operations bind a result into `into` and take the connection name in `handle`; `into=_` discards a value you do not need.

Connection steps bind `ok` when they succeed; on failure the step errors (or lands in the `none` bucket when the config sets `ignore_response_errors`).

### WebSocket

| Operation | Fields |
|-----------|--------|
| `ws_connect` | `url` |
| `ws_send` | `message` |
| `ws_send_raw` | `data` (hex) |
| `ws_read` | (reads the next message into `into`) |
| `ws_disconnect` | (closes and drops the handle) |

```kdl
net ws_connect handle=ws into=c url="wss://ws.ifelse.io"
net ws_send handle=ws into=_ message="hello"
net ws_read handle=ws into=reply
net ws_disconnect handle=ws into=_
```

### DNS

`dns_lookup` is one-shot, with no handle: look up `host` for a `record` type (`A`, `AAAA`, `MX`, `TXT`, `CNAME`, or `NS`); results are newline-joined.

```kdl
net dns_lookup host=gmail.com into=mx record=MX
```

### POP3

`tls="true"` means implicit TLS (e.g. port 995).

| Operation | Fields |
|-----------|--------|
| `pop3_connect` | `host`, `port`, `tls` |
| `pop3_auto_connect` | `host`, `port`, `tls`, `user`, `pass` |
| `pop3_login` | `user`, `pass` |
| `pop3_stat` | (binds `<count> <octets>`) |
| `pop3_retr` | `index` (full raw message) |
| `pop3_dele` | `index` (mark for deletion) |
| `pop3_get_mails` | (all message bodies, `---`-separated) |
| `pop3_get_log` | (the command/response transcript) |
| `pop3_quit` | |

### FTP

Plaintext control channel.

| Operation | Fields |
|-----------|--------|
| `ftp_connect` | `host`, `port` |
| `ftp_login` | `user`, `pass` |
| `ftp_list` | `path` (names, newline-joined) |
| `ftp_download` | `remote` (file text into `into`) |
| `ftp_download_folder` | `remote`, `local` (binds the count downloaded into a sandboxed folder) |
| `ftp_upload` | `remote`, `content` |
| `ftp_get_log` | (empty; the client exposes no transcript) |
| `ftp_quit` | |

### SMTP

`tls="true"` means implicit TLS on port 465; otherwise STARTTLS is used.

| Operation | Fields |
|-----------|--------|
| `smtp_connect` | `host`, `port`, `tls` |
| `smtp_auto_connect` | `host`, `port`, `tls`, `user`, `pass` |
| `smtp_login` | `user`, `pass` |
| `smtp_send` | `from`, `to`, `subject`, `body` |
| `smtp_send_advanced` | `from`, `to`, `cc`, `subject`, `text_body`, `html_body`, `attachments` |
| `smtp_disconnect` | |
| `smtp_get_log` | (empty; the transport exposes no transcript) |

With both a text and an HTML body the mail is sent as `multipart/alternative`; `attachments` is a space- or newline-separated list of names in the data dir's `files/` sandbox.

### IMAP

Always implicit TLS (e.g. port 993).

| Operation | Fields |
|-----------|--------|
| `imap_connect` | `host`, `port` |
| `imap_auto_connect` | `host`, `port`, `user`, `pass` |
| `imap_login` | `user`, `pass` |
| `imap_select` | `mailbox` (binds the message count) |
| `imap_search` | `query` (binds matching sequence numbers, space-separated) |
| `imap_fetch` | `seq` (RFC822 body) |
| `imap_open_inbox` | (select INBOX; binds the message count) |
| `imap_close_folder` | |
| `imap_list_folders` | (names, one per line) |
| `imap_delete_mail` | `seq` (flags `\Deleted` and expunges) |
| `imap_get_mail_count` | `mailbox` |
| `imap_get_last_message_id` | (highest sequence number) |
| `imap_get_log` | (the command/response transcript) |
| `imap_logout` | |

### Raw TCP with a handle

Unlike the one-shot `tcp` step, these keep the connection open across steps. `tls="true"` wraps it in TLS. Text operations use UTF-8; the `*_bytes` variants use hex. Reads collect until the stream idles or the request times out.

| Operation | Fields |
|-----------|--------|
| `tcp_open` | `host`, `port`, `tls` |
| `tcp_send` / `tcp_send_bytes` | `data` |
| `tcp_read` / `tcp_read_bytes` | |
| `tcp_send_read` / `tcp_send_read_bytes` | `data` |
| `tcp_send_read_http` | `data` (send a raw HTTP request; bind headers plus body) |
| `tcp_close` | |

### SSH

| Operation | Fields |
|-----------|--------|
| `ssh_connect` | `host`, `port` |
| `ssh_auth_password` | `user`, `pass` |
| `ssh_auth_none` | `user` (servers that allow it) |
| `ssh_auth_key` | `user`, `private_key`, `pass` (PEM key; `pass` may be empty) |
| `ssh_run` | `command` (binds stdout) |
| `ssh_disconnect` | |

```kdl
net ssh_connect handle=s into=ok host="203.0.113.7" port=22
net ssh_auth_password handle=s into=ok user="root" pass="{{PASSWORD}}"
net ssh_run handle=s into=uptime command="uptime"
net ssh_disconnect handle=s into=_
```
