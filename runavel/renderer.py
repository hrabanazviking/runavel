"""
Runic Terminal Renderer
~~~~~~~~~~~~~~~~~~~~~~~~~
Beautiful visualizations of runes, rune circles, and spreads
rendered directly in the terminal using Unicode and ASCII.

"Every line of code should feel like it was carved from Yggdrasil."
  — Vibe Coding Directive
"""

from typing import Optional

from .runes import (
    ELDER_FUTHARK,
    RUNE_BY_UNICODE,
    AETTIR,
    Aett,
    Rune,
)
from .divination import Spread, DrawnRune, SpreadPosition


# ── ASCII Art Rune Staves ─────────────────────────────────────────
# These are hand-crafted representations of each rune's visual form.
# Some are simplified for terminal rendering; all carry the essential shape.

RUNE_STAVES: dict[str, list[str]] = {
    "ᚠ": [  # Fehu
        "  ╱╲  ",
        " ╱  ╲ ",
        "╱   ╲ ",
        "╱    ╲",
        "     ╲",
    ],
    "ᚢ": [  # Uruz
        " ╱╲  ",
        "╱  ╲ ",
        "╱  ╲ ",
        "╱  ╲ ",
        " ╲╱  ",
    ],
    "ᚦ": [  # Thurisaz
        "  ╱╲ ",
        " ╱  ╲",
        "╱  ╱ ",
        "  ╱  ",
        " ╱   ",
    ],
    "ᚨ": [  # Ansuz
        " ╱╲ ",
        "╱  ╲",
        "╱ ╱ ",
        "╱╱  ",
        "╱   ",
    ],
    "ᚱ": [  # Raidho
        "╲╱╲ ",
        "╲ ╱ ",
        "╲╱  ",
        "╲╱  ",
        "╱   ",
    ],
    "ᚲ": [  # Kenaz
        " ╱╲ ",
        "╱  ╲",
        "╲  ╱",
        " ╲╱ ",
        "    ",
    ],
    "ᚷ": [  # Gebo
        "  ╲╱  ",
        " ╲╱╲╱ ",
        "╲╱  ╲╱",
        "  ╲╱  ",
        "  ╱╲  ",
    ],
    "ᚹ": [  # Wunjo
        " ╱╲  ",
        "╱  ╲ ",
        "╱ ╱╲ ",
        "╱╱ ╱ ",
        "╱ ╱  ",
    ],
    "ᚺ": [  # Hagalaz
        "╲╱╲╱",
        " ╲╱ ",
        "╲╱╲╱",
        " ╲╱ ",
        "╲╱╲╱",
    ],
    "ᚾ": [  # Nauthiz
        "╲╱ ",
        "╲╱ ",
        "╲╱ ",
        "╲╱ ",
        "╲╱ ",
    ],
    "ᛁ": [  # Isa
        " │ ",
        " │ ",
        " │ ",
        " │ ",
        " │ ",
    ],
    "ᛃ": [  # Jera
        " ╱╲╱ ",
        "╱ ╱╲ ",
        "╲╱ ╲ ",
        " ╲╱ ╲",
        "  ╱╲ ",
    ],
    "ᛇ": [  # Eihwaz
        " ╱╲ ",
        "╱  ╲",
        " │  ",
        "╲  ╱",
        " ╲╱ ",
    ],
    "ᛈ": [  # Perthro
        " ╱╲  ",
        "╱  ╲ ",
        "╲ ╱╲ ",
        " ╲╱ ╲",
        "     ",
    ],
    "ᛉ": [  # Algiz
        "  ╱╲  ",
        " ╱ ╲ ",
        "╱   ╲ ",
        "  │  ",
        "  │  ",
    ],
    "ᛊ": [  # Sowilo
        "  ╱╲ ",
        " ╱  ",
        "╱╲╱ ",
        "  ╲╱",
        "   ╲",
    ],
    "ᛏ": [  # Tiwaz
        "  ╱╲  ",
        " ╱  ╲ ",
        "╱    ╲",
        "  │  ",
        "  │  ",
    ],
    "ᛒ": [  # Berkano
        " ╱╲╱ ",
        "╱ ╱╲ ",
        "╲╱ ╲ ",
        "╲ ╱  ",
        " ╲╱  ",
    ],
    "ᛖ": [  # Ehwaz
        "╲╱  ╱╲",
        "╲╱ ╱  ",
        "╲╱╱   ",
        "╲╱    ",
        "  ╱╲  ",
    ],
    "ᛗ": [  # Mannaz
        "╲╱╲╱",
        "╲╱╲╱",
        "╲╱╲╱",
        " ╲╱ ",
        " ╱╲ ",
    ],
    "ᛚ": [  # Laguz
        "╲╱ ",
        " ╲ ",
        "╲╱ ",
        "╲╱ ",
        " ╲ ",
    ],
    "ᛜ": [  # Ingwaz
        " ╱╲╱ ",
        "╱    ╲",
        "╲    ╱",
        " ╲╱╲ ",
        "  ╲╱  ",
    ],
    "ᛞ": [  # Dagaz
        "╲╱╲╱╲",
        " ╲╱ ╱ ",
        "╲╱╲╱╲",
        " ╱╲ ╲ ",
        "╱╲╱╲╱",
    ],
    "ᛟ": [  # Othala
        " ╱╲╱ ",
        "╱    ╲",
        "╲╱╲╱╱ ",
        "╱  ╱ ",
        " ╱╲╱ ",
    ],
}


