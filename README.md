# MH Themes

Five dark themes and one light theme for VS Code with a shared, calm syntax palette,
tuned for reading JavaScript / TypeScript and Playwright test code.

| Theme | Type | Background | Notes |
|---|---|---|---|
| **MH Dusk** | dark | deep blue slate | steel-ice variables, sandy properties |
| **MH Graphite** | dark | graphite grey | the reference palette |
| **MH Midnight** | dark | darker graphite | lighter steel variables |
| **MH Steel** | dark | soft grey | coral keywords, purple functions |
| **MH Sunlight** | light | white | quiet palette for daylight |

## Install

Build the `.vsix` and install it locally:

```bash
npm run install-theme
```

Then reload the window (`Cmd/Ctrl+Shift+P` → **Developer: Reload Window**) and pick a theme
with `Cmd/Ctrl+K Cmd/Ctrl+T`.

## Customize

All colors live in `PALETTES` in [build.py](build.py). Edit a palette, then run
`npm run install-theme` again. The `themes/*.json` files are generated; do not edit them by hand.

Palette keys:

| Key | What it colors |
|---|---|
| `keyword` | `const`, `await`, `return`, `this` |
| `function` | function declarations and calls, built-in constructors |
| `method` | method calls (`.open()`, `.toBeVisible()`) |
| `type_` | types, `null`, `undefined` |
| `string` | string literals |
| `regex` | regular expressions and escape sequences |
| `number`, `boolean` | numbers, `true` / `false` |
| `local`, `param` | variables and function parameters |
| `property`, `prop` | object properties; brackets, `=>`, `=` |
| `comment`, `punct` | comments; punctuation and operators |

Method vs. function coloring relies on TypeScript semantic highlighting, so it applies
to `.ts` files (and to `.js` files with type checking).

## Uninstall

Extensions → **MH Themes** → Uninstall.

## License

MIT
