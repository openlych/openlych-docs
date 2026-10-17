# OpenBullet import and export

OpenLych reads OpenBullet configs and writes a subset of OpenBullet back out, so existing work moves across without a rewrite.

## Import

In the **Configs** tab, press **Import** and choose a file. Supported formats:

- OB2 `.opk` packages (a zip holding a LoliCode script and metadata).
- OB2 LoliCode as pasted text or a `.txt` file.
- OB1 LoliScript (`.loli` / `.les` files).

The importer maps blocks onto the equivalent OpenLych steps. Anything it cannot map becomes a disabled placeholder: a `set` step into an `UNMAPPED_n` variable holding the original block text, with a warning. The config still loads and runs up to those points, and you finish it by hand. A wrong guess degrades to a visible placeholder instead of a silent mis-map, which is the safer failure.

The import report names the detected format and block count and lists every warning.

## Export

Select a config and press **Export .loli** or **Export .opk** to write OB2-compatible output:

- **Request** and **LR-mode Parse** steps round-trip fully and run in real OpenBullet 2.
- Every other step (functions, utility, protocols, browser, script, keychains) is written as a commented placeholder with a warning naming what needs hand-filling.

The exported script also loads back into OpenLych itself, since the loader skips commented placeholder lines.

## What does not transfer

The engine differs from OpenBullet in a few places by design, so imported configs may need small edits:

- LoliScript-only syntax (OB1 conditionals, `JUMP`, `WHILE`) beyond what the parser maps.
- C# and Python Interop blocks: OpenLych's [script blocks](../kdl/script.md) use JS, Python, and shell, with a different binding convention.
- Selenium/Puppeteer browser blocks map onto the [browser blocks](../kdl/browser.md); check the generated selectors after import.
