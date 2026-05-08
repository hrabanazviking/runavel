"""Tests for the runic cipher engine."""

import pytest
from runavel.cipher import CipherMode, RunicCipher
from runavel.runes import ELDER_FUTHARK, RUNE_BY_UNICODE


class TestSubstitutionCipher:
    """Tests for substitution mode encoding/decoding."""

    def setup_method(self):
        self.cipher = RunicCipher(mode=CipherMode.SUBSTITUTION)

    def test_encode_simple_word(self):
        result = self.cipher.encode("fehu")
        assert len(result) == 4
        assert all(c in RUNE_BY_UNICODE or c in (" ", "·", "᛬") for c in result)

    def test_decode_encoded_text(self):
        encoded = self.cipher.encode("fehu")
        decoded = self.cipher.decode(encoded)
        assert decoded == "fehu"

    def test_encode_preserves_spaces(self):
        encoded = self.cipher.encode("hello world")
        assert " " in encoded

    def test_decode_spaces(self):
        encoded = self.cipher.encode("a b")
        decoded = self.cipher.decode(encoded)
        assert decoded == "a b"

    def test_unknown_characters_as_separator(self):
        result = self.cipher.encode("a!b")
        # Punctuation should become · separator
        assert "·" in result or "᛬" in result

    def test_capital_letter_mapping(self):
        # 'F' should map via phonetic_alt to Fehu
        result = self.cipher.encode("F")
        assert result == "ᚠ"

    def test_digraph_th(self):
        result = self.cipher.encode("th")
        assert len(result) == 1  # "th" maps to a single rune (Thurisaz)
        assert result == "ᚦ"

    def test_digraph_ng(self):
        result = self.cipher.encode("ng")
        assert len(result) == 1  # "ng" maps to Ingwaz
        assert result == "ᛜ"

    def test_roundtrip_various_words(self):
        for word in ["fehu", "raidho", "kenaz", "sowilo"]:
            encoded = self.cipher.encode(word)
            decoded = self.cipher.decode(encoded)
            assert decoded == word, f"Roundtrip failed for '{word}': {decoded}"


class TestShiftCipher:
    """Tests for shift (Caesar-style) cipher mode."""

    def test_shift_encode_shifts_positions(self):
        plain = RunicCipher(mode=CipherMode.SUBSTITUTION)
        shifted = RunicCipher(mode=CipherMode.SHIFT, key=1)
        # With key=1, each rune should be shifted by 1 position
        assert shifted.encode("f") != plain.encode("f")

    def test_shift_roundtrip(self):
        cipher = RunicCipher(mode=CipherMode.SHIFT, key=7)
        encoded = cipher.encode("hello")
        decoded = cipher.decode(encoded)
        assert decoded == "hello"

    def test_shift_roundtrip_zero_key(self):
        cipher = RunicCipher(mode=CipherMode.SHIFT, key=0)
        # Key 0 should be same as substitution for single chars
        sub = RunicCipher(mode=CipherMode.SUBSTITUTION)
        assert cipher.encode("hello") == sub.encode("hello")

    def test_shift_different_keys(self):
        for key in [3, 7, 13, 23]:
            cipher = RunicCipher(mode=CipherMode.SHIFT, key=key)
            encoded = cipher.encode("test")
            decoded = cipher.decode(encoded)
            assert decoded == "test", f"Roundtrip failed with key={key}"

    def test_key_normalization(self):
        # Keys are normalized mod 24
        cipher1 = RunicCipher(mode=CipherMode.SHIFT, key=5)
        cipher2 = RunicCipher(mode=CipherMode.SHIFT, key=29)
        assert cipher1.key == cipher2.key  # 29 % 24 == 5


class TestWyrdCipher:
    """Tests for wyrd numerological cipher mode."""

    def setup_method(self):
        self.cipher = RunicCipher(mode=CipherMode.WYRD)

    def test_wyrd_produces_runes(self):
        result = RunicCipher(mode=CipherMode.WYRD).encode("hello")
        # All non-space chars should be rune unicode chars
        for ch in result:
            if ch != " ":
                assert ch in RUNE_BY_UNICODE or ch == "᛬"

    def test_wyrd_preserves_spaces(self):
        result = RunicCipher(mode=CipherMode.WYRD).encode("hello world")
        assert " " in result

    def test_wyrd_is_lossy(self):
        # Wyrd encoding is intentionally lossy
        encoded = RunicCipher(mode=CipherMode.WYRD).encode("hello")
        decoded = RunicCipher(mode=CipherMode.WYRD).decode(encoded)
        # Decoded text may not round-trip perfectly
        assert isinstance(decoded, str)


class TestCipherAnalyze:
    """Tests for the analyze method."""

    def test_analyze_runic_text(self):
        cipher = RunicCipher(mode=CipherMode.SUBSTITUTION)
        encoded = cipher.encode("fehu")
        analysis = cipher.analyze(encoded)
        assert len(analysis) == 4
        assert all(item["type"] in ("rune", "space", "punctuation", "unknown")
                    for item in analysis)

    def test_analyze_with_spaces(self):
        cipher = RunicCipher(mode=CipherMode.SUBSTITUTION)
        encoded = cipher.encode("a b")
        analysis = cipher.analyze(encoded)
        space_items = [i for i in analysis if i["type"] == "space"]
        assert len(space_items) >= 1