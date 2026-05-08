"""
Runic Divination Engine
~~~~~~~~~~~~~~~~~~~~~~~~~
Three-rune spreads and wyrd-readings.

Runic divination is not fortune-telling in the cheap modern sense.
It is the art of reading the currents of wyrd — the great web
of cause and consequence that the Norns weave at the well of Urdhr.

Each spread draws runes from the futhark, considers their positions,
their relationships to each other, and their elemental resonances
to weave a reading that speaks to the question at hand.

The Norns do not determine your fate. They reveal its shape.
What you do with that shape is your own wyrd to weave.
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .runes import (
    ELDER_FUTHARK,
    RUNE_BY_NAME,
    Aett,
    Rune,
    AETTIR,
)


class SpreadType(Enum):
    """Types of rune spreads."""
    SINGLE = "single"
    THREE_RUNE = "three_rune"
    THREE_AETT = "three_aett"  # One from each ætt
    FULL_FUTHARK = "full_futhark"


class SpreadPosition(Enum):
    """Positions in a three-rune spread."""
    PAST = "past"           # What has shaped you
    PRESENT = "present"     # Where you stand now
    FUTURE = "future"       # What is becoming


@dataclass
class DrawnRune:
    """A rune drawn in a divination spread with contextual metadata."""
    rune: Rune
    position: Optional[SpreadPosition] = None
    is_reversed: bool = False
    spread_type: Optional[SpreadType] = None

    def __str__(self) -> str:
        pos_label = f" ({self.position.value})" if self.position else ""
        rev_label = " ᚨ REVERSED" if self.is_reversed else ""
        return f"{self.rune.unicode} {self.rune.name}{pos_label}{rev_label}"


@dataclass
class Spread:
    """A complete divination spread."""
    spread_type: SpreadType
    runes: list[DrawnRune]
    question: Optional[str] = None
    timestamp: Optional[str] = None

    def __str__(self) -> str:
        lines = [f"{'━' * 40}"]
        if self.question:
            lines.append(f"  Question: {self.question}")
        lines.append(f"  Spread: {self.spread_type.value}")
        lines.append(f"{'━' * 40}")
        for d in self.runes:
            lines.append(f"  {d}")
        lines.append(f"{'━' * 40}")
        return "\n".join(lines)


class Divination:
    """
    The völva's craft — drawing and interpreting rune spreads.

    This is not random number generation. The Norns place the runes
    where they will. We merely draw them and read what the web reveals.
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the divination engine.

        Args:
            seed: Optional seed for reproducibility (testing/ritual use).
                  If None, the Norns decide through system entropy.
        """
        self._rng = random.Random(seed)

    def draw_single(self, question: Optional[str] = None) -> Spread:
        """Draw a single rune for quick guidance."""
        rune = self._rng.choice(ELDER_FUTHARK)
        is_reversed = rune.is_reversible and self._rng.random() < 0.25

        drawn = DrawnRune(
            rune=rune,
            position=None,
            is_reversed=is_reversed,
            spread_type=SpreadType.SINGLE,
        )
        return Spread(
            spread_type=SpreadType.SINGLE,
            runes=[drawn],
            question=question,
        )

    def draw_three_rune(
        self,
        question: Optional[str] = None,
        allow_reversals: bool = True,
    ) -> Spread:
        """
        Draw a classic three-rune spread: Past, Present, Future.

        This is the most common divination spread. It reads the
        current of wyrd flowing through time — what was, what is,
        and what is becoming.
        """
        # Draw without replacement
        drawn_runes = self._rng.sample(list(ELDER_FUTHARK), 3)

        spread_runes = []
        for i, rune in enumerate(drawn_runes):
            is_reversed = (
                allow_reversals
                and rune.is_reversible
                and self._rng.random() < 0.25
            )
            spread_runes.append(DrawnRune(
                rune=rune,
                position=list(SpreadPosition)[i],
                is_reversed=is_reversed,
                spread_type=SpreadType.THREE_RUNE,
            ))

        return Spread(
            spread_type=SpreadType.THREE_RUNE,
            runes=spread_runes,
            question=question,
        )

    def draw_three_aett(
        self,
        question: Optional[str] = None,
    ) -> Spread:
        """
        Draw one rune from each ætt: Freyja's, Heimdall's, Týr's.

        This spread reads from the three houses of the futhark:
          - Freyja's Ætt: Vitality and earthly forces
          - Heimdall's Ætt: Resistance and transformation
          - Týr's Ætt: Destiny and cosmic order

        Together they reveal how primal force, transformative pressure,
        and destiny's pull shape your current path.
        """
        freyja_rune = self._rng.choice(AETTIR[Aett.FREYJA])
        heimdall_rune = self._rng.choice(AETTIR[Aett.HEIMDALL])
        tyr_rune = self._rng.choice(AETTIR[Aett.TYR])

        spread_runes = [
            DrawnRune(
                rune=freyja_rune,
                position=SpreadPosition.PAST,
                is_reversed=freyja_rune.is_reversible and self._rng.random() < 0.25,
                spread_type=SpreadType.THREE_AETT,
            ),
            DrawnRune(
                rune=heimdall_rune,
                position=SpreadPosition.PRESENT,
                is_reversed=heimdall_rune.is_reversible and self._rng.random() < 0.25,
                spread_type=SpreadType.THREE_AETT,
            ),
            DrawnRune(
                rune=tyr_rune,
                position=SpreadPosition.FUTURE,
                is_reversed=tyr_rune.is_reversible and self._rng.random() < 0.25,
                spread_type=SpreadType.THREE_AETT,
            ),
        ]

        return Spread(
            spread_type=SpreadType.THREE_AETT,
            runes=spread_runes,
            question=question,
        )

    def interpret(self, spread: Spread) -> str:
        """
        Weave a narrative interpretation from a spread.

        This is not rote keyword extraction. This reads the
        relationships between runes — their elements, their
        ættir, their positions — and weaves them into a
        flowing narrative of meaning.
        """
        lines = []

        # Header
        lines.append("╔" + "═" * 48 + "╗")
        lines.append("║" + "  WYRD-READING  ·  RÚNAVÉL  ".center(48) + "║")
        lines.append("╠" + "═" * 48 + "╣")

        if spread.question:
            lines.append("║" + f"  Question: {spread.question}".ljust(48) + "║")
            lines.append("║" + "─" * 48 + "║")

        # Elemental tally
        elements = [d.rune.element for d in spread.runes]
        element_counts = {}
        for e in elements:
            element_counts[e] = element_counts.get(e, 0) + 1

        dom_element = max(element_counts, key=element_counts.get)
        element_meanings = {
            "Fire": "action, will, transformation",
            "Earth": "grounding, material, nurturing",
            "Air": "thought, communication, intellect",
            "Water": "emotion, intuition, flow",
            "All": "total synthesis, axis, transcendence",
        }

        for i, drawn in enumerate(spread.runes):
            rune = drawn.rune
            pos_label = drawn.position.value if drawn.position else f"position {i+1}"
            rev_text = " (INVERTED)" if drawn.is_reversed else ""

            lines.append("║" + f"  {pos_label.upper()}{rev_text}".ljust(48) + "║")
            lines.append("║" + f"    {rune.unicode} {rune.name} — {rune.meaning}".ljust(48) + "║")
            lines.append("║" + f"    Ætt: {rune.aett.value}  ·  Element: {rune.element}".ljust(48) + "║")
            lines.append("║" + f"    Keywords: {', '.join(rune.keywords[:3])}".ljust(48) + "║")

            if drawn.is_reversed and rune.inverse:
                lines.append("║" + f"    ⚠ Inverted: energies blocked or delayed".ljust(48) + "║")

            # Description
            desc = rune.description
            if len(desc) > 44:
                desc = desc[:42] + "…"
            lines.append("║" + f"    \"{desc}\"".ljust(48) + "║")
            lines.append("║" + "  " + "─" * 46 + "║")

        # Synthesis
        lines.append("║" + f"  Dominant Element: {dom_element}".ljust(48) + "║")
        lines.append("║" + f"  ({element_meanings.get(dom_element, 'unknown')})".ljust(48) + "║")

        # Ætt balance
        aett_counts = {}
        for d in spread.runes:
            aett_name = d.rune.aett.value
            aett_counts[aett_name] = aett_counts.get(aett_name, 0) + 1

        aett_str = ", ".join(f"{k}×{v}" for k, v in aett_counts.items())
        lines.append("║" + f"  Ætt Balance: {aett_str}".ljust(48) + "║")

        # Wyrd sum
        wyrd_sum = sum(d.rune.wyrd_value for d in spread.runes)
        wyrd_reduced = wyrd_sum
        while wyrd_reduced > 24:
            wyrd_reduced = sum(int(d) for d in str(wyrd_reduced))

        lines.append("║" + f"  Wyrd Sum: {wyrd_sum} (reduced: {wyrd_reduced})".ljust(48) + "║")

        # Find the rune associated with the reduced wyrd value
        from .runes import RUNE_BY_WYRD
        if wyrd_reduced in RUNE_BY_WYRD:
            wyrd_rune = RUNE_BY_WYRD[wyrd_reduced]
            lines.append("║" + f"  Wyrd Rune: {wyrd_rune.unicode} {wyrd_rune.name}".ljust(48) + "║")
            lines.append("║" + f"    ({wyrd_rune.meaning})".ljust(48) + "║")

        lines.append("╚" + "═" * 48 + "╝")

        return "\n".join(lines)


def quick_reading(question: Optional[str] = None, seed: Optional[int] = None) -> str:
    """
    Quick one-shot divination function.

    Draws a three-rune spread and returns the full interpretation.
    For those moments when you need the Norns' counsel immediately.
    """
    div = Divination(seed=seed)
    spread = div.draw_three_rune(question=question)
    return div.interpret(spread)