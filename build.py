"""Generate themes/*.json from the palettes below.
Run: python3 build.py (then reinstall; see README.md)"""
import json, pathlib

PALETTES = {
    "light": dict(
        type="light",
        bg="#ffffff", bg_alt="#f6f8fa", line_hl="#f6f8fa", border="#d0d7de", text="#24292f", muted="#57606a",
        accent="#0969da", selection="#0969da33", line_no="#6a737d",
        keyword="#b8443a", function="#7b3ff2", type_="#0969da", string="#3a7d44",
        number="#9a6700", boolean="#9a6700", nullish="#0550ae", param="#9b4f96", local="#3d6a8a", prop="#1b1f24", comment="#66707b", punct="#57606a",
    ),
    "midnight": dict(
        type="dark",
        bg="#181c22", bg_alt="#181c22", line_hl="#222831", border="#2c333c", text="#cdd9e5", muted="#9aa7b5",
        accent="#1f6feb", link="#58a6ff", selection="#388bfd40", line_no="#8b95a1",
        keyword="#ff9580", function="#c28fff", type_="#79c0ff", string="#98c379",
        number="#d29922", boolean="#d29922", nullish="#79c0ff", param="#d9a0d6", local="#ccdff3", prop="#ffffff", comment="#9aa4b0", punct="#9da7b3",
    ),
}

# MH Steel: soft grey background with steel variables (MH Midnight: deeper background, lighter variables)
PALETTES["steel"] = {**PALETTES["midnight"],
    "bg": "#22272e", "bg_alt": "#22272e", "line_hl": "#2d333b", "border": "#373e47",
    "local": "#9db9d6", "line_no": "#98a2ae",
}

# status colors: contrast >= 4.5:1 on every surface
for _n, _p in PALETTES.items():
    _light = _p["type"] == "light"
    _p.setdefault("error", "#b3261e" if _light else "#ff8a80")
    _p.setdefault("warning", "#8a5a00" if _light else "#e5b84b")
    _p.setdefault("modified", "#895503" if _light else "#e2c08d")   # warm, matches VS Code's default for changed files
    _p.setdefault("added", "#1a7f37" if _light else "#7ee787")

NAMES = {"light": "MH Sunlight", "steel": "MH Steel", "midnight": "MH Midnight", "graphite": "MH Graphite", "dusk": "MH Dusk"}

# MH Graphite: reference palette, separate roles for functions, methods and regexes
PALETTES["graphite"] = {**PALETTES["midnight"],
    "bg": "#20252d", "bg_alt": "#20252d", "line_hl": "#2a303a", "border": "#363d49",
    "text": "#d5dce5", "muted": "#9aa5b8", "accent": "#7fa6d9", "selection": "#7fa6d933",
    "button": "#2f7d6b",     # filled buttons and badges: dark mint, white label
    "added": "#5cc0a6",      # new/untracked files: same mint, lightened to 4.5:1 as text
    "modified": "#d8b77a",   # changed files: saturated sand, distinct from the pale property color
    "line_no": "#92a0b5",
    "keyword": "#ff9b75",
    "function": "#82afff",   # function declarations and calls: expect(), expectedDatePattern()
    "method": "#61d6f5",     # method calls: .open(), .toBeVisible()
    "type_": "#55d6c8", "nullish": "#55d6c8",
    "string": "#a8e66b", "number": "#c5a0ff", "boolean": "#c5a0ff",
    "regex": "#b5d989",      # regular expressions and escape sequences
    "builtin": "#82afff",    # built-in constructors: String, Number, RegExp, Array
    "local": "#b6c9e0", "param": "#b6c9e0",
    "prop": "#d5dce5", "comment": "#98a3b6", "punct": "#d5dce5",
}


# MH Dusk: Graphite palette on a deep blue slate; ice variables, sandy properties (.heading, object keys)
PALETTES["dusk"] = {**PALETTES["graphite"],
    "bg": "#1b2230", "bg_alt": "#1b2230", "line_hl": "#252d3d", "border": "#303a4d", "line_no": "#97a5bd",
    "local": "#c6dcf2", "param": "#c6dcf2",
    "property": "#d9ceb2",
}

def _lum(h):
    h = h.lstrip("#")[:6]
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contrast(a, b):
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