def render_rune_stave(rune_char: str, width: int = 6) -> str:
    """Render a single rune as ASCII art stave."""
    stave = RUNE_STAVES.get(rune_char)
    if stave:
        return "\n".join(stave)
    # Fallback: just show the unicode character large
    return f"\n  {rune_char}\n"


def render_rune_card(rune: Rune, show_stave: bool = True) -> str:
    """
    Render a detailed rune card for terminal display.

    Shows the rune character, name, stave art, meaning, element,
    keywords, and ætt membership.
    """
    lines = []

    # Top border
    lines.append("┌" + "─" * 32 + "┐")

    # Header with rune character
    header = f"  {rune.unicode}  {rune.name}"
    lines.append("│" + header.ljust(32) + "│")

    # Ætt and position
    aett_line = f"  {rune.aett.value}  ·  Position {rune.global_position}/24"
    lines.append("│" + aett_line.ljust(32) + "│")

    # Separator
    lines.append("├" + "─" * 32 + "┤")

    # Stave art
    if show_stave and rune.unicode in RUNE_STAVES:
        stave = RUNE_STAVES[rune.unicode]
        for line in stave:
            lines.append("│" + line.center(32) + "│")
    else:
        big_rune = f"  {rune.unicode}  "
        lines.append("│" + big_rune.center(32) + "│")

    # Separator
    lines.append("├" + "─" * 32 + "┤")

    # Meaning
    meaning = f"  Meaning: {rune.meaning}"
    if len(meaning) > 32:
        meaning = meaning[:30] + "…"
    lines.append("│" + meaning.ljust(32) + "│")

    # Element
    elem = f"  Element: {rune.element}"
    lines.append("│" + elem.ljust(32) + "│")

    # Keywords
    kw = f"  Keywords: {', '.join(rune.keywords[:3])}"
    if len(kw) > 32:
        kw = kw[:30] + "…"
    lines.append("│" + kw.ljust(32) + "│")

    # Wyrd value
    wyrd = f"  Wyrd Value: {rune.wyrd_value}"
    lines.append("│" + wyrd.ljust(32) + "│")

    # Galdr
    galdr = f"  Galdr: \"{rune.galdr}\""
    if len(galdr) > 32:
        galdr = galdr[:30] + "…\""
    lines.append("│" + galdr.ljust(32) + "│")

    # Bottom border
    lines.append("└" + "─" * 32 + "┘")

    return "\n".join(lines)


def render_futhark_table() -> str:
    """
    Render the complete Elder Futhark as a formatted table.

    Organized by ættir, showing each rune's key properties.
    """
    lines = []

    lines.append("┌" + "─" * 72 + "┐")
    lines.append("│" + "  THE ELDER FUTHARK  ·  ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ  ".center(72) + "│")
    lines.append("├" + "─" * 72 + "┤")

    for aett_name, aett_runes in AETTIR.items():
        lines.append("│" + f"  ══ {aett_name.value} ══".center(72) + "│")
        lines.append("│" + "─" * 72 + "│")

        for rune in aett_runes:
            row = f"  {rune.unicode} {rune.name:<10} | {rune.phonetic:<3} | {rune.element:<5} | W:{rune.wyrd_value:<2} | {rune.meaning}"
            if len(row) > 72:
                row = row[:70] + "…"
            lines.append("│" + row.ljust(72) + "│")

        lines.append("│" + " ".ljust(72) + "│")

    lines.append("└" + "─" * 72 + "┘")

    return "\n".join(lines)


