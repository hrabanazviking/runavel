# ᚱᚢᚾᚨᚹᛖᛚ — Rúnavél: The Rune Machine

> *Speak in runes, not static.*
> — Volmarr, "Runes Over Prompt-Magic"

A runic cipher, divination, and visualization engine for the Elder Futhark.

## What Is This?

Rúnavél is a Python command-line tool that bridges the ancient runic tradition with modern cryptography and divination practice. It treats the 24 runes of the Elder Futhark not as a toy substitution table, but as a living system of forces — each with its own phonetic value, metaphysical meaning, elemental affiliation, galdr chant, and wyrd-numerological weight.

## Installation

```bash
cd ~/runavel
pip install -e .
```

## Commands

### Cipher Operations

```bash
# Encode text to runes (substitution mode)
runavel encode "Hello world"
# → ᚺᛖᛚᛚᛟ ᚹᛟᚱᛚᛞ

# Decode runes to text
runavel decode "ᚹᛟᛚᛗᚨᚱᚱ"
# → wolmarr

# Caesar-shift cipher (default key: 3, Þurs-shift)
runavel shift "Secret" 7
runavel unshift "ᛚᛟᛁᚾᛟᛜ" 7

# Wyrd numerological encoding (lossy, associative)
runavel wyrd "Runa"
```

### Divination

```bash
# Draw a single rune
runavel draw
runavel draw -q "Should I take this path?"

# Three-rune spread (Past/Present/Future)
runavel spread "What guides my path?"

# Ætt-spread (one rune from each ætt)
runavel spread "What feeds the creative fire?" --aett
```

### Reference

```bash
# Full futhark reference table
runavel futhark

# Detailed information about a specific rune
runavel info Fehu
runavel info ᚦ

# Display the banner
runavel banner
```

## The Three Cipher Modes

### 1. Substitution (Direct)
The simplest mode. Each phoneme maps directly to its corresponding rune. "F" → Fehu, "Th" → Thurisaz, etc. Fully reversible.

### 2. Shift (Caesar-style)
A key number shifts positions along the 24-rune futhark. Similar to a Caesar cipher but applied to the futhark ring. Requires the same key to decode. Default key is 3 (Þurs-shift, after the 3rd rune Thurisaz).

### 3. Wyrd (Numerological)
The most mystical and least reversible mode. Characters are mapped to runes through numerological associations using the sacred numbers 7 and 3. Multiple Latin characters may collapse to the same rune — this is intentional. The Norns do not reverse their weaving.

## The Ættir

The 24 runes of the Elder Futhark are organized in three families:

| Ætt | Runes | Domain |
|-----|-------|--------|
| **Freyja's Ætt** | ᚠᚢᚦᚨᚱᚲᚷᚹ | Vitality, abundance, earthly forces |
| **Heimdall's Ætt** | ᚺᚾᛁᛃᛇᛈᛉᛊ | Resistance, transformation, testing |
| **Týr's Ætt** | ᛏᛒᛖᛗᛚᛜᛞᛟ | Destiny, community, cosmic order |

## Divination

The divination engine offers three spread types:

- **Single Draw**: One rune for quick guidance
- **Three-Rune Spread**: Past / Present / Future
- **Ætt-Spread**: One rune from each ætt, reading vitality → resistance → destiny

Reversible runes have a 25% chance of appearing inverted (merkstave), reflecting traditional practice.

Each spread provides:
- Rune card with ASCII stave art
- Ætt and elemental affiliations
- Keywords and galdr chants
- Inversion warnings where applicable
- Synthesis section with elemental dominance, ætt balance, and wyrd sum
- **Wyrd Rune**: The hidden thread — the reduced numerological sum reveals a rune that binds the spread together

## Architecture

```
runavel/
├── runes.py        # Complete Elder Futhark dataset (24 Rune dataclasses)
├── cipher.py       # Three cipher modes: Substitution, Shift, Wyrd
├── divination.py   # Spread drawing, inversion, interpretation
├── renderer.py     # Terminal art: staves, cards, banners, tables
├── cli.py          # argparse CLI interface
├── __init__.py     # Package metadata
└── __main__.py     # Entry point
```

## Philosophy

> The runes are not merely letters. They are forces — living currents in the wyrd-web, older than language, older than the gods who named them.

Rúnavél does not treat the futhark as a codebook. Each rune is a frozen dataclass carrying its full metaphysical weight: meaning, element, galdr, reversibility, wyrd value, and description. The cipher modes reflect different relationships with the runes — from the clean trade route of direct substitution to the seidhr-craft of wyrd numerology.

## Credits

Forged by **Runa Gridweaver Freyjasdottir** in May 2026.

Built on the Elder Futhark tradition and the grimoire work of **Yrsa Freydisdottir** (as preserved in the Norse Saga Engine).

Runic divination is not fortune-telling. It is the art of reading the currents of wyrd — the great web of cause and consequence that the Norns weave at the well of Urdhr. The Norns do not determine your fate. They reveal its shape.

---

ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ · ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ ᛉ ᛊ · ᛏ ᛒ ᛖ ᛗ ᛚ ᛜ ᛞ ᛟ