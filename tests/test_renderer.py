"""Tests for the Terminal renderer."""

import pytest
from runavel.renderer import (
    render_futhark_table,
    render_rune_banner,
    render_rune_card,
    render_rune_circle,
    render_rune_stave,
    render_spread_visual,
    RUNE_STAVES,
)
from runavel.runes import ELDER_FUTHARK, RUNE_BY_NAME, RUNE_BY_UNICODE
from runavel.divination import Divination


class TestRuneStaves:
    """Tests for ASCII art rune staves."""

    def test_all_24_runes_have_staves(self):
        for rune in ELDER_FUTHARK:
            assert rune.unicode in RUNE_STAVES, f"Missing stave for {rune.name}"

    def test_staves_are_list_of_strings(self):
        for char, lines in RUNE_STAVES.items():
            assert isinstance(lines, list)
            for line in lines:
                assert isinstance(line, str)

    def test_render_rune_stave_known_rune(self):
        result = render_rune_stave("ᚠ")
        assert "╱" in result  # Fehu stave contains these chars

    def test_render_rune_stave_unknown_falls_back(self):
        result = render_rune_stave("X")
        assert "X" in result


class TestRuneCard:
    """Tests for the rune card renderer."""

    def test_render_rune_card(self):
        fehu = RUNE_BY_NAME["Fehu"]
        card = render_rune_card(fehu)
        assert "Fehu" in card
        assert "ᚠ" in card
        assert "Fire" in card
        assert "Meaning" in card

    def test_render_rune_card_without_stave(self):
        fehu = RUNE_BY_NAME["Fehu"]
        card = render_rune_card(fehu, show_stave=False)
        assert "Fehu" in card


class TestFutharkTable:
    """Tests for the full futhark table renderer."""

    def test_render_futhark_table(self):
        table = render_futhark_table()
        assert "ELDER FUTHARK" in table
        assert "ᚠ" in table  # At least one rune unicode

    def test_futhark_table_has_all_aettir(self):
        from runavel.runes import Aett
        table = render_futhark_table()
        for aett in Aett:
            assert aett.value in table


class TestRuneCircle:
    """Tests for the rune circle renderer."""

    def test_render_rune_circle(self):
        circle = render_rune_circle()
        assert isinstance(circle, str)
        assert len(circle) > 0

    def test_render_rune_circle_with_title(self):
        circle = render_rune_circle(title="Test Circle")
        assert "Test Circle" in circle

    def test_render_rune_circle_with_highlight(self):
        highlight = [ELDER_FUTHARK[0]]
        circle = render_rune_circle(highlight_runes=highlight)
        assert isinstance(circle, str)


class TestSpreadVisual:
    """Tests for the spread visual renderer."""

    def test_render_spread_visual(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune(question="Test")
        visual = render_spread_visual(spread)
        assert "RÚNAVÉL" in visual
        assert "Test" in visual

    def test_render_spread_visual_synthesis(self):
        div = Divination(seed=1)
        spread = div.draw_three_rune()
        visual = render_spread_visual(spread)
        assert "SYNTHESIS" in visual


class TestRuneBanner:
    """Tests for the rune banner renderer."""

    def test_render_rune_banner(self):
        banner = render_rune_banner()
        # Banner uses spaced letters: "R Ú N A V É L"
        assert "R Ú N A V É L" in banner or "RÚNAVÉL" in banner
        assert "Rune Machine" in banner
        assert "ᚠ" in banner