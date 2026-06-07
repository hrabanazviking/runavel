"""Tests for the CLI interface."""

import pytest
from unittest.mock import patch
from io import StringIO

from runavel.cli import main


class TestCLI:
    """Tests for the CLI entry point."""

    def test_futhark_command(self, capsys):
        with patch("sys.argv", ["runavel", "futhark"]):
            main()
        captured = capsys.readouterr()
        assert "ELDER FUTHARK" in captured.out

    def test_info_command(self, capsys):
        with patch("sys.argv", ["runavel", "info", "Fehu"]):
            main()
        captured = capsys.readouterr()
        assert "Fehu" in captured.out
        assert "ᚠ" in captured.out

    def test_encode_command(self, capsys):
        with patch("sys.argv", ["runavel", "encode", "fehu"]):
            main()
        captured = capsys.readouterr()
        assert "ᚠ" in captured.out

    def test_decode_command(self, capsys):
        with patch("sys.argv", ["runavel", "decode", "ᚠ"]):
            main()
        captured = capsys.readouterr()
        assert "f" in captured.out

    def test_draw_command(self, capsys):
        with patch("sys.argv", ["runavel", "draw"]):
            main()
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_spread_command(self, capsys):
        with patch("sys.argv", ["runavel", "spread", "What path?"]):
            main()
        captured = capsys.readouterr()
        assert "WYRD-READING" in captured.out or "RÚNAVÉL" in captured.out

    def test_banner_command(self, capsys):
        with patch("sys.argv", ["runavel", "banner"]):
            main()
        captured = capsys.readouterr()
        # Banner uses spaced letters: "R Ú N A V É L"
        assert "R Ú N A V É L" in captured.out or "RÚNAVÉL" in captured.out

    def test_no_command_shows_banner(self, capsys):
        with patch("sys.argv", ["runavel"]):
            main()
        captured = capsys.readouterr()
        assert "R Ú N A V É L" in captured.out or "RÚNAVÉL" in captured.out


class TestCLIRenderCommands:
    """Tests for SVG/PNG render CLI commands."""

    def test_render_rune_svg(self, capsys, tmp_path):
        output = str(tmp_path / "fehu.svg")
        with patch("sys.argv", ["runavel", "render-rune", "Fehu", "-o", output]):
            main()
        captured = capsys.readouterr()
        import os
        assert os.path.exists(output)
        content = open(output, encoding="utf-8").read()
        assert "Fehu" in content

    def test_render_rune_custom_style(self, capsys, tmp_path):
        output = str(tmp_path / "styled.svg")
        with patch("sys.argv", ["runavel", "render-rune", "Fehu", "-o", output,
                                 "--stroke-color", "#FF0000", "--background", "#000000"]):
            main()
        content = open(output, encoding="utf-8").read()
        assert "#FF0000" in content
        assert "#000000" in content

    def test_render_bindrune_svg(self, capsys, tmp_path):
        output = str(tmp_path / "bind.svg")
        with patch("sys.argv", ["runavel", "render-bindrune", "Fehu", "Uruz", "-o", output,
                                 "--name", "test bind"]):
            main()
        captured = capsys.readouterr()
        import os
        assert os.path.exists(output)

    def test_render_circle_svg(self, capsys, tmp_path):
        output = str(tmp_path / "circle.svg")
        with patch("sys.argv", ["runavel", "render-circle", "-o", output,
                                 "--title", "Test Circle"]):
            main()
        content = open(output, encoding="utf-8").read()
        assert "Test Circle" in content

    def test_render_futhark_svg(self, capsys, tmp_path):
        output = str(tmp_path / "futhark.svg")
        with patch("sys.argv", ["runavel", "render-futhark", "-o", output]):
            main()
        content = open(output, encoding="utf-8").read()
        assert "ELDER FUTHARK" in content

    def test_render_rune_unknown_rune(self, capsys):
        with patch("sys.argv", ["runavel", "render-rune", "Zzzzz"]):
            main()
        captured = capsys.readouterr()
        assert "Unknown rune" in captured.out