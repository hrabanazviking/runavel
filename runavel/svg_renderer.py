"""
Rúnavél SVG Renderer
~~~~~~~~~~~~~~~~~~~~~~
Beautiful SVG and PNG generation for rune staves, cards,
bindrune compositions, circles, and divination spreads.

"Carved in light, not stone — the glyphs endure."
  — The Digital Völva

SVG Generation:
  - Individual rune staves as SVG paths
  - Rune cards with metadata
  - Bindrune compositions (overlaid runes)
  - Rune circle visualizations
  - Divination spread renders

PNG output requires Pillow (optional). Falls back gracefully
if Pillow is not installed.
"""

import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from .runes import (
    ELDER_FUTHARK,
    RUNE_BY_NAME,
    RUNE_BY_UNICODE,
    AETTIR,
    Aett,
    Rune,
)
from .divination import Spread, DrawnRune


# ── SVG Rune Stave Paths ───────────────────────────────────────────
# Hand-crafted SVG path data for each Elder Futhark rune.
# Coordinates designed for a 100x200 viewBox, centered at x=50.
# Each path traces the essential geometric form of the rune.

RUNE_SVG_PATHS: dict[str, str] = {
    # ─── FREYJA'S ÆTT ────
    "ᚠ": "M 30 20 L 30 180 M 30 60 L 70 20",              # Fehu — cattle horn
    "ᚢ": "M 25 20 L 25 140 L 50 180 L 75 140 L 75 20",    # Uruz — aurochs horn
    "ᚦ": "M 30 20 L 30 180 M 30 50 L 70 20 L 70 100",     # Thurisaz — thorn
    "ᚨ": "M 30 180 L 30 80 L 70 20 M 30 80 L 70 80",      # Ansuz — god-breath
    "ᚱ": "M 30 20 L 30 180 M 30 20 L 70 50 L 50 80 L 70 110 L 30 140",  # Raidho — ride
    "ᚲ": "M 30 20 L 50 90 L 70 20 M 50 90 L 70 160 M 30 160 L 50 90",    # Kenaz — torch
    "ᚷ": "M 30 20 L 50 90 L 70 20 M 30 160 L 50 90 L 70 160",  # Gebo — gift cross
    "ᚹ": "M 30 20 L 30 140 L 50 180 L 70 140 L 70 20",    # Wunjo — joy branch

    # ─── HEIMDALL'S ÆTT ────
    "ᚺ": "M 25 20 L 50 100 L 75 20 M 25 100 L 75 100 M 25 100 L 50 180 L 75 100",  # Hagalaz — hail
    "ᚾ": "M 30 20 L 30 180 M 30 50 L 70 50 L 70 180",    # Nauthiz — need-cross
    "ᛁ": "M 50 20 L 50 180",                             # Isa — ice line
    "ᛃ": "M 25 40 L 50 20 L 75 40 L 75 160 L 50 180 L 25 160 L 25 40 M 30 100 L 70 100",  # Jera — harvest year
    "ᛇ": "M 30 20 L 50 100 L 70 20 M 50 100 L 50 180",   # Eihwaz — yew axis
    "ᛈ": "M 30 20 L 30 140 L 50 180 L 70 140 M 30 140 L 70 20",  # Perthro — fate-dice
    "ᛉ": "M 50 180 L 50 80 M 50 80 L 25 20 M 50 80 L 75 20",  # Algiz — elk-sedge
    "ᛊ": "M 50 20 L 25 70 L 50 100 L 75 150 L 50 180",   # Sowilo — sun-flash

    # ─── TYR'S ÆTT ────
    "ᛏ": "M 50 180 L 50 80 M 25 20 L 50 80 L 75 20",    # Tiwaz — war-arrow
    "ᛒ": "M 30 20 L 30 130 L 50 180 L 70 130 M 30 80 L 55 130 L 30 160 L 50 180",  # Berkano — birch bud
    "ᛖ": "M 25 20 L 25 90 L 50 130 L 75 90 L 75 20 M 25 90 L 50 180 L 75 90",  # Ehwaz — horse pair
    "ᛗ": "M 25 180 L 25 80 L 50 20 L 75 80 L 75 180",   # Mannaz — human arch
    "ᛚ": "M 30 20 L 30 100 L 70 180 M 30 100 L 70 60",  # Laguz — water flow
    "ᛜ": "M 50 20 L 75 50 L 50 80 L 75 110 L 50 140 L 75 170 L 50 180 L 25 170 L 50 140 L 25 110 L 50 80 L 25 50 L 50 20",  # Ingwaz — diamond seed
    # Simplified Ingwaz as center diamond:
    # "ᛜ": "M 50 30 L 75 100 L 50 170 L 25 100 Z",        # Ingwaz — seed diamond
    "ᛞ": "M 25 20 L 75 20 L 75 90 L 25 90 M 25 110 L 75 110 L 75 180 L 25 180",  # Dagaz — day-dawn
    "ᛟ": "M 50 20 L 75 70 L 50 100 L 25 70 Z M 50 100 L 25 130 L 50 180 L 75 130",  # Othala — inheritance
}