def on(bg, dark, light="#ffffff"):
    """Readable text color for a filled surface (buttons, badges, status items)."""
    return light if contrast(light, bg) >= contrast(dark, bg) else dark

def mix(a, b, t):
    a, b = a.lstrip("#")[:6], b.lstrip("#")[:6]
    return "#" + "".join(f"{round(int(a[i:i+2], 16) * (1 - t) + int(b[i:i+2], 16) * t):02x}" for i in (0, 2, 4))

def theme(name, p):
    dark = p["type"] == "dark"
    link = p.get("link", p["accent"])
    btn = p.get("button", p["accent"])
    btn_fg = on(btn, p["bg"], "#ffffff")
    # hover moves away from the label color so the label keeps its contrast
    btn_hover = mix(btn, "#000000" if btn_fg == "#ffffff" else "#ffffff", 0.12)
    sel = mix(p["bg"], p["accent"], 0.11 if dark else 0.10)               # opaque list selection, text keeps >= 4.5:1
    hover = p["line_hl"]
    widget = mix(p["bg"], p["text"], 0.06)
    tc = lambda scope, color, style=None: {"scope": scope, "settings": {"foreground": color, **({"fontStyle": style} if style is not None else {})}}
    return {
        "name": NAMES[name],
        "type": p["type"],
        "semanticHighlighting": True,
        "colors": {
            "editor.background": p["bg"], "editor.foreground": p["text"],
            "editor.lineHighlightBackground": p["line_hl"], "editor.selectionBackground": p["selection"],
            "editorCursor.foreground": p["accent"],
            "editorLineNumber.foreground": p["line_no"], "editorLineNumber.activeForeground": p["text"],
            "editorIndentGuide.background1": p["border"], "editorWhitespace.foreground": p["border"],
            "editorGroupHeader.tabsBackground": p["bg_alt"],
            "tab.activeBackground": p["bg"], "tab.inactiveBackground": p["bg_alt"],
            "tab.activeBorderTop": p["accent"], "tab.border": p["border"],
            "sideBar.background": p["bg_alt"], "sideBar.border": p["border"],
            "activityBar.background": p["bg_alt"], "activityBar.border": p["border"],
            "titleBar.activeBackground": p["bg_alt"], "titleBar.border": p["border"],
            "statusBar.background": p["bg_alt"], "statusBar.foreground": p["text"], "statusBar.border": p["border"],
            "panel.background": p["bg_alt"], "panel.border": p["border"],
            "terminal.background": p["bg"], "terminal.foreground": p["text"],
            "focusBorder": link, "contrastActiveBorder": link,
            "foreground": p["text"], "descriptionForeground": p["muted"], "disabledForeground": p["muted"],
            "icon.foreground": p["text"], "errorForeground": p["error"], "widget.border": p["border"],
            "button.background": btn, "button.foreground": btn_fg,
            "button.hoverBackground": btn_hover,
            "button.secondaryBackground": widget, "button.secondaryForeground": p["text"],
            "button.secondaryHoverBackground": hover, "button.border": p["border"],
            "textLink.foreground": link, "textLink.activeForeground": link,
            "badge.background": btn, "badge.foreground": btn_fg,
            "activityBarBadge.background": btn, "activityBarBadge.foreground": btn_fg,
            "activityBar.foreground": p["text"], "activityBar.inactiveForeground": p["muted"],
            "activityBar.activeBorder": link,
            "sideBar.foreground": p["text"], "sideBarTitle.foreground": p["text"],
            "sideBarSectionHeader.background": p["bg_alt"], "sideBarSectionHeader.foreground": p["text"],
            "tab.activeForeground": p["text"], "tab.inactiveForeground": p["muted"],
            "tab.unfocusedActiveForeground": p["muted"], "tab.unfocusedInactiveForeground": p["muted"],
            "titleBar.activeForeground": p["text"], "titleBar.inactiveForeground": p["muted"],
            "titleBar.inactiveBackground": p["bg_alt"],
            "statusBarItem.hoverBackground": hover, "statusBarItem.hoverForeground": p["text"],
            "statusBarItem.remoteBackground": btn, "statusBarItem.remoteForeground": btn_fg,
            "statusBarItem.prominentBackground": widget, "statusBarItem.prominentForeground": p["text"],
            "panelTitle.activeForeground": p["text"], "panelTitle.inactiveForeground": p["muted"],
            "panelTitle.activeBorder": link,
            "list.activeSelectionBackground": sel, "list.activeSelectionForeground": p["text"],
            "list.inactiveSelectionBackground": hover, "list.inactiveSelectionForeground": p["text"],
            "list.hoverBackground": hover, "list.hoverForeground": p["text"],
            "list.focusBackground": sel, "list.focusForeground": p["text"],
            "list.highlightForeground": link, "list.focusHighlightForeground": link,
            "list.errorForeground": p["error"], "list.warningForeground": p["warning"],
            "input.background": p["bg"], "input.foreground": p["text"], "input.border": p["muted"],
            "input.placeholderForeground": p["muted"],
            "inputOption.activeBorder": link, "inputOption.activeBackground": sel,
            "inputValidation.errorBackground": p["bg"], "inputValidation.errorForeground": p["text"],
            "inputValidation.errorBorder": p["error"],
            "inputValidation.warningBackground": p["bg"], "inputValidation.warningForeground": p["text"],
            "inputValidation.warningBorder": p["warning"],
            "inputValidation.infoBackground": p["bg"], "inputValidation.infoForeground": p["text"],
            "inputValidation.infoBorder": link,
            "dropdown.background": widget, "dropdown.foreground": p["text"], "dropdown.border": p["muted"],
            "checkbox.background": p["bg"], "checkbox.foreground": p["text"], "checkbox.border": p["muted"],
            "editorWidget.background": widget, "editorWidget.foreground": p["text"], "editorWidget.border": p["border"],
            "editorSuggestWidget.background": widget, "editorSuggestWidget.foreground": p["text"],
            "editorSuggestWidget.selectedBackground": sel, "editorSuggestWidget.selectedForeground": p["text"],
            "editorSuggestWidget.highlightForeground": link, "editorSuggestWidget.border": p["border"],
            "editorHoverWidget.background": widget, "editorHoverWidget.foreground": p["text"],
            "editorHoverWidget.border": p["border"],
            "quickInput.background": widget, "quickInput.foreground": p["text"],
            "quickInputList.focusBackground": sel, "quickInputList.focusForeground": p["text"],
            "menu.background": widget, "menu.foreground": p["text"],
            "menu.selectionBackground": sel, "menu.selectionForeground": p["text"],
            "menu.separatorBackground": p["border"],
            "notifications.background": widget, "notifications.foreground": p["text"],
            "notificationCenterHeader.background": p["bg_alt"], "notificationCenterHeader.foreground": p["text"],
            "notificationLink.foreground": link,
            "editorError.foreground": p["error"], "editorWarning.foreground": p["warning"],
            "editorInfo.foreground": link, "editorHint.foreground": p["muted"],
            "editorGutter.addedBackground": p["added"], "editorGutter.modifiedBackground": p["modified"],
            "editorGutter.deletedBackground": p["error"],
            "editor.findMatchBackground": mix(p["bg"], p["warning"], 0.45),
            "editor.findMatchHighlightBackground": mix(p["bg"], p["warning"], 0.25),
            "editor.wordHighlightBackground": mix(p["bg"], p["accent"], 0.18),
            "editor.wordHighlightStrongBackground": mix(p["bg"], p["accent"], 0.28),
            "editorLink.activeForeground": link,
            "gitDecoration.addedResourceForeground": p["added"],
            "gitDecoration.untrackedResourceForeground": p["added"],
            "gitDecoration.modifiedResourceForeground": p["modified"],
            "gitDecoration.deletedResourceForeground": p["error"],
            "gitDecoration.conflictingResourceForeground": p["warning"],
            "gitDecoration.ignoredResourceForeground": p["muted"],
            "peekViewEditor.background": widget, "peekViewResult.background": p["bg_alt"],
            "peekViewResult.lineForeground": p["text"], "peekViewResult.fileForeground": p["text"],
            "peekViewResult.selectionBackground": sel, "peekViewResult.selectionForeground": p["text"],
            "peekViewTitle.background": p["bg_alt"], "peekViewTitleLabel.foreground": p["text"],
            "peekViewTitleDescription.foreground": p["muted"],
            "terminal.ansiBlack": p["bg"], "terminal.ansiWhite": p["text"],
            "terminal.ansiRed": p["error"], "terminal.ansiGreen": p["added"], "terminal.ansiYellow": p["warning"],
            "terminal.ansiBlue": link, "terminal.ansiMagenta": p["param"], "terminal.ansiCyan": p["type_"],
            "terminal.ansiBrightBlack": p["muted"], "terminal.ansiBrightWhite": p["text"],
            "terminal.ansiBrightRed": p["error"], "terminal.ansiBrightGreen": p["added"],
            "terminal.ansiBrightYellow": p["warning"], "terminal.ansiBrightBlue": link,
            "terminal.ansiBrightMagenta": p["param"], "terminal.ansiBrightCyan": p["type_"],
            # bracket pairs: one color, shared with =>, = (no rainbow brackets)
            **{f"editorBracketHighlight.foreground{i}": p["prop"] for i in range(1, 7)},
            "editorBracketHighlight.unexpectedBracket.foreground": p["keyword"],
            "editorBracketMatch.background": p["selection"], "editorBracketMatch.border": p["border"],
            "editorBracketPairGuide.activeBackground1": p["border"],
        },
        "tokenColors": [
            tc(["comment", "punctuation.definition.comment"], p["comment"], "italic"),
            tc(["variable", "support.class.console", "support.variable.object"], p["text"]),
            tc(["variable.other.property", "meta.object-literal.key", "support.variable.property",
                "variable.object.property", "meta.object-literal.key string"], p.get("property", p["prop"])),
            tc(["keyword", "storage", "storage.type", "storage.modifier", "keyword.operator.new",
                "keyword.operator.expression", "keyword.control", "variable.language.this"], p["keyword"], "italic"),
            tc(["keyword.control.anchor.regexp", "keyword.operator.quantifier.regexp",
                "keyword.operator.or.regexp", "keyword.operator.negation.regexp",
                "punctuation.definition.group.regexp", "punctuation.definition.character-class.regexp",
                "punctuation.definition.group.assertion.regexp", "keyword.operator.lookahead.regexp"], p["punct"], ""),
            tc(["variable.other.readwrite", "variable.other.constant", "variable.other.object",
                "meta.object-binding-pattern-variable variable.object.property"], p["local"]),
            tc(["variable.parameter", "meta.parameters variable", "meta.parameters meta.object-binding-pattern-variable variable"], p["param"]),
            tc(["entity.name.function", "support.function", "meta.function-call entity.name.function",
                "variable.function"], p["function"]),
            tc(["entity.name.type", "entity.name.class", "entity.other.inherited-class", "support.class",
                "support.type", "support.type.primitive", "entity.name.type.interface",
                "entity.name.type.alias", "meta.type.parameters entity.name.type"], p["type_"]),
            tc(["string", "string.template", "punctuation.definition.string"], p["string"]),
            tc(["constant.numeric"], p["number"]),
            tc(["constant.language.boolean"], p["boolean"]),
            tc(["constant.language.null", "constant.language.undefined"], p["nullish"]),
            tc(["punctuation", "keyword.operator", "meta.brace", "storage.type.function.arrow"], p["punct"], ""),
            tc(["punctuation.definition.block", "punctuation.definition.binding-pattern.object",
                "punctuation.definition.dictionary", "meta.brace.curly"], p["prop"], ""),
            tc(["meta.brace.round", "punctuation.definition.parameters", "punctuation.definition.arguments",
                "punctuation.definition.begin.bracket.round", "punctuation.definition.end.bracket.round",
                "storage.type.function.arrow", "punctuation.section.function",
                "keyword.operator.assignment"], p["prop"], ""),
            tc(["punctuation.definition.template-expression", "punctuation.section.embedded"], p["keyword"]),
            *([tc(["support.class", "support.class.builtin", "support.class.console"], p["builtin"])]
              if "builtin" in p else []),
            *([tc(["string.regexp", "constant.character.escape", "constant.other.character-class.regexp",
                   "constant.character.character-class.regexp", "constant.other.character-class.set.regexp"],
                  p["regex"])] if "regex" in p else []),
            tc(["markup.heading", "entity.name.section"], link, "bold"),
            tc(["markup.inline.raw", "markup.fenced_code"], p["type_"]),
        ],
        "semanticTokenColors": {
            "function": p["function"], "method": p.get("method", p["function"]),
            "class": p["type_"], "class.defaultLibrary": p.get("builtin", p["type_"]), "type": p["type_"],
            "interface": p["type_"], "typeParameter": p["type_"], "enum": p["type_"],
            "variable": p["local"], "variable.defaultLibrary": p["text"], "parameter": p["param"],
            "property": p.get("property", p["prop"]), "namespace": p["text"],
        },
    }

