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

Examples:
    runavel encode "Hello world"
    runavel shift "Secret message" 7
    runavel spread "What guides my path?"
    runavel info Fehu
"""

import argparse
import sys
from datetime import datetime

from .runes import RUNE_BY_NAME, ELDER_FUTHARK, AETTIR, Aett
from .cipher import RunicCipher, CipherMode
from .divination import Divination, SpreadType
from .renderer import (
    render_rune_card,
    render_rune_banner,
    render_futhark_table,
    render_spread_visual,
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

    args = parser.parse_args()

    if args.command is None:
        print(render_rune_banner())
        print("\n  Use 'runavel --help' to see available commands.")
        print("  Try: runavel spread \"What guides my path?\"\n")
        return

    args.func(args)


if __name__ == "__main__":
    main()