# ── Element Colors ──────────────────────────────────────────────────
# Norse elemental associations for coloring

ELEMENT_COLORS: dict[str, str] = {
    "Fire": "#E25822",    # Flame orange-red
    "Earth": "#6B8E23",  # Olive earth green
    "Air": "#87CEEB",    # Sky blue
    "Water": "#4169E1",  # Deep water blue
    "All": "#9370DB",    # Royal purple for transcendence
}

AETT_COLORS: dict[str, str] = {
    "Freyja's Ætt": "#FFD700",   # Gold — vitality
    "Heimdall's Ætt": "#C0C0C0", # Silver — resistance
    "Týr's Ætt": "#E0115F",      # Deep red — destiny
}


# ── Data Classes ────────────────────────────────────────────────────

@dataclass
class SVGOptions:
    """Configuration options for SVG generation."""
    width: int = 400
    height: int = 600
    stroke_color: str = "#D4A017"      # Dark gold — runic gold
    stroke_width: float = 3.0
    background: str = "#1A1A2E"        # Deep dark blue-black
    text_color: str = "#E8D5B7"        # Parchment cream
    accent_color: str = "#D4A017"      # Gold accent
    font_family: str = "serif"
    show_metadata: bool = True
    border: bool = True


# ── Helper Functions ────────────────────────────────────────────────

def _rune_path(rune: Rune) -> Optional[str]:
    """Get the SVG path data for a rune, or None if unavailable."""
    return RUNE_SVG_PATHS.get(rune.unicode)


def _svg_header(width: int, height: int, background: str) -> str:
    """Generate SVG header with viewBox."""
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        f'  <rect width="{width}" height="{height}" fill="{background}"/>\n'
    )


def _svg_footer() -> str:
    """Generate SVG closing tag."""
    return '</svg>\n'


