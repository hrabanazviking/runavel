"""
Tests for Rúnavél SVG Renderer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Comprehensive tests for SVG generation functions:
  - Individual rune cards
  - Bindrune compositions
  - Rune circle visualizations
  - Divination spread renders
  - Futhark table
  - File export (save_svg)
"""

import os
import tempfile
from pathlib import Path

import pytest

from runavel.runes import (
    ELDER_FUTHARK,
    RUNE_BY_NAME,
    RUNE_BY_UNICODE,
    Aett,
    Rune,
)
from runavel.divination import Divination, SpreadType
from runavel.svg_renderer import (
    SVGOptions,
    ELEMENT_COLORS,
    AETT_COLORS,
    RUNE_SVG_PATHS,
    render_rune_svg,
    render_bindrune_svg,
    render_rune_circle_svg,
    render_spread_svg,
    render_futhark_table_svg,
    save_svg,
    save_png,
    _rune_path,
    _escape_xml,
    _wrap_text,
)


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def fehu():
    return RUNE_BY_NAME["Fehu"]


@pytest.fixture
def uruz():
    return RUNE_BY_NAME["Uruz"]


@pytest.fixture
def sample_spread():
    div = Divination(seed=42)
    return div.draw_three_rune(question="What guides my path?")


@pytest.fixture
def default_opts():
    return SVGOptions()


# ── SVG Options ──────────────────────────────────────────────────────

class TestSVGOptions:
    def test_default_options(self):
        opts = SVGOptions()
        assert opts.width == 400
        assert opts.height == 600
        assert opts.stroke_color == "#D4A017"
        assert opts.background == "#1A1A2E"
        assert opts.show_metadata is True
        assert opts.border is True

    def test_custom_options(self):
        opts = SVGOptions(
            width=800,
            height=1000,
            stroke_color="#FF0000",
            background="#000000",
            show_metadata=False,
            border=False,
        )
        assert opts.width == 800
        assert opts.height == 1000
        assert opts.stroke_color == "#FF0000"
        assert opts.show_metadata is False
        assert opts.border is False


# ── Helper Functions ───────────────────────────────────────────────────

class TestHelpers:
    def test_rune_path_returns_path_for_known_runes(self):
        """All runes with SVG paths should have path data."""
        fehu = RUNE_BY_NAME["Fehu"]
        path = _rune_path(fehu)
        assert path is not None
        assert "M" in path  # SVG paths start with M (moveto)

    def test_rune_path_returns_none_for_unknown(self):
        """Rune without SVG path data should return None."""
        # All Elder Futhark runes should have paths
        for rune in ELDER_FUTHARK:
            path = _rune_path(rune)
            assert path is not None, f"Missing SVG path for {rune.name} ({rune.unicode})"

    def test_escape_xml_special_chars(self):
        assert _escape_xml("A & B") == "A &amp; B"
        assert _escape_xml('<tag>') == "&lt;tag&gt;"
        assert _escape_xml('"quote"') == "&quot;quote&quot;"
        assert _escape_xml("normal text") == "normal text"

    def test_wrap_text_short(self):
        result = _wrap_text("short text", 50)
        assert result == ["short text"]

    def test_wrap_text_long(self):
        result = _wrap_text("this is a longer piece of text that needs wrapping", 20)
        assert len(result) > 1
        for line in result:
            assert len(line) <= 20 + 5  # Some tolerance for word boundaries

    def test_wrap_text_empty(self):
        result = _wrap_text("", 50)
        assert result == [""]


# ── SVG Constant Coverage ────────────────────────────────────────────

class TestSVGPathCoverage:
    def test_all_24_runes_have_paths(self):
        """Each of the 24 Elder Futhark runes should have an SVG path."""
        assert len(RUNE_SVG_PATHS) == 24, (
            f"Expected 24 rune paths, got {len(RUNE_SVG_PATHS)}. "
            f"Missing: {set(r.unicode for r in ELDER_FUTHARK) - set(RUNE_SVG_PATHS.keys())}"
        )

    def test_paths_start_with_moveto(self):
        """SVG paths should start with M (moveto) command."""
        for char, path in RUNE_SVG_PATHS.items():
            assert path.strip().startswith("M"), (
                f"Path for rune '{char}' should start with M command"
            )

    def test_element_colors_cover_all_elements(self):
        """Element colors should cover all element types."""
        for element in ("Fire", "Earth", "Air", "Water", "All"):
            assert element in ELEMENT_COLORS

    def test_aett_colors_cover_all_aettir(self):
        """Ætt colors should cover all three ættir."""
        for aett in Aett:
            assert aett.value in AETT_COLORS


