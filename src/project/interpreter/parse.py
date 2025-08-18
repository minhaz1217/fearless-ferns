from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .models import Emote, Token
from .nlp import EmojiCategory, identify_emoji
from .tokenizer import tokenize

if TYPE_CHECKING:
    from collections.abc import Generator


def parse(content: str, *, anger: float = 10.0) -> Generator[Emote, None, None]:
    """Emotional parsing function. Generates emotes."""
    bold = False
    emph = False  # emphasis: italic or underline
    strike = False
    number = 1

    for token in tokenize(content):
        match token:
            case Token(type="B"):
                bold = not bold
            case Token(type="I"):
                emph = not emph
            case Token(type="S"):
                strike = not strike

            case Token(value, type="E"):
                anger = emoji_relief(anger, value)
                yield Emote(value, anger, number, bold, emph, strike)

            case Token(value, type="W"):
                anger = word_relief(anger, value)
                yield Emote(value, anger, number, bold, emph, strike)

            case Token(value, type="N"):
                try:
                    number = round(float(value))
                except ValueError:
                    number = 0
                    anger += len(value.replace(".", ""))

            case Token(value, type="U"):
                anger += len(re.sub(r"\s", "", value))


emoji_relief_factor: dict[EmojiCategory, float] = {
    "positive": 100,
    "negative": -90,
    "gesture": 20,
    "heart": 50,
    "food": 100,
    "animal": 30,
}


def emoji_relief(anger: float, emo: str) -> float:
    """Relieves the parser's anger by the effect of emojies."""
    (cat, rat), _ = identify_emoji(emo)
    return anger - emoji_relief_factor[cat] * rat


def word_relief(anger: float, word: str) -> float:
    """Relieve the parser's anger by the effect of a pseudo-emoji made from words.

    The effect is less pronounced however.
    """
    pseudo_emoji = f":{word}:"
    (cat, rat), _ = identify_emoji(pseudo_emoji)
    return anger - emoji_relief_factor[cat] * rat * 0.1