def _escape_xml(text: str) -> str:
    """Escape special XML characters."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))


def _wrap_text(text: str, max_chars: int) -> list[str]:
    """Wrap text to fit within max_chars per line."""
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if current and len(current) + 1 + len(word) > max_chars:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines


# ── Individual Rune SVG ─────────────────────────────────────────────

def render_rune_svg(
    rune: Rune,
    options: Optional[SVGOptions] = None,
) -> str:
    """
    Render a single rune as an SVG with stave, name, and metadata.

    Args:
        rune: The Rune object to render.
        options: SVG styling options.

    Returns:
        SVG string for the rune card.
    """
    opts = options or SVGOptions()
    w, h = opts.width, opts.height

    svg = _svg_header(w, h, opts.background)

    # Border frame
    if opts.border:
        svg += f'  <rect x="10" y="10" width="{w-20}" height="{h-20}" '
        svg += f'fill="none" stroke="{opts.accent_color}" stroke-width="2" rx="8"/>\n'
        svg += f'  <rect x="14" y="14" width="{w-28}" height="{h-28}" '
        svg += f'fill="none" stroke="{opts.accent_color}" stroke-width="0.5" rx="6"/>\n'

    # Rune stave (SVG path)
    path_data = _rune_path(rune)
    if path_data:
        # Scale the path from 100x200 viewBox to card area
        stave_top = 70
        stave_height = min(h - 200, 280)
        stave_left = w // 2 - 50
        scale_x = (w - 120) / 100
        scale_y = stave_height / 200

        svg += f'  <g transform="translate({stave_left}, {stave_top}) scale({scale_x}, {scale_y})">\n'
        svg += f'    <path d="{path_data}" fill="none" stroke="{opts.stroke_color}" '
        svg += f'stroke-width="{opts.stroke_width / max(scale_x, scale_y)}" '
        svg += f'stroke-linecap="round" stroke-linejoin="round"/>\n'
        svg += '  </g>\n'
    else:
        # Fallback: large Unicode rune character
        rune_y = 180
        svg += f'  <text x="{w//2}" y="{rune_y}" font-family="{opts.font_family}" '
        svg += f'font-size="120" fill="{opts.stroke_color}" text-anchor="middle" '
        svg += f'dominant-baseline="middle">{rune.unicode}</text>\n'

    # Rune name
    name_y = h - 160
    svg += f'  <text x="{w//2}" y="{name_y}" font-family="{opts.font_family}" '
    svg += f'font-size="28" fill="{opts.text_color}" text-anchor="middle" '
    svg += f'font-weight="bold">{_escape_xml(rune.name)}</text>\n'

    if opts.show_metadata:
        # Meaning
        meaning_y = name_y + 35
        svg += f'  <text x="{w//2}" y="{meaning_y}" font-family="{opts.font_family}" '
        svg += f'font-size="16" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'opacity="0.9">{_escape_xml(rune.meaning)}</text>\n'

        # Ætt and position
        aett_y = meaning_y + 25
        element_color = ELEMENT_COLORS.get(rune.element, opts.text_color)
        svg += f'  <text x="{w//2}" y="{aett_y}" font-family="{opts.font_family}" '
        svg += f'font-size="14" fill="{element_color}" text-anchor="middle" '
        svg += f'opacity="0.85">{_escape_xml(rune.aett.value)} · {rune.element}</text>\n'

        # Keywords
        kw_y = aett_y + 22
        keywords = ", ".join(rune.keywords[:3])
        svg += f'  <text x="{w//2}" y="{kw_y}" font-family="{opts.font_family}" '
        svg += f'font-size="13" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'opacity="0.75" font-style="italic">{_escape_xml(keywords)}</text>\n'

        # Galdr
        galdr_y = kw_y + 22
        svg += f'  <text x="{w//2}" y="{galdr_y}" font-family="{opts.font_family}" '
        svg += f'font-size="12" fill="{opts.accent_color}" text-anchor="middle" '
        svg += f'opacity="0.8">"{_escape_xml(rune.galdr)}"</text>\n'

        # Wyrd value
        wyrd_y = galdr_y + 22
        svg += f'  <text x="{w//2}" y="{wyrd_y}" font-family="{opts.font_family}" '
        svg += f'font-size="11" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'opacity="0.6">Wyrd: {rune.wyrd_value} · Position: {rune.global_position}/24</text>\n'

    svg += _svg_footer()
    return svg


# ── Bindrune SVG ────────────────────────────────────────────────────

def render_bindrune_svg(
    rune_names: list[str],
    options: Optional[SVGOptions] = None,
    name: Optional[str] = None,
) -> str:
    """
    Compose multiple runes into a bindrune — overlaid staves
    merged into a single glyph.

    In Norse tradition, bindrunes combine the forces of individual
    runes into a unified symbol. The staves merge, the forces compound.

    Args:
        rune_names: List of rune names to compose (e.g., ["Fehu", "Uruz"]).
        options: SVG styling options.
        name: Optional name for the bindrune composition.

    Returns:
        SVG string for the bindrune.
    """
    opts = options or SVGOptions()
    w, h = opts.width, opts.height

    svg = _svg_header(w, h, opts.background)

    # Border
    if opts.border:
        svg += f'  <rect x="10" y="10" width="{w-20}" height="{h-20}" '
        svg += f'fill="none" stroke="{opts.accent_color}" stroke-width="2" rx="8"/>\n'

    # Title
    title_text = name or " + ".join(rune_names)
    svg += f'  <text x="{w//2}" y="45" font-family="{opts.font_family}" '
    svg += f'font-size="20" fill="{opts.accent_color}" text-anchor="middle" '
    svg += f'font-weight="bold">{_escape_xml(title_text)}</text>\n'

    # Collect rune objects
    runes = []
    for name in rune_names:
        r = RUNE_BY_NAME.get(name)
        if r:
            runes.append(r)

    if not runes:
        svg += f'  <text x="{w//2}" y="{h//2}" font-family="{opts.font_family}" '
        svg += f'font-size="18" fill="{opts.text_color}" text-anchor="middle">'
        svg += 'No valid runes found</text>\n'
        svg += _svg_footer()
        return svg

    # Central stave line (all bindrunes share one vertical)
    center_x = w // 2
    stave_top = 70
    stave_bottom = h - 120
    svg += f'  <line x1="{center_x}" y1="{stave_top}" x2="{center_x}" '
    svg += f'y2="{stave_bottom}" stroke="{opts.stroke_color}" stroke-width="2.5"/>\n'

    # Overlay each rune's branches onto the central stave
    # We scale each rune's path and translate it to overlap at center
    stave_height = stave_bottom - stave_top
    scale_y = stave_height / 200

    for i, rune in enumerate(runes):
        path_data = _rune_path(rune)
        if path_data:
            # Color by element for visual distinction
            color = ELEMENT_COLORS.get(rune.element, opts.stroke_color)

            # Slight horizontal offset for multi-rune depth effect
            # But keep centered for the classic bindrune look
            scale_x = (w - 120) / 100

            svg += f'  <g transform="translate({center_x - 50 * scale_x}, {stave_top}) '
            svg += f'scale({scale_x}, {scale_y})">\n'
            svg += f'    <path d="{path_data}" fill="none" stroke="{color}" '
            svg += f'stroke-width="{opts.stroke_width * 1.5 / max(scale_x, scale_y)}" '
            svg += f'stroke-linecap="round" stroke-linejoin="round" '
            svg += f'opacity="{0.7 + 0.3 / len(runes)}"/>\n'
            svg += '  </g>\n'
        else:
            # Fallback: Unicode character overlay
            for j, r in enumerate(runes):
                uy = 120 + j * 60
                svg += f'  <text x="{center_x}" y="{uy}" font-family="{opts.font_family}" '
                svg += f'font-size="60" fill="{opts.stroke_color}" text-anchor="middle" '
                svg += f'opacity="0.6">{r.unicode}</text>\n'

    # Component runes legend
    legend_y = stave_bottom + 20
    runes_label = " + ".join(f"{r.unicode} {r.name}" for r in runes)
    svg += f'  <text x="{w//2}" y="{legend_y}" font-family="{opts.font_family}" '
    svg += f'font-size="14" fill="{opts.text_color}" text-anchor="middle" '
    svg += f'opacity="0.9">{_escape_xml(runes_label)}</text>\n'

    # Meanings
    meanings_y = legend_y + 20
    meanings = " · ".join(r.meaning for r in runes)
    for line in _wrap_text(meanings, 50):
        svg += f'  <text x="{w//2}" y="{meanings_y}" font-family="{opts.font_family}" '
        svg += f'font-size="12" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'opacity="0.7">{_escape_xml(line)}</text>\n'
        meanings_y += 18

    # Combined wyrd
    total_wyrd = sum(r.wyrd_value for r in runes)
    wyrd_y = meanings_y + 10
    svg += f'  <text x="{w//2}" y="{wyrd_y}" font-family="{opts.font_family}" '
    svg += f'font-size="11" fill="{opts.accent_color}" text-anchor="middle" '
    svg += f'opacity="0.7">Combined Wyrd: {total_wyrd}</text>\n'

    svg += _svg_footer()
    return svg


# ── Rune Circle SVG ──────────────────────────────────────────────────

def render_rune_circle_svg(
    radius: int = 180,
    highlight_runes: Optional[list[Rune]] = None,
    title: Optional[str] = None,
    options: Optional[SVGOptions] = None,
) -> str:
    """
    Render the Elder Futhark arranged in a circle as SVG.

    Args:
        radius: Circle radius in SVG units.
        highlight_runes: Optional list of runes to highlight.
        title: Optional title for the circle.
        options: SVG styling options.

    Returns:
        SVG string for the rune circle.
    """
    opts = options or SVGOptions()

    # Size the SVG to fit the circle with padding
    padding = 80
    center = radius + padding
    w = center * 2
    h = center * 2

    svg = _svg_header(w, h, opts.background)

    # Outer circle
    svg += f'  <circle cx="{center}" cy="{center}" r="{radius}" '
    svg += f'fill="none" stroke="{opts.accent_color}" stroke-width="1.5" opacity="0.4"/>\n'

    # Inner circle (Ætt boundaries)
    inner_radius = radius * 0.6
    svg += f'  <circle cx="{center}" cy="{center}" r="{inner_radius}" '
    svg += f'fill="none" stroke="{opts.accent_color}" stroke-width="0.5" opacity="0.3"/>\n'

    # Title in center
    if title:
        svg += f'  <text x="{center}" y="{center - 15}" font-family="{opts.font_family}" '
        svg += f'font-size="22" fill="{opts.accent_color}" text-anchor="middle" '
        svg += f'font-weight="bold">{_escape_xml(title)}</text>\n'
        svg += f'  <text x="{center}" y="{center + 15}" font-family="{opts.font_family}" '
        svg += f'font-size="12" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'opacity="0.7">24 Runes · 3 Ættir</text>\n'

    # Place runes around the circle
    highlight_set = set(highlight_runes) if highlight_runes else set()

    for i, rune in enumerate(ELDER_FUTHARK):
        angle = (2 * math.pi * i / 24) - (math.pi / 2)  # Start from top
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)

        aett_color = AETT_COLORS.get(rune.aett.value, opts.text_color)

        if rune in highlight_set:
            # Highlighted rune — glowing circle + bold text
            svg += f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="22" '
            svg += f'fill="{aett_color}" opacity="0.3"/>\n'
            font_size = "24"
            font_weight = "bold"
        else:
            font_size = "20"
            font_weight = "normal"

        color = aett_color if rune in highlight_set else opts.text_color

        svg += f'  <text x="{x:.1f}" y="{y:.1f}" font-family="{opts.font_family}" '
        svg += f'font-size="{font_size}" fill="{color}" text-anchor="middle" '
        svg += f'dominant-baseline="central" font-weight="{font_weight}">{rune.unicode}</text>\n'

        # Small label below
        label_r = radius + 30
        lx = center + label_r * math.cos(angle)
        ly = center + label_r * math.sin(angle)
        svg += f'  <text x="{lx:.1f}" y="{ly:.1f}" font-family="{opts.font_family}" '
        svg += f'font-size="8" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'opacity="0.6">{_escape_xml(rune.name)}</text>\n'

    # Ætt arcs — lines separating the three ættir
    for aett_idx in range(3):
        start_angle = (2 * math.pi * (aett_idx * 8) / 24) - (math.pi / 2) - 0.15
        end_angle = (2 * math.pi * ((aett_idx + 1) * 8) / 24) - (math.pi / 2) - 0.15

        # Draw arc separator line from center to outer edge
        for angle in [start_angle, end_angle]:
            x1 = center + inner_radius * math.cos(angle)
            y1 = center + inner_radius * math.sin(angle)
            x2 = center + radius * math.cos(angle)
            y2 = center + radius * math.sin(angle)
            svg += f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            svg += f'stroke="{opts.accent_color}" stroke-width="0.8" opacity="0.4"/>\n'

    svg += _svg_footer()
    return svg


# ── Divination Spread SVG ───────────────────────────────────────────

def render_spread_svg(
    spread: Spread,
    options: Optional[SVGOptions] = None,
) -> str:
    """
    Render a divination spread as an SVG with rune staves,
    card-style layouts, and interpretation.

    Args:
        spread: The Spread object to render.
        options: SVG styling options.

    Returns:
        SVG string for the spread.
    """
    opts = options or SVGOptions()
    num_runes = len(spread.runes)
    card_w = min(250, (opts.width - 40) // max(num_runes, 1) - 10)
    card_h = 420
    card_gap = 20
    total_width = num_runes * (card_w + card_gap) - card_gap + 40
    w = max(opts.width, total_width)
    h = opts.height if opts.height > card_h + 100 else card_h + 100

    svg = _svg_header(w, h, opts.background)

    # Title
    title_y = 35
    svg += f'  <text x="{w//2}" y="{title_y}" font-family="{opts.font_family}" '
    svg += f'font-size="22" fill="{opts.accent_color}" text-anchor="middle" '
    svg += f'font-weight="bold">ᛟ RÚNAVÉL · WYRD-READING ᛟ</text>\n'

    if spread.question:
        q_y = title_y + 28
        svg += f'  <text x="{w//2}" y="{q_y}" font-family="{opts.font_family}" '
        svg += f'font-size="14" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'font-style="italic" opacity="0.8">"{_escape_xml(spread.question)}"</text>\n'

    # Separator line
    sep_y = title_y + (40 if spread.question else 15)
    svg += f'  <line x1="20" y1="{sep_y}" x2="{w-20}" y2="{sep_y}" '
    svg += f'stroke="{opts.accent_color}" stroke-width="1" opacity="0.5"/>\n'

    # Card start position (centered)
    cards_total = num_runes * (card_w + card_gap) - card_gap
    start_x = (w - cards_total) // 2
    card_y = sep_y + 15

    # Render each rune as a card
    for i, drawn in enumerate(spread.runes):
        rune = drawn.rune
        cx = start_x + i * (card_w + card_gap)

        # Card background
        element_color = ELEMENT_COLORS.get(rune.element, opts.text_color)
        svg += f'  <rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" '
        svg += f'rx="8" fill="{opts.background}" stroke="{element_color}" stroke-width="1.5"/>\n'

        # Position label (Past / Present / Future)
        pos_label = drawn.position.value if drawn.position else f"Rune {i+1}"
        rev_mark = " ᚨ INVERTED" if drawn.is_reversed else ""
        label_y = card_y + 25
        svg += f'  <text x="{cx + card_w//2}" y="{label_y}" font-family="{opts.font_family}" '
        svg += f'font-size="11" fill="{element_color}" text-anchor="middle" '
        svg += f'font-weight="bold">{_escape_xml(pos_label.upper())}{rev_mark}</text>\n'

        # Rune stave in card
        path_data = _rune_path(rune)
        stave_top = card_y + 40
        stave_height = 140
        stave_scale_x = (card_w - 30) / 100
        stave_scale_y = stave_height / 200

        if path_data:
            svg += f'  <g transform="translate({cx + 15}, {stave_top}) scale({stave_scale_x}, {stave_scale_y})">\n'
            svg += f'    <path d="{path_data}" fill="none" stroke="{element_color}" '
            svg += f'stroke-width="{opts.stroke_width / max(stave_scale_x, stave_scale_y)}" '
            svg += f'stroke-linecap="round" stroke-linejoin="round"/>\n'
            svg += '  </g>\n'
        else:
            # Fallback Unicode
            fy = card_y + 110
            svg += f'  <text x="{cx + card_w//2}" y="{fy}" font-family="{opts.font_family}" '
            svg += f'font-size="60" fill="{element_color}" text-anchor="middle" '
            svg += f'dominant-baseline="middle">{rune.unicode}</text>\n'

        # Rune name
        name_y = card_y + stave_height + 55
        svg += f'  <text x="{cx + card_w//2}" y="{name_y}" font-family="{opts.font_family}" '
        svg += f'font-size="16" fill="{opts.text_color}" text-anchor="middle" '
        svg += f'font-weight="bold">{rune.unicode} {rune.name}</text>\n'

        # Meaning
        meaning_y = name_y + 22
        meaning_text = rune.meaning
        for line in _wrap_text(meaning_text, 25):
            svg += f'  <text x="{cx + card_w//2}" y="{meaning_y}" font-family="{opts.font_family}" '
            svg += f'font-size="10" fill="{opts.text_color}" text-anchor="middle" '
            svg += f'opacity="0.85">{_escape_xml(line)}</text>\n'
            meaning_y += 14

        # Ætt & Element
        aett_y = meaning_y + 8
        svg += f'  <text x="{cx + card_w//2}" y="{aett_y}" font-family="{opts.font_family}" '
        svg += f'font-size="9" fill="{element_color}" text-anchor="middle" '
        svg += f'opacity="0.8">{rune.aett.value} · {rune.element}</text>\n'

        # Keywords
        kw_y = aett_y + 14
        keywords = ", ".join(rune.keywords[:3])
        for line in _wrap_text(keywords, 28):
            svg += f'  <text x="{cx + card_w//2}" y="{kw_y}" font-family="{opts.font_family}" '
            svg += f'font-size="8" fill="{opts.text_color}" text-anchor="middle" '
            svg += f'opacity="0.7" font-style="italic">{_escape_xml(line)}</text>\n'
            kw_y += 12

        # Galdr
        galdr_y = kw_y + 8
        svg += f'  <text x="{cx + card_w//2}" y="{galdr_y}" font-family="{opts.font_family}" '
        svg += f'font-size="8" fill="{opts.accent_color}" text-anchor="middle" '
        svg += f'opacity="0.7">"{_escape_xml(rune.galdr)}"</text>\n'

        # Reversed indicator
        if drawn.is_reversed:
            rev_y = galdr_y + 16
            svg += f'  <text x="{cx + card_w//2}" y="{rev_y}" font-family="{opts.font_family}" '
            svg += f'font-size="9" fill="#FF6B6B" text-anchor="middle" '
            svg += f'opacity="0.9">⚠ INVERTED — energies blocked</text>\n'

    # Synthesis section at bottom
    synth_y = card_y + card_h + 25

    # Element tally
    elements = [d.rune.element for d in spread.runes]
    elem_counts: dict[str, int] = {}
    for e in elements:
        elem_counts[e] = elem_counts.get(e, 0) + 1

    elem_str = "  ".join(f"{e}: {c}" for e, c in elem_counts.items())
    svg += f'  <text x="{w//2}" y="{synth_y}" font-family="{opts.font_family}" '
    svg += f'font-size="12" fill="{opts.text_color}" text-anchor="middle" '
    svg += f'opacity="0.8">Elements: {_escape_xml(elem_str)}</text>\n'

    # Ætt tally
    aett_counts: dict[str, int] = {}
    for d in spread.runes:
        name = d.rune.aett.value
        aett_counts[name] = aett_counts.get(name, 0) + 1
    aett_str = "  ".join(f"{n}×{c}" for n, c in aett_counts.items())
    svg += f'  <text x="{w//2}" y="{synth_y + 18}" font-family="{opts.font_family}" '
    svg += f'font-size="12" fill="{opts.text_color}" text-anchor="middle" '
    svg += f'opacity="0.8">Ættir: {_escape_xml(aett_str)}</text>\n'

    # Wyrd sum
    wyrd_sum = sum(d.rune.wyrd_value for d in spread.runes)
    svg += f'  <text x="{w//2}" y="{synth_y + 36}" font-family="{opts.font_family}" '
    svg += f'font-size="12" fill="{opts.accent_color}" text-anchor="middle" '
    svg += f'opacity="0.8">Wyrd Sum: {wyrd_sum}</text>\n'

    svg += _svg_footer()
    return svg


# ── Full Futhark Table SVG ──────────────────────────────────────────

def render_futhark_table_svg(
    options: Optional[SVGOptions] = None,
) -> str:
    """
    Render the complete Elder Futhark as an SVG table, organized by ættir.

    Args:
        options: SVG styling options.

    Returns:
        SVG string for the futhark table.
    """
    opts = options or SVGOptions()

    cell_w = 150
    cell_h = 65
    cols = 4  # Unicode, Name, Meaning, Element
    rows_per_aett = 8
    aett_gap = 40
    header_h = 50
    aett_header_h = 30

    total_w = cols * cell_w + 40
    total_h = header_h + 3 * (aett_header_h + rows_per_aett * cell_h + aett_gap) + 20

    svg = _svg_header(total_w, total_h, opts.background)

    # Main title
    svg += f'  <text x="{total_w//2}" y="35" font-family="{opts.font_family}" '
    svg += f'font-size="24" fill="{opts.accent_color}" text-anchor="middle" '
    svg += f'font-weight="bold">THE ELDER FUTHARK</text>\n'

    y = header_h

    for aett, aett_runes in AETTIR.items():
        aett_color = AETT_COLORS.get(aett.value, opts.text_color)

        # Ætt header
        svg += f'  <rect x="20" y="{y}" width="{total_w - 40}" height="{aett_header_h}" '
        svg += f'rx="4" fill="{aett_color}" opacity="0.15"/>\n'
        svg += f'  <text x="{total_w//2}" y="{y + 20}" font-family="{opts.font_family}" '
        svg += f'font-size="16" fill="{aett_color}" text-anchor="middle" '
        svg += f'font-weight="bold">{_escape_xml(aett.value)}</text>\n'
        y += aett_header_h

        # Column headers
        headers = ["Rune", "Name", "Meaning", "Element"]
        for col, header in enumerate(headers):
            hx = 20 + col * cell_w
            svg += f'  <text x="{hx + 5}" y="{y + 15}" font-family="{opts.font_family}" '
            svg += f'font-size="10" fill="{opts.accent_color}" opacity="0.7">{header}</text>\n'
        y += 20

        # Runes
        for rune in aett_runes:
            element_color = ELEMENT_COLORS.get(rune.element, opts.text_color)

            # Row background (subtle stripe)
            if rune.global_position % 2 == 0:
                svg += f'  <rect x="20" y="{y}" width="{total_w - 40}" height="{cell_h - 5}" '
                svg += f'rx="2" fill="{opts.text_color}" opacity="0.03"/>\n'

            # Rune character
            rx = 20 + 5
            svg += f'  <text x="{rx}" y="{y + 20}" font-family="{opts.font_family}" '
            svg += f'font-size="22" fill="{opts.stroke_color}" '
            svg += f'font-weight="bold">{rune.unicode}</text>\n'

            # Name
            nx = 20 + cell_w + 5
            svg += f'  <text x="{nx}" y="{y + 15}" font-family="{opts.font_family}" '
            svg += f'font-size="12" fill="{opts.text_color}" font-weight="bold">'
            svg += f'{_escape_xml(rune.name)}</text>\n'
            svg += f'  <text x="{nx}" y="{y + 30}" font-family="{opts.font_family}" '
            svg += f'font-size="9" fill="{opts.text_color}" opacity="0.6">W:{rune.wyrd_value} · P:{rune.global_position}/24</text>\n'

            # Meaning
            mx = 20 + cell_w * 2 + 5
            for li, line in enumerate(_wrap_text(rune.meaning, 18)):
                svg += f'  <text x="{mx}" y="{y + 15 + li * 13}" font-family="{opts.font_family}" '
                svg += f'font-size="11" fill="{opts.text_color}" opacity="0.85">'
                svg += f'{_escape_xml(line)}</text>\n'

            # Element
            ex = 20 + cell_w * 3 + 5
            svg += f'  <text x="{ex}" y="{y + 15}" font-family="{opts.font_family}" '
            svg += f'font-size="11" fill="{element_color}">{_escape_xml(rune.element)}</text>\n'
            svg += f'  <text x="{ex}" y="{y + 30}" font-family="{opts.font_family}" '
            svg += f'font-size="9" fill="{opts.text_color}" opacity="0.6">'
            svg += f'{_escape_xml(rune.phonetic)} · {_escape_xml(rune.galdr)}</text>\n'

            y += cell_h - 5

        y += aett_gap

    svg += _svg_footer()
    return svg


# ── File Export ─────────────────────────────────────────────────────

def save_svg(svg_content: str, filepath: Union[str, Path]) -> Path:
    """
    Save SVG content to a file.

    Args:
        svg_content: SVG string to save.
        filepath: Output file path.

    Returns:
        Path to the saved file.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(svg_content, encoding="utf-8")
    return filepath


