from __future__ import annotations

from functools import reduce
from typing import NamedTuple


class Token(NamedTuple):
    value: str
    type: str


class Emote(NamedTuple):
    value: str
    anger: float
    number: int = 1
    bold: bool = False
    emph: bool = False
    strike: bool = False

    def is_emoji(self):
        return self.value.startswith(":") and self.value.endswith(":")

    @classmethod
    def join_words(cls, emotes: list[Emote]) -> Emote:
        def reduce_emotes(emote1: Emote, emote2: Emote) -> Emote:
            if emote1.is_emoji():
                raise TypeError()
            
            if emote2.is_emoji():
                return emote1
            
            return cls(
                emote1.value + ' ' + emote2.value,
                (emote1.anger + emote2.anger) / 2,
                emote1.number,
                emote1.bold,
                emote1.emph,
                emote1.strike,
            )
        
        try:
            return reduce(reduce_emotes, emotes)
        except TypeError:
            return Emote("", 100)
