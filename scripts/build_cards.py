"""Generates the app cards in assets/cards/. Run from the repo root: python3 scripts/build_cards.py"""

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "cards"

APPS = [
    {
        "slug": "argus",
        "name": "Argus",
        "tag": "macOS · Swift",
        "icon": "argus.png",
        "lines": [
            "A menu bar app that shows your",
            "Claude Code, Codex, OpenCode, and",
            "Pi sessions, which ones need you,",
            "and what they cost.",
        ],
    },
    {
        "slug": "halolight",
        "name": "HaloLight",
        "tag": "Windows · C#",
        "icon": "halolight.png",
        "lines": [
            "A virtual ring light. Your screen",
            "glows to light your face on video",
            "calls and streams.",
        ],
    },
    {
        "slug": "rovepane",
        "name": "Rovepane",
        "tag": "Windows · C#",
        "icon": "rovepane.svg",
        "lines": [
            "A tray app for virtual desktops.",
            "Switch desktops, move windows",
            "between them, and bind global",
            "hotkeys.",
        ],
    },
]

THEMES = {
    "light": {"name": "#0969da", "muted": "#59636e", "text": "#1f2328"},
    "dark": {"name": "#4493f8", "muted": "#9198a1", "text": "#f0f6fc"},
}

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
WIDTH = 260
ICON = 72
LINE_HEIGHT = 20
FIRST_LINE_Y = 158
HEIGHT = FIRST_LINE_Y + LINE_HEIGHT * (max(len(app["lines"]) for app in APPS) - 1) + 32


def icon_uri(filename):
    path = ROOT / "assets" / filename
    mime = "image/svg+xml" if path.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def card(app, colors):
    mid = WIDTH / 2
    lines = "\n".join(
        f'<text x="{mid}" y="{FIRST_LINE_Y + i * LINE_HEIGHT}" font-size="14" fill="{colors["text"]}">{escape(line)}</text>'
        for i, line in enumerate(app["lines"])
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<g font-family="{FONT}" text-anchor="middle">
<image x="{mid - ICON / 2}" y="0" width="{ICON}" height="{ICON}" xlink:href="{icon_uri(app["icon"])}"/>
<text x="{mid}" y="100" font-size="16" font-weight="600" fill="{colors["name"]}">{escape(app["name"])}</text>
<text x="{mid}" y="122" font-size="12" fill="{colors["muted"]}">{escape(app["tag"])}</text>
{lines}
</g>
</svg>
"""


OUT.mkdir(parents=True, exist_ok=True)
for app in APPS:
    for theme, colors in THEMES.items():
        (OUT / f"{app['slug']}-{theme}.svg").write_text(card(app, colors))
