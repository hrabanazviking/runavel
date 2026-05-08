"""
Runic Cipher Engine
~~~~~~~~~~~~~~~~~~~~~
Encodes and decodes text using the Elder Futhark.

Three cipher modes:
  1. SUBSTITUTION — Direct phoneme-to-rune mapping
  2. SHIFT (Caesar-style) — Shifts phonetic positions by a key number
  3. WYRD — Encodes using runic numerological associations

The cipher treats the futhark as a living system —
not merely a substitution table, but a web of correspondences
where meaning shifts with context, just as the Norns weave.

"Speak in runes, not static."
  — Volmarr, "Runes Over Prompt-Magic"
"""

from enum import Enum
from typing import Optional

from .runes import (
    ELDER_FUTHARK,
    RUNE_BY_NAME,
    RUNE_BY_PHONETIC,
    RUNE_BY_PHONETIC_ALT,
    RUNE_BY_WYRD,
    Rune,
)


class CipherMode(Enum):
    """Available runic cipher modes."""
    SUBSTITUTION = "substitution"
    SHIFT = "shift"
    WYRD = "wyrd"


class RunicCipher:
    """
    A living cipher engine for the Elder Futhark.

    The runes are not a code — they are a language of forces.
    This engine translates between text and runes, preserving
    as much semantic information as the chosen mode allows.
    """

    # Extended phoneme mapping for English text → runic phonemes
    # This is simplified — Old Norse had cleaner phoneme-to-rune mapping
    PHONEME_MAP: dict[str, str] = {
        # Direct phonetic matches
        "f": "f", "F": "F",
        "u": "u", "U": "U",
        "th": "th", "TH": "Þ", "Th": "Þ",
        "a": "a", "A": "A",
        "r": "r", "R": "R",
        "k": "k", "K": "K", "c": "k", "C": "K",
        "g": "g", "G": "G",
        "v": "w", "V": "W", "w": "w", "W": "W",
        "h": "h", "H": "H",
        "n": "n", "N": "N",
        "i": "i", "I": "I",
        "j": "j", "J": "J", "y": "j", "Y": "J",
        "p": "p", "P": "P",
        "z": "z", "Z": "Z",
        "s": "s", "S": "S",
        "t": "t", "T": "T",
        "b": "b", "B": "B",
        "e": "e", "E": "E",
        "m": "m", "M": "M",
        "l": "l", "L": "L",
        "d": "d", "D": "D",
        "o": "o", "O": "O",
        "ng": "ng", "NG": "Ŋ",
    }

    def __init__(self, mode: CipherMode = CipherMode.SUBSTITUTION, key: int = 0):
        """
        Initialize the cipher.

        Args:
            mode: The cipher mode to use
            key: The shift key (only used in SHIFT mode)
        """
        self.mode = mode
        self.key = key % 24  # Normalize key to futhark range

    def encode(self, text: str) -> str:
        """
        Encode a text string into runes.

        In SUBSTITUTION mode: direct phoneme-to-rune mapping.
        In SHIFT mode: applies a Caesar-style shift on the futhark positions.
        In WYRD mode: maps each character to its wyrd-numerological rune.
        """
        if self.mode == CipherMode.SUBSTITUTION:
            return self._encode_substitution(text)
        elif self.mode == CipherMode.SHIFT:
            return self._encode_shift(text)
        elif self.mode == CipherMode.WYRD:
            return self._encode_wyrd(text)
        else:
            raise ValueError(f"Unknown cipher mode: {self.mode}")

    def decode(self, runic_text: str) -> str:
        """
        Decode a runic string back to Latin text.

        Note: SUBSTITUTION mode decodes cleanly. SHIFT mode requires
        the same key. WYRD mode is lossy — phonetic reconstruction
        is approximate.
        """
        if self.mode == CipherMode.SUBSTITUTION:
            return self._decode_substitution(runic_text)
        elif self.mode == CipherMode.SHIFT:
            return self._decode_shift(runic_text)
        elif self.mode == CipherMode.WYRD:
            return self._decode_wyrd(runic_text)
        else:
            raise ValueError(f"Unknown cipher mode: {self.mode}")

    # ── SUBSTITUTION ───────────────────────────────────────────────

    def _encode_substitution(self, text: str) -> str:
        """Direct phoneme-to-rune substitution."""
        result = []
        i = 0
        while i < len(text):
            char = text[i]

            # Handle spaces and punctuation — pass through as dividers
            if not char.isalpha():
                result.append(" " if char == " " else "·")
                i += 1
                continue

            # Try multi-character phonemes first (th, ng)
            if i + 1 < len(text):
                digraph = text[i:i+2]
                if digraph.lower() in ("th", "ng"):
                    phoneme = self.PHONEME_MAP.get(digraph.lower(), digraph.lower())
                    phoneme_alt = self.PHONEME_MAP.get(digraph, phoneme)
                    rune = self._phoneme_to_rune(phoneme_alt if digraph[0].isupper() else phoneme)
                    if rune:
                        result.append(rune.unicode)
                    else:
                        result.append("᛬")  # Unknown rune marker
                    i += 2
                    continue

            # Single character phoneme
            is_upper = char.isupper()
            phoneme = char.lower()
            rune = self._phoneme_to_rune(phoneme, capitalize=is_upper)

            if rune:
                result.append(rune.unicode)
            elif phoneme in self.PHONEME_MAP:
                mapped = self.PHONEME_MAP[phoneme]
                rune = self._phoneme_to_rune(mapped)
                if rune:
                    result.append(rune.unicode)
                else:
                    result.append("᛬")
            else:
                result.append("᛬")

            i += 1

        return "".join(result)

    def _decode_substitution(self, runic_text: str) -> str:
        """Decode runes back to Latin characters (phonetic values)."""
        from .runes import RUNE_BY_UNICODE
        result = []
        for char in runic_text:
            if char == " ":
                result.append(" ")
            elif char == "·":
                result.append(" ")
            elif char == "᛬":
                result.append("?")
            elif char in RUNE_BY_UNICODE:
                rune = RUNE_BY_UNICODE[char]
                result.append(rune.phonetic)
            else:
                result.append("?")
        return "".join(result)

    def _phoneme_to_rune(self, phoneme: str, capitalize: bool = False) -> Optional[Rune]:
        """Map a phoneme to its corresponding rune.

        Checks both primary and alternate phoneme dictionaries,
        so uppercase and special phoneme values (like Þ, Ŋ) resolve correctly.
        """
        # Try the preferred dict first, then fall back
        primary = RUNE_BY_PHONETIC_ALT if capitalize else RUNE_BY_PHONETIC
        secondary = RUNE_BY_PHONETIC if capitalize else RUNE_BY_PHONETIC_ALT

        result = primary.get(phoneme)
        if result is None:
            result = secondary.get(phoneme)
        return result

    # ── SHIFT (Caesar-style) ───────────────────────────────────────

    def _encode_shift(self, text: str) -> str:
        """
        Caesar-style shift cipher on the futhark.

        Each phoneme is mapped to its futhark position, shifted by key,
        then mapped back to the rune at the new position.
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]

            if not char.isalpha():
                result.append(" " if char == " " else "·")
                i += 1
                continue

            # Get the base rune for this character
            base_rune = self._char_to_base_rune(char)
            if base_rune:
                # Shift position
                shifted_pos = ((base_rune.global_position - 1) + self.key) % 24 + 1
                shifted_rune = ELDER_FUTHARK[shifted_pos - 1]
                result.append(shifted_rune.unicode)
            else:
                # Try multi-char phoneme
                if i + 1 < len(text):
                    digraph = text[i:i+2].lower()
                    if digraph in ("th", "ng"):
                        base_rune = self._phoneme_to_rune(
                            "Þ" if digraph == "th" else "Ŋ"
                        )
                        if base_rune:
                            shifted_pos = ((base_rune.global_position - 1) + self.key) % 24 + 1
                            shifted_rune = ELDER_FUTHARK[shifted_pos - 1]
                            result.append(shifted_rune.unicode)
                            i += 2
                            continue
                result.append("᛬")

            i += 1

        return "".join(result)

    def _decode_shift(self, runic_text: str) -> str:
        """Reverse the shift cipher."""
        from .runes import RUNE_BY_UNICODE
        result = []
        for char in runic_text:
            if char == " ":
                result.append(" ")
            elif char == "·":
                result.append(" ")
            elif char == "᛬":
                result.append("?")
            elif char in RUNE_BY_UNICODE:
                rune = RUNE_BY_UNICODE[char]
                # Reverse shift
                original_pos = ((rune.global_position - 1) - self.key) % 24 + 1
                original_rune = ELDER_FUTHARK[original_pos - 1]
                result.append(original_rune.phonetic)
            else:
                result.append("?")
        return "".join(result)

    def _char_to_base_rune(self, char: str) -> Optional[Rune]:
        """Map a single character to its base rune."""
        # Try direct phonetic match first
        phoneme = char.lower()
        rune = RUNE_BY_PHONETIC.get(phoneme)
        if rune:
            return rune

        # Try PHONEME_MAP for alternate mappings
        mapped = self.PHONEME_MAP.get(char) or self.PHONEME_MAP.get(phoneme)
        if mapped:
            return RUNE_BY_PHONETIC.get(mapped) or RUNE_BY_PHONETIC_ALT.get(mapped)

        return None

    # ── WYRD NUMEROLOGY ────────────────────────────────────────────

    def _encode_wyrd(self, text: str) -> str:
        """
        Wyrd cipher: encodes text using runic numerology.

        Each character's ordinal value is mapped to a position in the
        futhark through wyrd-associative mathematics. Letters that
        share numerological resonance are grouped together, reflecting
        how the Norns bind related threads of fate.

        The encoding is: for each char, take its ordinal, reduce it
        through the futhark cycle (mod 24), and use the wyrd-value
        as a secondary verification layer.
        """
        result = []
        for char in text:
            if not char.isalpha():
                result.append(" " if char == " " else "·")
                continue

            # Map character ordinal to futhark position via modular reduction
            ordinal = ord(char.upper())
            # Use a more complex mapping that preserves some phonetic resonance
            # while introducing wyrd-associative depth
            futhark_index = ((ordinal * 7) + 3) % 24  # 7 and 3 are sacred numbers
            rune = ELDER_FUTHARK[futhark_index]
            result.append(rune.unicode)

        return "".join(result)

    def _decode_wyrd(self, runic_text: str) -> str:
        """
        Decode wyrd-encoded text.

        This is lossy — multiple Latin characters may map to the same
        rune through wyrd-associative encoding. The best we can do is
        reconstruct the most likely phonetic value of each rune.
        """
        from .runes import RUNE_BY_UNICODE
        result = []
        for char in runic_text:
            if char == " ":
                result.append(" ")
            elif char == "·":
                result.append(" ")
            elif char in RUNE_BY_UNICODE:
                rune = RUNE_BY_UNICODE[char]
                result.append(rune.phonetic)
            else:
                result.append("?")
        return "".join(result)

    # ── UTILITY ────────────────────────────────────────────────────

    def analyze(self, runic_text: str) -> list[dict]:
        """
        Analyze a runic text and return metadata for each rune.

        Returns a list of dictionaries with rune data, for divination
        and insight. Not all characters need be runes — non-rune
        characters are annotated as separators.
        """
        from .runes import RUNE_BY_UNICODE
        analysis = []

        for char in runic_text:
            if char in RUNE_BY_UNICODE:
                rune = RUNE_BY_UNICODE[char]
                analysis.append({
                    "char": char,
                    "rune": rune,
                    "type": "rune",
                })
            elif char == " ":
                analysis.append({"char": char, "type": "space"})
            elif char == "·":
                analysis.append({"char": char, "type": "punctuation"})
            else:
                analysis.append({"char": char, "type": "unknown"})

        return analysis