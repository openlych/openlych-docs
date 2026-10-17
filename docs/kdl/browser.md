# Browser blocks

A `browser` step drives a headless Chromium from inside the flow: navigate, click, type, read the DOM, screenshot. The browser is one per runner; each list item gets an isolated incognito context, so cookies and storage never leak between items.

```kdl
browser <operation> into=<var> field=value ...
```

The operation is the first positional argument; every field is a `key=value` property with the exact field names below (underscores included). All fields are templated. Every operation binds something into `into`: action operations bind `ok` on success, boolean operations bind `true`/`false`, value operations bind the value. `into=_` discards a value you do not need.

The browser binary is configured in [Settings](../usage/settings.md#browser): auto-downloaded managed Chromium by default, or a Chrome/Chromium executable you point at. Headless is the default; switch it off in settings to watch a run.

```kdl
browser open into=_
browser navigate_to into=_ url="https://the-internet.herokuapp.com/dropdown"
browser select_by_value into=picked selector="select#dropdown" value="2"
browser get_attribute_value_all into=links selector=a attribute=href
browser screenshot_page into=shot
browser close into=_
```

`selector` fields are CSS selectors, or XPath when the selector starts with `/` or `(`.

## Page and navigation

| Operation | Fields | Binds |
|-----------|--------|-------|
| `open` | | `ok`; opens an isolated page for this item |
| `close` | | `ok`; closes the page, the browser stays for the next item |
| `navigate_to` | `url` | `ok` |
| `reload` | | `ok` |
| `get_dom` | | the full page HTML |
| `get_current_url` | | the current URL |
| `execute_js` | `code` | the JS result as a string |
| `screenshot_page` | | full-page PNG, base64 |
| `new_tab` | `url` (optional) | `ok` |
| `switch_tab` | `index` (0-based) | `ok` |
| `close_tab` | | `ok` |
| `go_back` / `go_forward` | | `ok` |
| `wait_for_navigation` | `timeout_ms` | `ok` |
| `wait_for_response` | `url`, `timeout_ms` | `ok` when a response whose URL contains `url` was seen. Matches by URL substring over resource timings; it cannot read the response body. |

## Elements

| Operation | Fields | Binds |
|-----------|--------|-------|
| `click` | `selector` | `ok` |
| `type_text` | `selector`, `text` | `ok` (focuses first) |
| `type_element_human` | `selector`, `text`, `delay_ms` | `ok`, with a per-keystroke delay |
| `clear` | `selector` | `ok` |
| `submit` | `selector` | `ok` (submits the element's form) |
| `select_by_index` | `selector`, `index` | `ok` |
| `select_by_text` | `selector`, `text` | `ok` |
| `select_by_value` | `selector`, `value` | `ok` |
| `exists` | `selector` | `true`/`false` |
| `is_displayed` | `selector` | `true`/`false` (element has layout boxes) |
| `get_attribute` | `selector`, `attribute` | the attribute value (empty if absent) |
| `get_attribute_value_all` | `selector`, `attribute` | the attribute from every match, one per line |
| `set_attribute` | `selector`, `attribute`, `value` | `ok` |
| `wait_for_element` | `selector`, `timeout_ms` | `ok` |
| `screenshot_element` | `selector` | element PNG, base64 |
| `upload_files` | `selector`, `files` | `ok`; a file input set to space-separated absolute paths |
| `scroll_to_element` | `selector` | `ok` |
| `get_position_x` / `get_position_y` | `selector` | the element's X/Y in pixels |
| `switch_to_frame` | `selector` | `ok`; scopes later JS and DOM ops to a same-origin iframe |
| `switch_to_main_frame` | | `ok`; back to the main frame |

## Mouse and keyboard

| Operation | Fields |
|-----------|--------|
| `mouse_move` | `x`, `y` (viewport coordinates) |
| `mouse_click_xy` | `x`, `y` |
| `mouse_down` / `mouse_up` | `x`, `y` |
| `press_key` | `key` (e.g. `Enter`, `Tab`, `Escape`) |
| `page_type` | `text` (inserts at the focused element) |
| `scroll_by` | `x`, `y` (pixels) |
| `scroll_to_bottom` / `scroll_to_top` | |

## State

| Operation | Fields | Binds |
|-----------|--------|-------|
| `get_cookies` | | all cookies as a JSON array |
| `set_cookie` | `name`, `value`, `domain` | `ok` |
| `clear_cookies` | | `ok` |
| `set_user_agent` | `user_agent` | `ok` (for this page) |
| `set_viewport` | `width`, `height` | `ok` |
| `get_viewport` | | `{"width":..,"height":..}` |

Cookies set here are the browser's own, separate from the HTTP cookie jar used by `request` steps.
