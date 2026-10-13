"""Generate themes/*.json from the palettes below.
Run: python3 build.py (then reinstall; see README.md)"""
import json, pathlib

PALETTES = {
    "light": dict(
        type="light",
        bg="#ffffff", bg_alt="#f6f8fa", line_hl="#f6f8fa", border="#d0d7de", text="#24292f", muted="#57606a",
        accent="#0969da", selection="#0969da33", line_no="#8c959f",
        keyword="#c9564a", function="#7b3ff2", type_="#0969da", string="#3a7d44",
        number="#9a6700", boolean="#9a6700", nullish="#0550ae", param="#9b4f96", local="#3d6a8a", prop="#1b1f24", comment="#6e7781", punct="#57606a",
    ),
    "midnight": dict(
        type="dark",
        bg="#181c22", bg_alt="#181c22", line_hl="#222831", border="#2c333c", text="#cdd9e5", muted="#909dab",
        accent="#1f6feb", selection="#388bfd40", line_no="#6e7681",
        keyword="#ff9580", function="#c28fff", type_="#79c0ff", string="#98c379",
        number="#d29922", boolean="#d29922", nullish="#79c0ff", param="#d9a0d6", local="#ccdff3", prop="#ffffff", comment="#8b949e", punct="#9da7b3",
    ),
}

# MH Steel: soft grey background with steel variables (MH Midnight: deeper background, lighter variables)
PALETTES["steel"] = {**PALETTES["midnight"],
    "bg": "#22272e", "bg_alt": "#22272e", "line_hl": "#2d333b", "border": "#373e47",
    "local": "#9db9d6",
}

NAMES = {"light": "MH Sunlight", "steel": "MH Steel", "midnight": "MH Midnight", "graphite": "MH Graphite", "dusk": "MH Dusk"}

# MH Graphite: reference palette, separate roles for functions, methods and regexes
PALETTES["graphite"] = {**PALETTES["midnight"],
    "bg": "#20252d", "bg_alt": "#20252d", "line_hl": "#2a303a", "border": "#363d49",
    "text": "#d5dce5", "muted": "#7f899a", "accent": "#61d6f5", "selection": "#61d6f533", "line_no": "#6b7789",
    "keyword": "#ff9b75",
    "function": "#82afff",   # function declarations and calls: expect(), expectedDatePattern()
    "method": "#61d6f5",     # method calls: .open(), .toBeVisible()
    "type_": "#55d6c8", "nullish": "#55d6c8",
    "string": "#a8e66b", "number": "#c5a0ff", "boolean": "#c5a0ff",
    "regex": "#b5d989",      # regular expressions and escape sequences
    "builtin": "#82afff",    # built-in constructors: String, Number, RegExp, Array
    "local": "#b6c9e0", "param": "#b6c9e0",
    "prop": "#d5dce5", "comment": "#7f899a", "punct": "#d5dce5",
}


# MH Dusk: Graphite palette on a deep blue slate; ice variables, sandy properties (.heading, object keys)
PALETTES["dusk"] = {**PALETTES["graphite"],
    "bg": "#1b2230", "bg_alt": "#1b2230", "line_hl": "#252d3d", "border": "#303a4d", "line_no": "#5f6b82",
    "local": "#c6dcf2", "param": "#c6dcf2",
    "property": "#d9ceb2",
}

def theme(name, p):
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
            "statusBar.background": p["bg_alt"], "statusBar.foreground": p["muted"], "statusBar.border": p["border"],
            "panel.background": p["bg_alt"], "panel.border": p["border"],
            "terminal.background": p["bg"], "terminal.foreground": p["text"],
            "focusBorder": p["accent"], "button.background": p["accent"],
            "textLink.foreground": p["accent"], "badge.background": p["accent"],
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
            tc(["markup.heading", "entity.name.section"], p["accent"], "bold"),
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

for name, p in PALETTES.items():
    out = pathlib.Path(__file__).parent / "themes" / f"{name}.json"
    out.write_text(json.dumps(theme(name, p), indent=2, ensure_ascii=False) + "\n")
    print("wrote", out.name)
