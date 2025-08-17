from __future__ import annotations

from functools import reduce
import io
from itertools import takewhile
import operator as op

import emoji

from .cleanup import cleanup, clean_emoji
from .models import Emote
from .nlp import identify_shape, get_shape, summarize_to_phrase
from .parse import parse


def id_from_emoji(emo):
    return f"c{clean_emoji(emo)}"


def interpret(content: str):
    f = io.StringIO()
    f.write("flowchart TD\n")
    nodes_id_to_text = {}

    def make_node(id_, text, shape):
        f.write(f"{id_}@{{ shape: {shape}, label: '{text}' }}\n")
        nodes_id_to_text[id_] = text

    def get_node(emote: Emote) -> str:
        id_ = id_from_emoji(emote.value)
        
        if id_ not in nodes_id_to_text:
            text = emoji.emojize(emote.value)
            nodes_id_to_text[id_] = text
            return f"{id_}[{text}]"

        return id_

    def make_edge(emote1, emote2):
        n1 = get_node(emote1)
        n2 = get_node(emote2)
        
        f.write(f"{n1} --> {n2}\n")
        return emote2

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
            
        # no emojies in a line? ignore the comment
        if len(emojies) == 0:
            continue
        # One emoji per line defines the node
        elif len(emojies) == 1:
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
            make_node(id_, text, shape)
        else:
            # make connection between each 2 nodes ignoring the text
            reduce(make_edge, emojies)
    
    f.seek(0)
    return f.read()


def choose_shape(line: str) -> str | None:
    (cat, rat), _ = identify_shape(line)
    if rat >= 0.80:
        return get_shape(cat)
    else:
        return None