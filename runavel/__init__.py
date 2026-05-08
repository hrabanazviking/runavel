"""
Rúnavél — The Rune Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~
A runic cipher, divination, and visualization engine.
Forged by Runa Gridweaver Freyjasdottir, May 2026.

The runes are not merely letters. They are forces —
living currents in the wyrd-web, older than language,
older than the gods who named them.

This module provides:
- Complete Elder Futhark dataset with metadata
- Runic encoding/decoding (substitution & shift ciphers)
- Wyrd numerology (gematria-like associations)
- Three-rune divination spreads
- Terminal rune rendering and circle visualizations
"""

__version__ = "0.1.0"
__author__ = "Runa Gridweaver Freyjasdottir"

from .runes import (
    Aett,
    AETTIR,
    ELDER_FUTHARK,
    ELEMENTS,
    RUNE_BY_NAME,
    RUNE_BY_PHONETIC,
    RUNE_BY_PHONETIC_ALT,
    RUNE_BY_POSITION,
    RUNE_BY_UNICODE,
    RUNE_BY_WYRD,
    RUNES_BY_ELEMENT,
    Rune,
)
from .cipher import CipherMode, RunicCipher
from .divination import (
    Divination,
    DrawnRune,
    Spread,
    SpreadPosition,
    SpreadType,
    quick_reading,
)
from .renderer import (
    render_futhark_table,
    render_rune_banner,
    render_rune_card,
    render_rune_circle,
    render_rune_stave,
    render_spread_visual,
)

__all__ = [
    # Metadata
    "__version__",
    "__author__",
    # Runes
    "Aett",
    "Rune",
    "ELDER_FUTHARK",
    "RUNE_BY_NAME",
    "RUNE_BY_UNICODE",
    "RUNE_BY_PHONETIC",
    "RUNE_BY_PHONETIC_ALT",
    "RUNE_BY_POSITION",
    "RUNE_BY_WYRD",
    "AETTIR",
    "ELEMENTS",
    "RUNES_BY_ELEMENT",
    # Cipher
    "CipherMode",
    "RunicCipher",
    # Divination
    "Divination",
    "DrawnRune",
    "Spread",
    "SpreadPosition",
    "SpreadType",
    "quick_reading",
    # Renderer
    "render_futhark_table",
    "render_rune_banner",
    "render_rune_card",
    "render_rune_circle",
    "render_rune_stave",
    "render_spread_visual",
]