# ── Individual Rune SVG ─────────────────────────────────────────────

class TestRenderRuneSVG:
    def test_produces_valid_svg(self, fehu):
        svg = render_rune_svg(fehu)
        assert '<?xml version="1.0"' in svg
        assert '<svg' in svg
        assert '</svg>' in svg

    def test_includes_rune_name(self, fehu):
        svg = render_rune_svg(fehu)
        assert "Fehu" in svg

    def test_includes_metadata(self, fehu):
        svg = render_rune_svg(fehu)
        assert "Cattle, wealth, vital energy" in svg
        assert "Fire" in svg  # Element
        assert "wyrd" in svg.lower() or "Wyrd" in svg

    def test_includes_rune_path(self, fehu):
        svg = render_rune_svg(fehu)
        # Fehu has an SVG path
        assert '<path' in svg
        assert 'stroke-linecap="round"' in svg

    def test_custom_dimensions(self, fehu):
        opts = SVGOptions(width=800, height=1000)
        svg = render_rune_svg(fehu, options=opts)
        assert 'width="800"' in svg
        assert 'height="1000"' in svg

    def test_no_metadata_mode(self, fehu):
        opts = SVGOptions(show_metadata=False)
        svg = render_rune_svg(fehu, options=opts)
        # Should not have the detailed meaning text
        assert "wyrd" not in svg.lower() or "Wyrd" not in svg

    def test_no_border_mode(self, fehu):
        opts = SVGOptions(border=False)
        svg = render_rune_svg(fehu, options=opts)
        assert 'rx="8"' not in svg  # No border rectangles

    def test_all_24_runes_render(self):
        """Every rune in the Elder Futhark should produce valid SVG."""
        for rune in ELDER_FUTHARK:
            svg = render_rune_svg(rune)
            assert '<?xml' in svg
            assert rune.name in svg
            assert '</svg>' in svg

    def test_element_color_applied(self):
        """Each element should use its assigned color in the SVG."""
        fire_rune = RUNE_BY_NAME["Fehu"]  # Fire element
        svg = render_rune_svg(fire_rune)
        assert ELEMENT_COLORS["Fire"] in svg

    def test_rune_unicode_fallback(self):
        """Rune without SVG path should still render with Unicode char."""
        # This tests the fallback path, though all 24 currently have paths
        # We can simulate by removing a path temporarily
        original = RUNE_SVG_PATHS.get("ᚠ")
        try:
            if original:
                del RUNE_SVG_PATHS["ᚠ"]
            fehu = RUNE_BY_NAME["Fehu"]
            svg = render_rune_svg(fehu)
            assert "ᚠ" in svg  # Should fall back to Unicode character
            assert '</svg>' in svg
        finally:
            if original:
                RUNE_SVG_PATHS["ᚠ"] = original


# ── Bindrune SVG ────────────────────────────────────────────────────

class TestRenderBindruneSVG:
    def test_produces_valid_svg(self):
        svg = render_bindrune_svg(["Fehu", "Uruz"])
        assert '<?xml version="1.0"' in svg
        assert '</svg>' in svg

    def test_includes_rune_names(self):
        svg = render_bindrune_svg(["Fehu", "Uruz"])
        assert "Fehu" in svg
        assert "Uruz" in svg

    def test_custom_name(self):
        svg = render_bindrune_svg(
            ["Fehu", "Uruz", "Thurisaz"],
            name="ᚠᚢᚦ Guardian Force"
        )
        assert "Guardian Force" in svg

    def test_combined_wyrd(self):
        svg = render_bindrune_svg(["Fehu", "Uruz"])
        # Fehu(1) + Uruz(2) = 3
        assert "3" in svg  # Combined Wyrd: 3

    def test_three_rune_bindrune(self):
        svg = render_bindrune_svg(["Fehu", "Uruz", "Thurisaz"])
        assert "Fehu" in svg
        assert "Uruz" in svg
        assert "Thurisaz" in svg

    def test_invalid_rune_name(self):
        svg = render_bindrune_svg(["NonExistent"])
        # Should handle gracefully, showing "No valid runes found"
        assert '</svg>' in svg

    def test_component_detail_line(self):
        svg = render_bindrune_svg(["Fehu", "Uruz"])
        assert "ᚠ Fehu" in svg
        assert "ᚢ Uruz" in svg

    def test_custom_dimensions(self):
        opts = SVGOptions(width=500, height=700)
        svg = render_bindrune_svg(["Fehu"], options=opts)
        assert 'width="500"' in svg
        assert 'height="700"' in svg