def check(name, t):
    """WCAG AA: fail the build when a foreground/background pair drops under 4.5:1 (3:1 for borders)."""
    c = t["colors"]
    def solid(k):
        return c[k][:7]
    pairs = [(k, k.rsplit(".", 1)[0] + ".background") for k in c if k.endswith(".foreground") and k.rsplit(".", 1)[0] + ".background" in c]
    pairs += [("editor.foreground", "editor.background"), ("editorLineNumber.foreground", "editor.background"),
              ("editorLineNumber.foreground", "editor.lineHighlightBackground"),
              ("tab.inactiveForeground", "tab.inactiveBackground"), ("tab.activeForeground", "tab.activeBackground"),
              ("activityBar.inactiveForeground", "activityBar.background"), ("activityBar.foreground", "activityBar.background"),
              ("sideBar.foreground", "sideBar.background"), ("descriptionForeground", "sideBar.background"),
              ("descriptionForeground", "editor.background"), ("input.placeholderForeground", "input.background"),
              ("list.activeSelectionForeground", "list.activeSelectionBackground"),
              ("list.highlightForeground", "list.activeSelectionBackground"),
              ("list.hoverForeground", "list.hoverBackground"), ("textLink.foreground", "editor.background"),
              ("textLink.foreground", "sideBar.background"), ("errorForeground", "editor.background"),
              ("editorError.foreground", "editor.background"), ("editorWarning.foreground", "editor.background"),
              ("button.foreground", "button.hoverBackground"), ("statusBar.foreground", "statusBarItem.hoverBackground"),
              ("titleBar.inactiveForeground", "titleBar.inactiveBackground"),
              ("panelTitle.inactiveForeground", "panel.background"),
              ("gitDecoration.untrackedResourceForeground", "sideBar.background"),
              ("gitDecoration.modifiedResourceForeground", "sideBar.background"),
              ("gitDecoration.deletedResourceForeground", "sideBar.background"),
              ("gitDecoration.ignoredResourceForeground", "sideBar.background"),
              ("gitDecoration.conflictingResourceForeground", "sideBar.background"),
              ("terminal.ansiBrightBlack", "terminal.background"), ("terminal.ansiBlue", "terminal.background"),
              ("terminal.ansiRed", "terminal.background"), ("terminal.ansiGreen", "terminal.background"),
              ("terminal.ansiYellow", "terminal.background"), ("terminal.ansiMagenta", "terminal.background"),
              ("terminal.ansiCyan", "terminal.background")]
    bad = []
    for fg, bg in pairs:
        if fg in c and bg in c and contrast(solid(fg), solid(bg)) < 4.5:
            bad.append(f"{fg} on {bg}: {contrast(solid(fg), solid(bg)):.2f}")
    bgs = [t["colors"]["editor.background"], t["colors"]["editor.lineHighlightBackground"], t["colors"]["sideBar.background"]]
    for tok in t["tokenColors"]:
        fg = tok["settings"]["foreground"]
        for bg in bgs:
            if contrast(fg, bg) < 4.5:
                bad.append(f"token {tok['scope'][0]} {fg} on {bg}: {contrast(fg, bg):.2f}")
    for k, v in t["semanticTokenColors"].items():
        for bg in bgs:
            if contrast(v, bg) < 4.5:
                bad.append(f"semantic {k} {v} on {bg}: {contrast(v, bg):.2f}")
    if bad:
        raise SystemExit(f"{name}: contrast below WCAG AA\n  " + "\n  ".join(sorted(set(bad))))

for name, p in PALETTES.items():
    check(name, theme(name, p))
    out = pathlib.Path(__file__).parent / "themes" / f"{name}.json"
    out.write_text(json.dumps(theme(name, p), indent=2, ensure_ascii=False) + "\n")
    print("wrote", out.name)
