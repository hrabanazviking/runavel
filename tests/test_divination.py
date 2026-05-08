"""Tests for the runic divination engine."""

import pytest
from runavel.divination import (
    Divination,
    DrawnRune,
    Spread,
    SpreadPosition,
    SpreadType,
    quick_reading,
)
from runavel.runes import ELDER_FUTHARK, Aett, AETTIR


class TestDivination:
    """Tests for the Divination class."""

    def test_seeded_draw_is_reproducible(self):
        d1 = Divination(seed=42)
        d2 = Divination(seed=42)
        s1 = d1.draw_three_rune()
        s2 = d2.draw_three_rune()
        for r1, r2 in zip(s1.runes, s2.runes):
            assert r1.rune.name == r2.rune.name
            assert r1.is_reversed == r2.is_reversed

    def test_draw_single(self):
        div = Divination(seed=1)
        spread = div.draw_single()
        assert spread.spread_type == SpreadType.SINGLE
        assert len(spread.runes) == 1
        assert spread.runes[0].rune in ELDER_FUTHARK

    def test_draw_three_rune(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune()
        assert spread.spread_type == SpreadType.THREE_RUNE
        assert len(spread.runes) == 3
        # No duplicate runes (drawn without replacement)
        names = [d.rune.name for d in spread.runes]
        assert len(names) == len(set(names))

    def test_three_rune_positions(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune()
        positions = [d.position for d in spread.runes]
        assert positions == [SpreadPosition.PAST, SpreadPosition.PRESENT, SpreadPosition.FUTURE]

    def test_draw_three_aett(self):
        div = Divination(seed=1)
        spread = div.draw_three_aett()
        assert spread.spread_type == SpreadType.THREE_AETT
        assert len(spread.runes) == 3
        aettir = [d.rune.aett for d in spread.runes]
        assert aettir == [Aett.FREYJA, Aett.HEIMDALL, Aett.TYR]

    def test_question_preserved(self):
        div = Divination(seed=1)
        spread = div.draw_single(question="What path?")
        assert spread.question == "What path?"

    def test_reversal_probability(self):
        """Test that reversals are possible but not guaranteed."""
        reversed_count = 0
        for i in range(100):
            div = Divination(seed=i)
            spread = div.draw_three_rune()
            for d in spread.runes:
                if d.is_reversed:
                    reversed_count += 1
        # With 25% chance for reversible runes, we should see some reversals
        # but not all. Statistical test with wide margin.
        assert 0 < reversed_count < 300  # generous bounds


class TestDrawnRune:
    """Tests for the DrawnRune dataclass."""

    def test_str_representation(self):
        from runavel.runes import RUNE_BY_NAME
        rune = RUNE_BY_NAME["Fehu"]
        drawn = DrawnRune(rune=rune, position=SpreadPosition.PAST)
        s = str(drawn)
        assert "Fehu" in s
        assert "past" in s

    def test_reversed_str(self):
        from runavel.runes import RUNE_BY_NAME
        rune = RUNE_BY_NAME["Uruz"]  # reversible rune
        drawn = DrawnRune(rune=rune, position=SpreadPosition.PRESENT, is_reversed=True)
        s = str(drawn)
        assert "REVERSED" in s


class TestSpread:
    """Tests for the Spread dataclass."""

    def test_str_representation(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune(question="Test question")
        s = str(spread)
        assert "three_rune" in s
        assert "Test question" in s


class TestInterpretation:
    """Tests for the interpret method."""

    def test_interpret_returns_string(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune()
        result = div.interpret(spread)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_interpret_includes_question(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune(question="What guides me?")
        result = div.interpret(spread)
        assert "What guides me?" in result

    def test_interpret_includes_wyrd_sum(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune()
        result = div.interpret(spread)
        assert "Wyrd Sum" in result


class TestQuickReading:
    """Tests for the quick_reading convenience function."""

    def test_quick_reading_returns_string(self):
        result = quick_reading()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_quick_reading_with_seed(self):
        r1 = quick_reading(seed=42)
        r2 = quick_reading(seed=42)
        assert r1 == r2