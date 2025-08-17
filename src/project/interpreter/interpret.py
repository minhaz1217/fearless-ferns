from __future__ import annotations

import io
from itertools import takewhile
import operator as op

import emoji

from .cleanup import cleanup
from .models import Emote
from .nlp import identify_shape, get_shape, summarize_to_phrase
from .parse import parse


def id_from_emoji(emo):
    return f"c{emo[1:-1]}"


def interpret(content: str):
    f = io.StringIO()
    f.write("flowchart TD\n")

    def node(id_, label, shape):
        return f"{id_}@{{ shape: {shape}, label: '{label}' }}\n"

    for line in cleanup(content).splitlines():
        emojies: list[Emote] = []
        words: list[Emote] = []
        discarded: list[Emote] = []
        
        for emote in parse(line):
            # Each list will fill with corresponding type
            (emojies if emote.is_emoji() else words).append(emote)
            
            # Except that words that occur before the first emoji are moved
            if words and not emojies:
                discarded.append(words.pop())
            
        
        # Each line must contain only one emoji
        if len(emojies) != 1:
            continue
        
        emo, = emojies
        id_ = id_from_emoji(emo.value)
        joined = Emote.join_words(words)

        if len(joined.value.split(' ')) >= 3:
            text = summarize_to_phrase(joined.value)
        elif joined.value:
            text = joined.value
        else:
            text = emoji.emojize(emo.value)
        
        # infer the shape
        shape = choose_shape(line) or choose_shape(Emote.join_words(discarded).value) or "rect"
        
        # write the data
        f.write(node(id_, text, shape))
    
    f.seek(0)
    return f.read()


def choose_shape(line: str) -> str | None:
    (cat, rat), _ = identify_shape(line)
    if rat >= 0.80:
        return get_shape(cat)
    else:
        return None