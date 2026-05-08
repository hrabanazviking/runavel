"""
Elder Futhark Rune Dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The twenty-four runes of the Elder Futhark, organized in three aettir.
Each rune carries its name, phonetic value, Unicode character,
metaphysical meaning, associated element, and wyrd-numerological value.

The number associations follow the runic tradition:
  - First ætt (Freyja's): values shaped by abundance and flow
  - Second ætt (Heimdall's): values shaped by resistance and transformation
  - Third ætt (Týr's): values shaped by destiny and cosmic order

These are not arbitrary — they reflect the positional mysticism
of the futhark order and the sacred numerology of the Norse.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Aett(Enum):
    """The three families (ættir) of the Elder Futhark."""
    FREYJA = "Freyja's Ætt"
    HEIMDALL = "Heimdall's Ætt"
    TYR = "Týr's Ætt"


@dataclass(frozen=True)
class Rune:
    """A single Elder Futhark rune with all its metadata."""
    name: str               # e.g. "Fehu"
    unicode: str            # e.g. "ᚠ"
    phonetic: str           # e.g. "f"
    phonetic_alt: str       # e.g. "F" (uppercase form)
    meaning: str            # e.g. "Cattle, wealth"
    element: str            # e.g. "Fire"
    aett: Aett              # Which ætt this rune belongs to
    position_in_aett: int   # 1-8 within the ætt
    global_position: int    # 1-24 in the full futhark
    wyrd_value: int         # Numerological/associative value
    galdr: str              # The chanting sound for galdr
    keywords: tuple         # Keywords for divination
    inverse: Optional[str]  # Name of the rune in reversed/inverted position (if any)
    description: str        # Brief metaphysical description

    @property
    def aett_position_value(self) -> int:
        """Position within the ætt, used in some cipher modes."""
        return self.position_in_aett

    @property
    def is_reversible(self) -> bool:
        """Whether the rune has a distinct inverted meaning."""
        return self.inverse is not None


# =============================================================================
# THE ELDER FUTHARK — Complete Dataset
# =============================================================================

ELDER_FUTHARK: tuple[Rune, ...] = (

    # ─── FREYJA'S ÆTT ─────────────────────────────────────────────────────
    # The Ætt of Vitality: Fire, Earth, Thorn, Breath, Journey, Gift, Joy, Harvest
    # These runes speak of the forces that give life, sustain it, and test it.

    Rune(
        name="Fehu", unicode="ᚠ", phonetic="f", phonetic_alt="F",
        meaning="Cattle, wealth, vital energy",
        element="Fire", aett=Aett.FREYJA,
        position_in_aett=1, global_position=1, wyrd_value=1,
        galdr="fay-hooo",
        keywords=("wealth", "abundance", "energy", "flow", "generosity"),
        inverse=None,
        description="The golden pulse of vitality. Energy that must circulate or die."
    ),
    Rune(
        name="Uruz", unicode="ᚢ", phonetic="u", phonetic_alt="U",
        meaning="Aurochs, primal strength, health",
        element="Earth", aett=Aett.FREYJA,
        position_in_aett=2, global_position=2, wyrd_value=2,
        galdr="ooo-roooz",
        keywords=("strength", "endurance", "health", "vitality", "wild"),
        inverse="Uruz (inverted)",
        description="The untamed beast. Raw power that shatters old form for new growth."
    ),
    Rune(
        name="Thurisaz", unicode="ᚦ", phonetic="th", phonetic_alt="Þ",
        meaning="Thorn, giant, chaotic force",
        element="Fire", aett=Aett.FREYJA,
        position_in_aett=3, global_position=3, wyrd_value=3,
        galdr="thoo-ree-saz",
        keywords=("chaos", "protection", "thorn", "conflict", "awakening"),
        inverse="Thurisaz (inverted)",
        description="The thorn and the thunder. Necessary destruction that clears deadwood."
    ),
    Rune(
        name="Ansuz", unicode="ᚨ", phonetic="a", phonetic_alt="A",
        meaning="God, divine breath, Odin",
        element="Air", aett=Aett.FREYJA,
        position_in_aett=4, global_position=4, wyrd_value=4,
        galdr="ahn-soooz",
        keywords=("wisdom", "communication", "prophecy", "breath", "insight"),
        inverse=None,
        description="The breath of the Ash. Divine signal cutting through noise."
    ),
    Rune(
        name="Raidho", unicode="ᚱ", phonetic="r", phonetic_alt="R",
        meaning="Riding, journey, cosmic order",
        element="Air", aett=Aett.FREYJA,
        position_in_aett=5, global_position=5, wyrd_value=5,
        galdr="rye-tho",
        keywords=("journey", "movement", "rhythm", "order", "ritual"),
        inverse="Raidho (inverted)",
        description="The riding force. Right action in accordance with cosmic rhythm."
    ),
    Rune(
        name="Kenaz", unicode="ᚲ", phonetic="k", phonetic_alt="K",
        meaning="Torch, controlled fire, knowledge",
        element="Fire", aett=Aett.FREYJA,
        position_in_aett=6, global_position=6, wyrd_value=6,
        galdr="kay-naz",
        keywords=("knowledge", "illumination", "craft", "creativity", "fire"),
        inverse="Kenaz (inverted)",
        description="The torch in the dark. Craft-skill and the controlled flame of art."
    ),
    Rune(
        name="Gebo", unicode="ᚷ", phonetic="g", phonetic_alt="G",
        meaning="Gift, exchange, sacred partnership",
        element="Air", aett=Aett.FREYJA,
        position_in_aett=7, global_position=7, wyrd_value=7,
        galdr="gay-bo",
        keywords=("gift", "partnership", "exchange", "balance", "sacred bond"),
        inverse=None,  # Gebo cannot be inverted — it is always a cross
        description="The sacred exchange. What is given must be returned; all bonds require balance."
    ),
    Rune(
        name="Wunjo", unicode="ᚹ", phonetic="w", phonetic_alt="W",
        meaning="Joy, harmony, wish-fulfillment",
        element="Earth", aett=Aett.FREYJA,
        position_in_aett=8, global_position=8, wyrd_value=8,
        galdr="woon-yo",
        keywords=("joy", "harmony", "wish", "pleasure", "belonging"),
        inverse="Wunjo (inverted)",
        description="The wish fulfilled. Harmony born from the balance of all forces."
    ),

    # ─── HEIMDALL'S ÆTT ────────────────────────────────────────────────────
    # The Ætt of Resistance: Hail, Need, Ice, Harvest, Warrior, Birch, Horse, Light
    # These runes speak of the forces that test, transform, and ultimately reveal truth.

    Rune(
        name="Hagalaz", unicode="ᚺ", phonetic="h", phonetic_alt="H",
        meaning="Hail, disruption, the seed of change",
        element="Water", aett=Aett.HEIMDALL,
        position_in_aett=1, global_position=9, wyrd_value=9,
        galdr="hah-gah-laz",
        keywords=("disruption", "hail", "chaos", "transformation", "testing"),
        inverse=None,  # Hagalaz cannot be inverted — hail has no reverse
        description="The hail-storm that shatters illusion. Growth through destruction."
    ),
    Rune(
        name="Nauthiz", unicode="ᚾ", phonetic="n", phonetic_alt="N",
        meaning="Need, constraint, necessity-born innovation",
        element="Fire", aett=Aett.HEIMDALL,
        position_in_aett=2, global_position=10, wyrd_value=10,
        galdr="now-theez",
        keywords=("need", "constraint", "necessity", "innovation", "endurance"),
        inverse="Nauthiz (inverted)",
        description="The fire born from friction. Necessity drives all invention."
    ),
    Rune(
        name="Isa", unicode="ᛁ", phonetic="i", phonetic_alt="I",
        meaning="Ice, stillness, contraction",
        element="Water", aett=Aett.HEIMDALL,
        position_in_aett=3, global_position=11, wyrd_value=11,
        galdr="ee-sah",
        keywords=("ice", "stillness", "pause", "concentration", "contracts"),
        inverse=None,  # Isa cannot be inverted — ice is symmetric
        description="The ice that concentrates. Stillness is not death but gestation."
    ),
    Rune(
        name="Jera", unicode="ᛃ", phonetic="j", phonetic_alt="J",
        meaning="Harvest, cyclical completion, reward",
        element="Earth", aett=Aett.HEIMDALL,
        position_in_aett=4, global_position=12, wyrd_value=12,
        galdr="yay-rah",
        keywords=("harvest", "cycle", "reward", "patience", "completion"),
        inverse=None,  # Jera cannot be inverted — cycles have no reverse
        description="The turning of the year. What was sown must be reaped."
    ),
    Rune(
        name="Eihwaz", unicode="ᛇ", phonetic="ï", phonetic_alt="Ï",
        meaning="Yew, endurance, the axis between worlds",
        element="All", aett=Aett.HEIMDALL,
        position_in_aett=5, global_position=13, wyrd_value=13,
        galdr="eye-waz",
        keywords=("yew", "endurance", "axis", "transformation", "between-worlds"),
        inverse=None,  # Eihwaz cannot be inverted — the axis stands
        description="The yew that endures. The world-axis between life and death."
    ),
    Rune(
        name="Perthro", unicode="ᛈ", phonetic="p", phonetic_alt="P",
        meaning="Fate-dice, mystery, the well of wyrd",
        element="Water", aett=Aett.HEIMDALL,
        position_in_aett=6, global_position=14, wyrd_value=14,
        galdr="per-thro",
        keywords=("fate", "mystery", "divination", "chance", "hidden"),
        inverse="Perthro (inverted)",
        description="The dice-cup of fate. Mystery revealed through surrender to the unknown."
    ),
    Rune(
        name="Algiz", unicode="ᛉ", phonetic="z", phonetic_alt="Z",
        meaning="Elk-sedge, protection, the reaching hand",
        element="Air", aett=Aett.HEIMDALL,
        position_in_aett=7, global_position=15, wyrd_value=15,
        galdr="ahl-geez",
        keywords=("protection", "shield", "connection", "reaching", "sacred"),
        inverse="Algiz (inverted)",
        description="The elk-sedge guarding the path. Protection through openness, not walls."
    ),
    Rune(
        name="Sowilo", unicode="ᛊ", phonetic="s", phonetic_alt="S",
        meaning="Sun, victory, the lightning-flash of will",
        element="Fire", aett=Aett.HEIMDALL,
        position_in_aett=8, global_position=16, wyrd_value=16,
        galdr="so-wee-lo",
        keywords=("sun", "victory", "will", "lightning", "wholeness"),
        inverse=None,  # Sowilo cannot be inverted — the sun has no reverse
        description="The sun-flash of certain will. Victory through clarity and purpose."
    ),

    # ─── TYR'S ÆTT ─────────────────────────────────────────────────────────
    # The Ætt of Destiny: Kin, Harvest, War, Birch, Horse, Water, Inheritance, Day
    # These runes speak of the forces that bind communities, move between worlds,
    # and carry the weight of ancestral wyrd.

    Rune(
        name="Tiwaz", unicode="ᛏ", phonetic="t", phonetic_alt="T",
        meaning="Týr, justice, the warrior's sacrifice",
        element="Air", aett=Aett.TYR,
        position_in_aett=1, global_position=17, wyrd_value=17,
        galdr="tee-waz",
        keywords=("justice", "sacrifice", "honor", "warrior", "truth"),
        inverse="Tiwaz (inverted)",
        description="The one-handed god's rune. Justice demands sacrifice; honor demands truth."
    ),
    Rune(
        name="Berkano", unicode="ᛒ", phonetic="b", phonetic_alt="B",
        meaning="Birch, birth, nurturing renewal",
        element="Earth", aett=Aett.TYR,
        position_in_aett=2, global_position=18, wyrd_value=18,
        galdr="bear-kah-no",
        keywords=("birth", "renewal", "nurturing", "growth", "birch"),
        inverse="Berkano (inverted)",
        description="The birch pushing through snow. New life nurtured in darkness."
    ),
    Rune(
        name="Ehwaz", unicode="ᛖ", phonetic="e", phonetic_alt="E",
        meaning="Horse, trust, the sacred partnership",
        element="Earth", aett=Aett.TYR,
        position_in_aett=3, global_position=19, wyrd_value=19,
        galdr="ay-waz",
        keywords=("trust", "partnership", "movement", "horse", "loyalty"),
        inverse="Ehwaz (inverted)",
        description="The horse carrying rider and mount as one. Trust that transforms movement."
    ),
    Rune(
        name="Mannaz", unicode="ᛗ", phonetic="m", phonetic_alt="M",
        meaning="Human, self-knowledge, the community mind",
        element="Air", aett=Aett.TYR,
        position_in_aett=4, global_position=20, wyrd_value=20,
        galdr="man-naz",
        keywords=("self", "humanity", "community", "intelligence", "identity"),
        inverse="Mannaz (inverted)",
        description="The rune of self-knowing. We are the lens through which the divine sees itself."
    ),
    Rune(
        name="Laguz", unicode="ᛚ", phonetic="l", phonetic_alt="L",
        meaning="Water, flow, the unconscious depths",
        element="Water", aett=Aett.TYR,
        position_in_aett=5, global_position=21, wyrd_value=21,
        galdr="lah-gooz",
        keywords=("water", "flow", "intuition", "depths", "unconscious"),
        inverse="Laguz (inverted)",
        description="The deep water flowing. Intuition that knows what logic cannot."
    ),
    Rune(
        name="Ingwaz", unicode="ᛜ", phonetic="ng", phonetic_alt="Ŋ",
        meaning="Freyr, fertility, the seed completing itself",
        element="Earth", aett=Aett.TYR,
        position_in_aett=6, global_position=22, wyrd_value=22,
        galdr="ing-waz",
        keywords=("fertility", "completion", "seed", "gestation", "Freyr"),
        inverse=None,  # Ingwaz cannot be inverted — the seed contains its own future
        description="The seed completing its own becoming. Gestation and sacred completion."
    ),
    Rune(
        name="Dagaz", unicode="ᛞ", phonetic="d", phonetic_alt="D",
        meaning="Day, dawn, the breakthrough to clarity",
        element="Fire", aett=Aett.TYR,
        position_in_aett=7, global_position=23, wyrd_value=23,
        galdr="dah-gaz",
        keywords=("dawn", "breakthrough", "clarity", "awakening", "day"),
        inverse=None,  # Dagaz cannot be inverted — dawn has no reverse
        description="The dawn breaking through. Enlightenment as sudden, total clarity."
    ),
    Rune(
        name="Othala", unicode="ᛟ", phonetic="o", phonetic_alt="O",
        meaning="Ancestral homestead, sacred inheritance",
        element="Earth", aett=Aett.TYR,
        position_in_aett=8, global_position=24, wyrd_value=24,
        galdr="oh-thah-lah",
        keywords=("heritage", "homeland", "ancestry", "inheritance", "sacred ground"),
        inverse="Othala (inverted)",
        description="The ancestral homestead. What we inherit and what we mustProtect."
    ),
)


# =============================================================================
# Lookup Dictionaries
# =============================================================================

# Primary lookups
RUNE_BY_NAME: dict[str, Rune] = {r.name: r for r in ELDER_FUTHARK}
RUNE_BY_UNICODE: dict[str, Rune] = {r.unicode: r for r in ELDER_FUTHARK}
RUNE_BY_PHONETIC: dict[str, Rune] = {r.phonetic: r for r in ELDER_FUTHARK}
RUNE_BY_PHONETIC_ALT: dict[str, Rune] = {r.phonetic_alt: r for r in ELDER_FUTHARK}
RUNE_BY_POSITION: dict[int, Rune] = {r.global_position: r for r in ELDER_FUTHARK}
RUNE_BY_WYRD: dict[int, Rune] = {r.wyrd_value: r for r in ELDER_FUTHARK}

# Ætt groupings
AETTIR: dict[Aett, tuple[Rune, ...]] = {
    Aett.FREYJA: tuple(r for r in ELDER_FUTHARK if r.aett == Aett.FREYJA),
    Aett.HEIMDALL: tuple(r for r in ELDER_FUTHARK if r.aett == Aett.HEIMDALL),
    Aett.TYR: tuple(r for r in ELDER_FUTHARK if r.aett == Aett.TYR),
}

# Elements
ELEMENTS: tuple[str, ...] = ("Fire", "Earth", "Air", "Water", "All")
RUNES_BY_ELEMENT: dict[str, tuple[Rune, ...]] = {
    e: tuple(r for r in ELDER_FUTHARK if r.element == e)
    for e in ELEMENTS
}