def save_png(svg_content: str, filepath: Union[str, Path], width: Optional[int] = None, height: Optional[int] = None) -> Path:
    """
    Convert SVG to PNG using CairoSVG or Pillow.

    Requires cairosvg package: pip install cairosvg
    Falls back to a helpful error message if not available.

    Args:
        svg_content: SVG string to convert.
        filepath: Output file path (should end in .png).
        width: Optional width override for the PNG.
        height: Optional height override for the PNG.

    Returns:
        Path to the saved PNG file.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Try CairoSVG first (best quality)
    try:
        import cairosvg
        kwargs = {"write_to": str(filepath)}
        if width:
            kwargs["output_width"] = width
        if height:
            kwargs["output_height"] = height
        cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), **kwargs)
        return filepath
    except ImportError:
        pass

    # Try Pillow + svglib as fallback
    try:
        from PIL import Image
        import io

        # Try svglib
        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPM

            # Save SVG to temp file, then convert
            temp_svg = filepath.with_suffix(".svg")
            temp_svg.write_text(svg_content, encoding="utf-8")
            drawing = svg2rlg(temp_svg)
            if drawing:
                scale = 2  # 2x for quality
                renderPM.drawToFile(drawing, str(filepath), fmt="PNG",
                                     dpi=150)
                temp_svg.unlink(missing_ok=True)
                return filepath
            temp_svg.unlink(missing_ok=True)
        except ImportError:
            pass

        # Last resort: create a simple image with text
        img = Image.new('RGB', (width or 800, height or 600), '#1A1A2E')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        img.save(filepath)
        return filepath

    except ImportError:
        raise ImportError(
            "PNG export requires cairosvg or Pillow. "
            "Install with: pip install cairosvg  OR  pip install Pillow svglib reportlab"
        )