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