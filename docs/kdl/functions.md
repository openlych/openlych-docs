# Function blocks

A `function` step computes a value with a built-in operation and binds it to a variable. All value arguments are templated first, so `{{var}}` and `<VAR>` expand before the operation runs.

```kdl
function "<into>" <operation> <arguments...> [capture=#true]
```

`capture=#true` surfaces the result in the job results and the Hits DB, exactly like on a `parse` step.

Operations that cannot produce a value (bad input, wrong length, missing key) bind an empty string rather than failing the item.

```kdl
function "hash"  sha256 "{{PASSWORD}}"
function "now"   unix-time
function "pin"   random-int 1000 9999
function "nonce" random-string 16 capture=#true
```

## Strings

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `length` | input | Character count. |
| `to-upper` / `to-lower` | input | Case conversion. |
| `trim` | input | Whitespace trimmed from both ends. |
| `reverse` | input | Reversed string. |
| `substring` | input start len | `len` characters from `start` (0-based). |
| `replace` | input from to | All occurrences of `from` replaced. |
| `regex-replace` | input pattern replacement | Regex replace. |
| `char-at` | input index | One character (0-based). |
| `count` | input needle | Occurrences of `needle` in `input`. |
| `unescape` | input | `\n`, `\t`, `\\`, `\"` and friends resolved. |
| `translate` | input map | Look up `input` in `map`, written `"US=United States;UK=United Kingdom"`. No match leaves the input unchanged. |

## Encodings

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `base64-encode` / `base64-decode` | input | Base64. |
| `url-encode` / `url-decode` | input | Percent-encoding. |
| `hex-encode` / `hex-decode` | input | Hex. |
| `html-encode` / `html-decode` | input | HTML entities. |
| `base64-to-hex` / `hex-to-base64` | input | Convert between the two. |
| `merge-bytes` | a b | Concatenate two hex byte arrays (whitespace ignored). |

## Hashes

All return a lower-case hex digest.

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `md5` / `sha1` / `sha256` / `sha384` / `sha512` | input | Digest of the input. |
| `md4` | input | MD4 digest. |
| `hmac-sha256` | input key [algorithm] | HMAC of `input` keyed by `key`. `algorithm` is `MD5`, `SHA1`, `SHA256`, `SHA384`, `SHA512`, or `MD4`; blank means SHA256. |
| `ntlm` | input | NTLM hash (MD4 of the UTF-16LE input). |

## Crypto

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `aes-encrypt` / `aes-decrypt` | input key iv | AES-256-CBC. `key` is 32 bytes of hex, `iv` 16 bytes of hex; the output is hex. |
| `rsa-encrypt` / `rsa-decrypt` | input key | RSA with the given key. |
| `rsa-pkcs1-pad2` | input modulus exponent | The PKCS#1 v1.5 padding used by some JavaScript login forms. |
| `pbkdf2` | input salt rounds | PBKDF2-HMAC-SHA256, hex output. |
| `bcrypt-hash` | input rounds | Bcrypt hash. |
| `bcrypt-verify` | input hash | `true` when the input matches the hash, else `false`. |
| `scrypt` | input salt | Scrypt, hex output. |
| `xor` | input key | XOR of the input with the repeating key, hex output. |

## Numbers and dates

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `compute` | expression | Evaluate an arithmetic expression (`compute "2*(3+4)"` -> `14`). Non-numeric input gives an empty string. |
| `ceil` / `floor` | input | Rounding, output as a whole number. |
| `round` | input [decimals] | Rounding, optionally to `decimals` places. |
| `date-to-unix` | input `"YYYY-MM-DD HH:MM:SS"` | Unix seconds. |
| `unix-to-date` | unix-seconds | `"YYYY-MM-DD HH:MM:SS"`. |
| `unix-to-iso` | unix-seconds | ISO 8601. |
| `unix-ms-to-date` | unix-millis | `"YYYY-MM-DD HH:MM:SS"`. |

## Random values and identity

Random values use a non-cryptographic generator: fine for test data, not for keys.

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `uuid` | (none) | Random UUID v4. |
| `unix-time` | (none) | Current Unix time in seconds. |
| `unix-time-ms` | (none) | Current Unix time in milliseconds. |
| `random-int` | min max | Integer in `[min, max]`. |
| `random-float` | min max | Float in `[min, max]`. |
| `random-string` | length | Random alphanumeric string. |
| `get-random-ua` | (none) | A random browser User-Agent string. |
| `get-hwid` | (none) | SHA-256 of the machine ID (or empty when unavailable). |

## Tokens

| Operation | Arguments | Result |
|-----------|-----------|--------|
| `jwt-encode` | payload secret algorithm | Sign `payload` (JSON) into a JWT. `algorithm` such as `HS256`. |
| `jwt-decode` | token | The JWT's payload as JSON. |
| `aws4-signature` | key datestamp region service string-to-sign | An AWS Signature v4 for the given string-to-sign. |

## Captcha solving

These operations submit a captcha to the configured solving service (see [Settings](../usage/settings.md#captcha)) and poll for the answer. With no API key, a failed submission, or after roughly two minutes of polling, the result is an empty string.

Two shorthands exist:

```kdl
function "answer" captcha-image "{{b64image}}"
function "answer" captcha-recaptcha-v2 "SITE_KEY" "https://page.url"
```

The general form covers every supported kind, with the kind as the third positional argument and its fields as properties. Field names use underscores (they match the internal model names):

```kdl
function "answer" captcha hcaptcha site_key="SITE_KEY" page_url="https://page.url"
```

| Kind | Fields |
|------|--------|
| `image` | `body` (base64 image) |
| `text` | `text` |
| `audio` | `body`, `lang` |
| `recaptcha_v2` | `site_key`, `page_url`, `invisible` |
| `recaptcha_v3` | `site_key`, `page_url`, `action`, `min_score` |
| `recaptcha_mobile` | `site_key`, `page_url` |
| `hcaptcha` | `site_key`, `page_url` |
| `funcaptcha` | `public_key`, `page_url`, `service_url` |
| `geetest` | `gt`, `challenge`, `page_url` |
| `geetest_v4` | `captcha_id`, `page_url` |
| `turnstile` | `site_key`, `page_url`, `action`, `data` |
| `cloudflare_challenge` | `site_key`, `page_url` |
| `data_dome` | `captcha_url`, `page_url` |
| `amazon_waf` | `site_key`, `iv`, `context`, `page_url` |
| `capy` | `site_key`, `page_url` |
| `key_captcha` | `user_id`, `session_id`, `server_sign`, `server_sign2`, `page_url` |
| `cut_captcha` | `api_key`, `misery_key`, `page_url` |
| `cyber_siara` | `master_url_id`, `page_url` |
| `lemin` | `captcha_id`, `div_id`, `page_url` |
| `mt_captcha` | `site_key`, `page_url` |
| `atb_captcha` | `app_id`, `api_server`, `page_url` |
| `tencent` | `app_id`, `page_url` |
| `friendly_captcha` | `site_key`, `page_url` |
| `report` | `id`, `correct` |

`report` tells the service whether a previous solution was good (`correct` is `true` or `false`), which some services use for refunds.

The provider is 2captcha (full kind set) or CapMonster (a subset; unsupported kinds return an empty string). Which one is used is a global setting, not a per-step option.
