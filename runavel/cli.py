#!/usr/bin/env python3
"""
Rúnavél CLI — The Rune Machine Command Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:
    runavel encode <text>           Encode text to runes (substitution mode)
    runavel decode <runes>          Decode runes to text
    runavel shift <text> [key]      Encode with shift cipher
    runavel unshift <runes> [key]   Decode shift cipher
    runavel wyrd <text>             Encode with wyrd numerology
    runavel draw                     Draw a single rune
    runavel spread [question]        Draw a three-rune spread
    runavel aett-spread [question]   Draw one rune per ætt
    runavel futhark                  Display the full futhark table
    runavel info <rune>              Show detailed rune information
    runavel banner                   Display the Rúnavél banner
    runavel render-rune <rune>       Render a single rune as SVG
    runavel render-bindrune <names> Compose multiple runes into a bindrune
    runavel render-spread [question] Render a divination spread as SVG
    runavel render-circle            Render the futhark circle as SVG
    runavel render-futhark           Render the full futhark table as SVG

Examples:
    runavel encode "Hello world"
    runavel shift "Secret message" 7
    runavel spread "What guides my path?"
    runavel info Fehu
    runavel render-rune Fehu -o fehu.svg
    runavel render-bindrune Fehu Uruz -o protection.svg
    runavel render-spread "What guides my path?" -o reading.svg
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .runes import RUNE_BY_NAME, ELDER_FUTHARK, AETTIR, Aett
from .cipher import RunicCipher, CipherMode
from .divination import Divination, SpreadType
from .renderer import (
    render_rune_card,
    render_rune_banner,
    render_futhark_table,
    render_spread_visual,
)
from .svg_renderer import (
    SVGOptions,
    render_rune_svg,
    render_bindrune_svg,
    render_rune_circle_svg,
    render_spread_svg,
    render_futhark_table_svg,
    save_svg,
    save_png,
)


def cmd_encode(args):
    """Encode text to runes using substitution cipher."""
    cipher = RunicCipher(mode=CipherMode.SUBSTITUTION)
    result = cipher.encode(args.text)
    print(f"\n  Input:  {args.text}")
    print(f"  Runes:  {result}\n")


def cmd_decode(args):
    """Decode runes to text."""
    cipher = RunicCipher(mode=CipherMode.SUBSTITUTION)
    result = cipher.decode(args.runes)
    print(f"\n  Runes:  {args.runes}")
    print(f"  Text:   {result}\n")


def cmd_shift_encode(args):
    """Encode text using shift cipher."""
    key = args.key or 3  # Þurs-based default (Thurisaz = 3)
    cipher = RunicCipher(mode=CipherMode.SHIFT, key=key)
    result = cipher.encode(args.text)
    print(f"\n  Input:  {args.text}")
    print(f"  Key:    {key} (Þurs-shift)")
    print(f"  Runes:  {result}\n")


def cmd_shift_decode(args):
    """Decode shift cipher."""
    key = args.key or 3
    cipher = RunicCipher(mode=CipherMode.SHIFT, key=key)
    result = cipher.decode(args.runes)
    print(f"\n  Runes:  {args.runes}")
    print(f"  Key:    {key} (Þurs-shift)")
    print(f"  Text:   {result}\n")


def cmd_wyrd_encode(args):
    """Encode text using wyrd numerology."""
    cipher = RunicCipher(mode=CipherMode.WYRD)
    result = cipher.encode(args.text)
    print(f"\n  Input:  {args.text}")
    print(f"  Wyrd:   {result}")

    # Show analysis
    analysis = cipher.analyze(result)
    print("\n  Wyrd Analysis:")
    for item in analysis:
        if item["type"] == "rune":
            rune = item["rune"]
            print(f"    {rune.unicode} {rune.name:<10} (W:{rune.wyrd_value:<2}) {rune.meaning}")
        elif item["type"] == "space":
            print(f"    · (separator)")
    print()


def cmd_draw(args):
    """Draw a single rune."""
    div = Divination()
    spread = div.draw_single(question=args.question)
    drawn = spread.runes[0]

    print()
    print(render_rune_card(drawn.rune))
    if drawn.is_reversed:
        print(f"\n  ⚠ {drawn.rune.name} is INVERTED — energies may be blocked or delayed.")
    print(f"\n  \"{drawn.rune.description}\"")
    print()


def cmd_spread(args):
    """Draw a three-rune spread."""
    question = args.question if args.question else None
    div = Divination()

    if args.aett:
        spread = div.draw_three_aett(question=question)
    else:
        spread = div.draw_three_rune(question=question)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spread.timestamp = timestamp

    print()
    print(render_spread_visual(spread))
    print()

    # Show interpretation
    interpretation = div.interpret(spread)
    print(interpretation)
    print()


def cmd_futhark(args):
    """Display the full Elder Futhark."""
    print()
    print(render_futhark_table())
    print()

    # Show some statistics
    print(f"  Total runes: {len(ELDER_FUTHARK)}")
    print(f"  Ættir: {len(AETTIR)}")
    for aett, runes in AETTIR.items():
        print(f"    {aett.value}: {', '.join(r.unicode + ' ' + r.name for r in runes)}")
    print()


def cmd_info(args):
    """Show detailed information about a specific rune."""
    name = args.rune.capitalize()
    if name not in RUNE_BY_NAME:
        # Try matching by unicode character
        for rune in ELDER_FUTHARK:
            if rune.unicode == args.rune:
                name = rune.name
                break
        else:
            print(f"\n  Unknown rune: {args.rune}")
            print(f"  Available runes: {', '.join(r.name for r in ELDER_FUTHARK)}\n")
            return

    rune = RUNE_BY_NAME[name]
    print()
    print(render_rune_card(rune))
    print()
    print(f"  Description: {rune.description}")
    print(f"  All Keywords: {', '.join(rune.keywords)}")
    print(f"  Galdr Chant:  \"{rune.galdr}\"")
    print(f"  Reversible:   {'Yes' if rune.is_reversible else 'No'}")
    if rune.is_reversible and rune.inverse:
        print(f"  Inverse Form: {rune.inverse}")
    print()


def cmd_banner(args):
    """Display the Rúnavél banner."""
    print(render_rune_banner())


def _resolve_output_path(args, default_name: str) -> Path:
    """Resolve output path from args or generate default."""
    if args.output:
        return Path(args.output)
    # Default to current directory
    return Path(default_name)


def _build_svg_options(args) -> SVGOptions:
    """Build SVGOptions from CLI args (style customization)."""
    kwargs = {
        "width": getattr(args, "width", 400),
        "height": getattr(args, "height", 600),
    }
    if hasattr(args, "stroke_color") and args.stroke_color:
        kwargs["stroke_color"] = args.stroke_color
    if hasattr(args, "background") and args.background:
        kwargs["background"] = args.background
    if hasattr(args, "text_color") and args.text_color:
        kwargs["text_color"] = args.text_color
    if hasattr(args, "accent_color") and args.accent_color:
        kwargs["accent_color"] = args.accent_color
    if hasattr(args, "no_metadata"):
        kwargs["show_metadata"] = not args.no_metadata
    if hasattr(args, "no_border"):
        kwargs["border"] = not args.no_border
    return SVGOptions(**kwargs)


def _write_svg_or_png(svg_content: str, filepath: Path):
    """Write SVG content to file, optionally converting to PNG."""
    if filepath.suffix.lower() == ".png":
        try:
            save_png(svg_content, filepath)
            print(f"\n  ✨ Written: {filepath}")
        except ImportError as e:
            print(f"\n  ⚠ PNG export requires cairosvg: {e}")
            print(f"  Falling back to SVG...")
            svg_path = filepath.with_suffix(".svg")
            save_svg(svg_content, svg_path)
            print(f"\n  ✨ Written: {svg_path}")
    else:
        save_svg(svg_content, filepath)
        print(f"\n  ✨ Written: {filepath}")


def cmd_render_rune(args):
    """Render a single rune as SVG/PNG."""
    name = args.rune.capitalize()
    if name not in RUNE_BY_NAME:
        # Try matching by unicode character
        for rune in ELDER_FUTHARK:
            if rune.unicode == args.rune:
                name = rune.name
                break
        else:
            print(f"\n  Unknown rune: {args.rune}")
            print(f"  Available runes: {', '.join(r.name for r in ELDER_FUTHARK)}\n")
            return

    rune = RUNE_BY_NAME[name]
    opts = _build_svg_options(args)
    svg = render_rune_svg(rune, options=opts)

    if args.output:
        filepath = Path(args.output)
    else:
        filepath = Path(f"{rune.name.lower()}.svg")

    _write_svg_or_png(svg, filepath)


def cmd_render_bindrune(args):
    """Compose multiple runes into a bindrune SVG/PNG."""
    rune_names = [name.capitalize() for name in args.runes]
    # Validate
    for name in rune_names:
        if name not in RUNE_BY_NAME:
            print(f"\n  Unknown rune: {name}")
            print(f"  Available runes: {', '.join(r.name for r in ELDER_FUTHARK)}\n")
            return

    opts = _build_svg_options(args)
    svg = render_bindrune_svg(rune_names, options=opts, name=args.name)

    if args.output:
        filepath = Path(args.output)
    else:
        bindrune_name = "-".join(rune_names).lower()
        filepath = Path(f"bindrune-{bindrune_name}.svg")

    _write_svg_or_png(svg, filepath)


def cmd_render_spread(args):
    """Render a divination spread as SVG/PNG."""
    question = args.question
    div = Divination(seed=getattr(args, 'seed', None))

    if args.aett:
        spread = div.draw_three_aett(question=question)
    else:
        spread = div.draw_three_rune(question=question)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spread.timestamp = timestamp

    opts = _build_svg_options(args)
    svg = render_spread_svg(spread, options=opts)

    if args.output:
        filepath = Path(args.output)
    else:
        timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = Path(f"spread-{timestamp_file}.svg")

    _write_svg_or_png(svg, filepath)

    # Also show the terminal interpretation
    print()
    interpretation = div.interpret(spread)
    print(interpretation)
    print()


def cmd_render_circle(args):
    """Render the futhark circle as SVG/PNG."""
    highlight = []
    if args.highlight:
        for name in args.highlight:
            r = RUNE_BY_NAME.get(name.capitalize())
            if r:
                highlight.append(r)
            else:
                print(f"  Warning: Unknown rune '{name}', skipping highlight")

    opts = _build_svg_options(args)
    svg = render_rune_circle_svg(
        radius=args.radius,
        highlight_runes=highlight if highlight else None,
        title=args.title,
        options=opts,
    )

    if args.output:
        filepath = Path(args.output)
    else:
        filepath = Path("futhark-circle.svg")

    _write_svg_or_png(svg, filepath)


def cmd_render_futhark(args):
    """Render the full futhark table as SVG/PNG."""
    opts = _build_svg_options(args)
    svg = render_futhark_table_svg(options=opts)

    if args.output:
        filepath = Path(args.output)
    else:
        filepath = Path("futhark-table.svg")

    _write_svg_or_png(svg, filepath)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="runavel",
        description="Rúnavél — The Rune Machine. Cipher, divination, and visualization for the Elder Futhark.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # encode
    p_encode = subparsers.add_parser("encode", help="Encode text to runes (substitution mode)")
    p_encode.add_argument("text", help="Text to encode")
    p_encode.set_defaults(func=cmd_encode)

    # decode
    p_decode = subparsers.add_parser("decode", help="Decode runes to text")
    p_decode.add_argument("runes", help="Runic text to decode")
    p_decode.set_defaults(func=cmd_decode)

    # shift (Caesar-style)
    p_shift = subparsers.add_parser("shift", help="Encode text with shift cipher")
    p_shift.add_argument("text", help="Text to encode")
    p_shift.add_argument("key", type=int, nargs="?", default=None,
                         help="Shift key (default: 3, Þurs-shift)")
    p_shift.set_defaults(func=cmd_shift_encode)

    # unshift
    p_unshift = subparsers.add_parser("unshift", help="Decode shift cipher")
    p_unshift.add_argument("runes", help="Runic text to decode")
    p_unshift.add_argument("key", type=int, nargs="?", default=None,
                           help="Shift key (default: 3)")
    p_unshift.set_defaults(func=cmd_shift_decode)

    # wyrd
    p_wyrd = subparsers.add_parser("wyrd", help="Encode text with wyrd numerology")
    p_wyrd.add_argument("text", help="Text to encode")
    p_wyrd.set_defaults(func=cmd_wyrd_encode)

    # draw
    p_draw = subparsers.add_parser("draw", help="Draw a single rune")
    p_draw.add_argument("-q", "--question", help="Optional question for the draw")
    p_draw.set_defaults(func=cmd_draw)

    # spread
    p_spread = subparsers.add_parser("spread", help="Draw a three-rune spread")
    p_spread.add_argument("question", nargs="?", default=None,
                          help="Optional question for the spread")
    p_spread.add_argument("--aett", action="store_true",
                          help="Draw one rune from each ætt instead")
    p_spread.set_defaults(func=cmd_spread)

    # futhark
    p_futhark = subparsers.add_parser("futhark", help="Display the full Elder Futhark")
    p_futhark.set_defaults(func=cmd_futhark)

    # info
    p_info = subparsers.add_parser("info", help="Show detailed rune information")
    p_info.add_argument("rune", help="Rune name (e.g., 'Fehu') or Unicode character")
    p_info.set_defaults(func=cmd_info)

    # banner
    p_banner = subparsers.add_parser("banner", help="Display the Rúnavél banner")
    p_banner.set_defaults(func=cmd_banner)

    # ── SVG Render Commands ────────────────────────────────────────

    # Shared style arguments for all render commands
    def _add_style_args(parser, default_w=400, default_h=600):
        """Add common SVG style arguments to a render subparser."""
        parser.add_argument("-o", "--output", help="Output file path (.svg or .png)")
        parser.add_argument("--width", type=int, default=default_w, help=f"SVG width (default: {default_w})")
        parser.add_argument("--height", type=int, default=default_h, help=f"SVG height (default: {default_h})")
        parser.add_argument("--stroke-color", help="Rune stroke color (hex, e.g. #D4A017)")
        parser.add_argument("--background", help="Background color (hex, e.g. #1A1A2E)")
        parser.add_argument("--text-color", help="Text color (hex, e.g. #E8D5B7)")
        parser.add_argument("--accent-color", help="Accent/border color (hex, e.g. #D4A017)")

    # render-rune
    p_render_rune = subparsers.add_parser("render-rune", help="Render a single rune as SVG/PNG")
    p_render_rune.add_argument("rune", help="Rune name (e.g., 'Fehu') or Unicode character")
    _add_style_args(p_render_rune)
    p_render_rune.add_argument("--no-metadata", action="store_true", help="Hide rune metadata from card")
    p_render_rune.add_argument("--no-border", action="store_true", help="Hide border from card")
    p_render_rune.set_defaults(func=cmd_render_rune)

    # render-bindrune
    p_render_bindrune = subparsers.add_parser("render-bindrune", help="Compose multiple runes into a bindrune SVG")
    p_render_bindrune.add_argument("runes", nargs="+", help="Rune names to compose (e.g., Fehu Uruz)")
    _add_style_args(p_render_bindrune)
    p_render_bindrune.add_argument("--name", help="Optional name for the bindrune")
    p_render_bindrune.set_defaults(func=cmd_render_bindrune)

    # render-spread
    p_render_spread = subparsers.add_parser("render-spread", help="Render a divination spread as SVG/PNG")
    p_render_spread.add_argument("question", nargs="?", default=None,
                                  help="Optional question for the spread")
    _add_style_args(p_render_spread, default_w=900, default_h=650)
    p_render_spread.add_argument("--aett", action="store_true",
                                  help="Draw one rune from each ætt instead")
    p_render_spread.add_argument("--seed", type=int, default=None,
                                  help="Seed for reproducible spread")
    p_render_spread.set_defaults(func=cmd_render_spread)

    # render-circle
    p_render_circle = subparsers.add_parser("render-circle", help="Render the futhark circle as SVG/PNG")
    _add_style_args(p_render_circle, default_w=520, default_h=520)
    p_render_circle.add_argument("--radius", type=int, default=180, help="Circle radius (default: 180)")
    p_render_circle.add_argument("--highlight", nargs="*", help="Rune names to highlight")
    p_render_circle.add_argument("--title", help="Title for the circle")
    p_render_circle.set_defaults(func=cmd_render_circle)

    # render-futhark
    p_render_futhark = subparsers.add_parser("render-futhark", help="Render the full futhark table as SVG/PNG")
    _add_style_args(p_render_futhark)
    p_render_futhark.set_defaults(func=cmd_render_futhark)

    args = parser.parse_args()

    if args.command is None:
        print(render_rune_banner())
        print("\n  Use 'runavel --help' to see available commands.")
        print("  Try: runavel spread \"What guides my path?\"\n")
        return

    args.func(args)


if __name__ == "__main__":
    main()