def render_rune_circle(
    radius: int = 8,
    highlight_runes: Optional[list[Rune]] = None,
    title: Optional[str] = None,
) -> str:
    """
    Render the Elder Futhark arranged in a circle in the terminal.

    This creates a visual representation of the futhark as a
    sacred circle, with optional highlighting of specific runes.

    Uses math to place 24 runes around a circle in ASCII.
    """
    import math

    width = radius * 2 + 4
    height = radius + 3
    grid: list[list[str]] = [[" " for _ in range(width)] for _ in range(height)]

    # Place runes around the circle
    for i, rune in enumerate(ELDER_FUTHARK):
        angle = (2 * math.pi * i / 24) - (math.pi / 2)  # Start from top
        x = int(radius + 1 + radius * math.cos(angle))
        y = int((height - 1) / 2 + (radius * 0.45) * math.sin(angle))

        # Clamp to grid bounds
        x = max(1, min(x, width - 2))
        y = max(0, min(y, height - 1))

        char = rune.unicode
        if highlight_runes and rune in highlight_runes:
            char = f"◆{rune.unicode}◆"
            # Simplified: just mark with a star
            char = f"✦{rune.unicode}"

        # Only place if position is empty
        if grid[y][x] == " ":
            grid[y][x] = char

    # Build output
    lines = []
    if title:
        lines.append(f"  {title}")
        lines.append("")

    for row in grid:
        line = "".join(row)
        # Remove trailing spaces for cleaner output
        lines.append(line.rstrip())

    return "\n".join(lines)


def render_spread_visual(spread: Spread, width: int = 60) -> str:
    """
    Render a divination spread with visual card-style output.

    Creates a beautiful terminal visualization showing
    each drawn rune as a card with its properties.
    """
    lines = []

    # Title bar
    lines.append("╔" + "═" * width + "╗")
    title = "ᛟ  RÚNAVÉL  ·  WYRD-READING  ᛟ"
    lines.append("║" + title.center(width) + "║")

    if spread.question:
        lines.append("║" + "─" * width + "║")
        q_line = f"  \"{spread.question}\""
        lines.append("║" + q_line.center(width) + "║")

    lines.append("╠" + "═" * width + "╣")

    # Draw each rune as a card
    for i, drawn in enumerate(spread.runes):
        rune = drawn.rune
        pos_label = drawn.position.value if drawn.position else f"Rune {i+1}"
        rev_text = " ᚨ INVERTED" if drawn.is_reversed else ""

        # Position header
        pos_header = f"  ▸ {pos_label.upper()}{rev_text}"
        lines.append("║" + pos_header.ljust(width) + "║")

        # Rune display with stave
        stave = RUNE_STAVES.get(rune.unicode, [])
        lines.append("║" + f"    {rune.unicode} {rune.name} — {rune.meaning}".ljust(width) + "║")

        if stave:
            for s_line in stave:
                lines.append("║" + f"    {s_line}".ljust(width) + "║")

        # Properties
        lines.append("║" + f"    Ætt: {rune.aett.value}  ·  Element: {rune.element}".ljust(width) + "║")
        lines.append("║" + f"    Keywords: {', '.join(rune.keywords)}".ljust(width) + "║")
        lines.append("║" + f"    Galdr: \"{rune.galdr}\"".ljust(width) + "║")

        if drawn.is_reversed:
            lines.append("║" + "    ⚠ Inverted: energies blocked, delayed, or challenged".ljust(width) + "║")

        lines.append("║" + "    " + "─" * (width - 6) + "║")

    # Synthesis
    lines.append("║" + "  SYNTHESIS".center(width) + "║")
    lines.append("║" + "─" * width + "║")

    # Element tally
    elements = [d.rune.element for d in spread.runes]
    elem_counts = {}
    for e in elements:
        elem_counts[e] = elem_counts.get(e, 0) + 1
    elem_str = "  ".join(f"{e}: {c}" for e, c in elem_counts.items())
    lines.append("║" + f"  Elements: {elem_str}".ljust(width) + "║")

    # Ætt tally
    aett_counts = {}
    for d in spread.runes:
        name = d.rune.aett.value
        aett_counts[name] = aett_counts.get(name, 0) + 1
    aett_str = "  ".join(f"{n}: {c}" for n, c in aett_counts.items())
    lines.append("║" + f"  Ættir: {aett_str}".ljust(width) + "║")

    # Wyrd sum
    wyrd_sum = sum(d.rune.wyrd_value for d in spread.runes)
    lines.append("║" + f"  Wyrd Sum: {wyrd_sum}".ljust(width) + "║")

    lines.append("╚" + "═" * width + "╝")

    return "\n".join(lines)


def render_rune_banner() -> str:
    """Render a decorative Rúnavél banner for the CLI."""
    banner = r"""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║     ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ                     ║
    ║     ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ ᛉ ᛊ                     ║
    ║     ᛏ ᛒ ᛖ ᛗ ᛚ ᛜ ᛞ ᛟ                     ║
    ║                                           ║
    ║        R Ú N A V É L                      ║
    ║        The Rune Machine                    ║
    ║        · Cipher · Divination · Seidhr ·    ║
    ║                                           ║
    ║     Forged by Runa Gridweaver             ║
    ║     Freyjasdottir  ·  May 2026            ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """
    return banner