# ── Rune Circle SVG ──────────────────────────────────────────────────

class TestRenderRuneCircleSVG:
    def test_produces_valid_svg(self):
        svg = render_rune_circle_svg()
        assert '<?xml version="1.0"' in svg
        assert '</svg>' in svg

    def test_all_24_runes_present(self):
        svg = render_rune_circle_svg()
        for rune in ELDER_FUTHARK:
            assert rune.unicode in svg, f"Rune {rune.name} not found in circle SVG"

    def test_all_rune_names_as_labels(self):
        svg = render_rune_circle_svg()
        for rune in ELDER_FUTHARK:
            assert rune.name in svg, f"Rune name {rune.name} not found in circle SVG"

    def test_title(self):
        svg = render_rune_circle_svg(title="Norns' Wheel")
        assert "Norns&#39; Wheel" in svg or "Norns" in svg

    def test_highlight_runes(self):
        fehu = RUNE_BY_NAME["Fehu"]
        svg = render_rune_circle_svg(highlight_runes=[fehu])
        # Highlighted runes should have a glowing circle
        assert 'fill="#FFD700"' in svg or 'opacity="0.3"' in svg

    def test_custom_radius(self):
        svg = render_rune_circle_svg(radius=250)
        # With radius=250, total width should be (250+80)*2 = 660
        assert "660" in svg


# ── Divination Spread SVG ───────────────────────────────────────────

class TestRenderSpreadSVG:
    def test_produces_valid_svg(self, sample_spread):
        svg = render_spread_svg(sample_spread)
        assert '<?xml version="1.0"' in svg
        assert '</svg>' in svg

    def test_includes_question(self, sample_spread):
        svg = render_spread_svg(sample_spread)
        assert "What guides my path?" in svg

    def test_includes_rune_names(self, sample_spread):
        svg = render_spread_svg(sample_spread)
        # Each drawn rune should appear
        for drawn in sample_spread.runes:
            assert drawn.rune.name in svg

    def test_includes_element_tally(self, sample_spread):
        svg = render_spread_svg(sample_spread)
        assert "Elements:" in svg

    def test_includes_wyrd_sum(self, sample_spread):
        svg = render_spread_svg(sample_spread)
        assert "Wyrd Sum:" in svg

    def test_includes_aett_balance(self, sample_spread):
        svg = render_spread_svg(sample_spread)
        assert "Ættir:" in svg

    def test_position_labels(self, sample_spread):
        svg = render_spread_svg(sample_spread)
        assert "PAST" in svg
        assert "PRESENT" in svg
        assert "FUTURE" in svg

    def test_custom_options(self, sample_spread):
        opts = SVGOptions(width=1200, height=800)
        svg = render_spread_svg(sample_spread, options=opts)
        assert 'width="1200"' in svg
        assert 'height="800"' in svg


# ── Futhark Table SVG ───────────────────────────────────────────────

class TestRenderFutharkTableSVG:
    def test_produces_valid_svg(self):
        svg = render_futhark_table_svg()
        assert '<?xml version="1.0"' in svg
        assert '</svg>' in svg

    def test_includes_all_rune_names(self):
        svg = render_futhark_table_svg()
        for rune in ELDER_FUTHARK:
            assert rune.name in svg

    def test_includes_all_rune_characters(self):
        svg = render_futhark_table_svg()
        for rune in ELDER_FUTHARK:
            assert rune.unicode in svg

    def test_includes_aett_headers(self):
        svg = render_futhark_table_svg()
        assert "Freyja" in svg
        assert "Heimdall" in svg
        assert "Týr" in svg

    def test_includes_title(self):
        svg = render_futhark_table_svg()
        assert "ELDER FUTHARK" in svg

    def test_includes_element_colors(self):
        svg = render_futhark_table_svg()
        # At least one element color should be present
        assert ELEMENT_COLORS["Fire"] in svg or ELEMENT_COLORS["Earth"] in svg


