"""Tests for the Elder Futhark rune dataset."""

import pytest
from runavel.runes import (
    Aett,
    ELDER_FUTHARK,
    RUNE_BY_NAME,
    RUNE_BY_PHONETIC,
    RUNE_BY_PHONETIC_ALT,
    RUNE_BY_POSITION,
    RUNE_BY_UNICODE,
    RUNE_BY_WYRD,
    AETTIR,
    ELEMENTS,
    RUNES_BY_ELEMENT,
    Rune,
)


class TestRuneDataclass:
    """Tests for the Rune dataclass and its properties."""

    def test_elder_futhark_has_24_runes(self):
        assert len(ELDER_FUTHARK) == 24

    def test_all_runes_are_rune_instances(self):
        assert all(isinstance(r, Rune) for r in ELDER_FUTHARK)

    def test_global_positions_are_unique_and_contiguous(self):
        positions = [r.global_position for r in ELDER_FUTHARK]
        assert sorted(positions) == list(range(1, 25))

    def test_wyrd_values_are_unique_and_contiguous(self):
        values = [r.wyrd_value for r in ELDER_FUTHARK]
        assert sorted(values) == list(range(1, 25))

    def test_rune_is_frozen(self):
        fehu = ELDER_FUTHARK[0]
        with pytest.raises(AttributeError):
            fehu.name = "NotFehu"

    def test_reversible_runes_have_inverse(self):
        for rune in ELDER_FUTHARK:
            if rune.is_reversible:
                assert rune.inverse is not None
            else:
                assert rune.inverse is None

    def test_specific_rune_properties(self):
        fehu = RUNE_BY_NAME["Fehu"]
        assert fehu.unicode == "ᚠ"
        assert fehu.phonetic == "f"
        assert fehu.aett == Aett.FREYJA
        assert fehu.global_position == 1
        assert fehu.wyrd_value == 1
        assert fehu.is_reversible is False

    def test_othala_inverse(self):
        othala = RUNE_BY_NAME["Othala"]
        assert othala.is_reversible is True
        assert othala.inverse == "Othala (inverted)"


class TestLookupDictionaries:
    """Tests for the lookup dictionaries."""

    def test_rune_by_name_coverage(self):
        assert len(RUNE_BY_NAME) == 24

    def test_rune_by_unicode_coverage(self):
        assert len(RUNE_BY_UNICODE) == 24

    def test_rune_by_phonetic_coverage(self):
        # 24 primary phonetic values
        assert len(RUNE_BY_PHONETIC) == 24

    def test_rune_by_position_coverage(self):
        assert len(RUNE_BY_POSITION) == 24

    def test_rune_by_wyrd_coverage(self):
        assert len(RUNE_BY_WYRD) == 24

    def test_name_lookup_roundtrip(self):
        for rune in ELDER_FUTHARK:
            assert RUNE_BY_NAME[rune.name] is rune

    def test_unicode_lookup_roundtrip(self):
        for rune in ELDER_FUTHARK:
            assert RUNE_BY_UNICODE[rune.unicode] is rune

    def test_position_lookup_roundtrip(self):
        for rune in ELDER_FUTHARK:
            assert RUNE_BY_POSITION[rune.global_position] is rune


class TestAettir:
    """Tests for ætt groupings."""

    def test_three_aettir(self):
        assert len(AETTIR) == 3

    def test_each_aett_has_8_runes(self):
        for aett_runes in AETTIR.values():
            assert len(aett_runes) == 8

    def test_aett_membership(self):
        for aett, runes in AETTIR.items():
            for rune in runes:
                assert rune.aett == aett

    def test_freyja_aett_first_rune(self):
        assert AETTIR[Aett.FREYJA][0].name == "Fehu"

    def test_tyr_aett_last_rune(self):
        assert AETTIR[Aett.TYR][-1].name == "Othala"


class TestElements:
    """Tests for elemental groupings."""

    def test_five_elements(self):
        assert len(ELEMENTS) == 5

    def test_all_runes_have_valid_element(self):
        for rune in ELDER_FUTHARK:
            assert rune.element in ELEMENTS

    def test_element_coverage(self):
        total = sum(len(runes) for runes in RUNES_BY_ELEMENT.values())
        assert total == 24

    def test_fire_runes(self):
        assert len(RUNES_BY_ELEMENT["Fire"]) > 0
        assert all(r.element == "Fire" for r in RUNES_BY_ELEMENT["Fire"])