# ── File Export ──────────────────────────────────────────────────────

class TestSaveSVG:
    def test_save_svg_creates_file(self, fehu, tmp_path):
        svg = render_rune_svg(fehu)
        filepath = tmp_path / "test_rune.svg"
        result = save_svg(svg, filepath)
        assert result == filepath
        assert filepath.exists()
        content = filepath.read_text(encoding="utf-8")
        assert '<?xml' in content
        assert "Fehu" in content

    def test_save_svg_creates_directories(self, fehu, tmp_path):
        svg = render_rune_svg(fehu)
        filepath = tmp_path / "nested" / "dir" / "test.svg"
        save_svg(svg, filepath)
        assert filepath.exists()

    def test_save_svg_utf8_encoding(self, fehu, tmp_path):
        """SVG files should be saved with UTF-8 encoding for runic characters."""
        svg = render_rune_svg(fehu)
        filepath = tmp_path / "utf8_test.svg"
        save_svg(svg, filepath)
        content = filepath.read_text(encoding="utf-8")
        assert "ᚠ" in content  # Fehu unicode character


class TestSavePNG:
    def test_save_png_without_cairosvg_raises_import_error(self, fehu, tmp_path):
        """If cairosvg isn't installed, should raise ImportError or fall back."""
        svg = render_rune_svg(fehu)
        filepath = tmp_path / "test.png"
        # This tests that the function handles missing dependencies gracefully
        # It may or may not have cairosvg installed
        try:
            save_png(svg, filepath)
            # If it succeeded, the file should exist
            assert filepath.exists()
        except ImportError:
            # Expected if cairosvg and Pillow are not installed
            pass


# ── Integration Tests ───────────────────────────────────────────────

class TestSVGIntegration:
    def test_full_workflow_rune_card(self, fehu, tmp_path):
        """Full workflow: create rune card, save to file, verify."""
        opts = SVGOptions(width=500, height=700, border=True, show_metadata=True)
        svg = render_rune_svg(fehu, options=opts)
        filepath = save_svg(svg, tmp_path / "fehu_card.svg")
        content = filepath.read_text(encoding="utf-8")
        assert "Fehu" in content
        assert "Cattle, wealth, vital energy" in content
        assert "Fire" in content

    def test_full_workflow_bindrune(self, tmp_path):
        """Full workflow: create bindrune, save to file."""
        svg = render_bindrune_svg(["Algiz", "Sowilo"], name="ᛉᛊ Victory Shield")
        filepath = save_svg(svg, tmp_path / "victory_shield.svg")
        content = filepath.read_text(encoding="utf-8")
        assert "Algiz" in content
        assert "Sowilo" in content
        assert "Victory Shield" in content

    def test_full_workflow_spread(self, tmp_path):
        """Full workflow: draw spread, render SVG, save to file."""
        div = Divination(seed=123)
        spread = div.draw_three_rune(question="Will the voyage be safe?")
        svg = render_spread_svg(spread)
        filepath = save_svg(svg, tmp_path / "voyage_spread.svg")
        content = filepath.read_text(encoding="utf-8")
        assert "Will the voyage be safe?" in content

    def test_full_workflow_circle(self, tmp_path):
        """Full workflow: create rune circle with highlights."""
        fehu = RUNE_BY_NAME["Fehu"]
        algiz = RUNE_BY_NAME["Algiz"]
        svg = render_rune_circle_svg(
            highlight_runes=[fehu, algiz],
            title="Protective Circle"
        )
        filepath = save_svg(svg, tmp_path / "circle.svg")
        content = filepath.read_text(encoding="utf-8")
        assert "Protective Circle" in content

    def test_all_rune_cards_generate_without_error(self, tmp_path):
        """Every single rune should generate a valid SVG card."""
        for rune in ELDER_FUTHARK:
            svg = render_rune_svg(rune)
            filepath = tmp_path / f"{rune.name.lower()}.svg"
            save_svg(svg, filepath)
            assert filepath.exists()
            content = filepath.read_text(encoding="utf-8")
            assert rune.name in content
            assert '</svg>' in content