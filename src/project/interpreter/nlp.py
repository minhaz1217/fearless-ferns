from __future__ import annotations

import functools
import operator as op
import sys
from typing import Literal, TypeAlias

import spacy

from .cleanup import clean_emoji


# Smallest model that supports `similarity` method
_spacy_model = "en_core_web_md"

try:
    nlp = spacy.load(_spacy_model)
except OSError:
    commands = f"python -m pip install -U pip setuptools wheel\n\tpython -m spacy download {_spacy_model}"
    print(f"Couldn't load spacy language model. Run this command\n\n\t{commands}")
    sys.exit(1)


EmojiCategory: TypeAlias = (
    Literal["positive"]
    | Literal["negative"]
    | Literal["animal"]
    | Literal["food"]
    | Literal["gesture"]
    | Literal["heart"]
)
VALUES_SEPARATOR = ", "

# Used to narrow down emojies
emoji_categories: dict[EmojiCategory, str] = {
    "positive": "face, happy, fun, active, joy, energy, heart, grinning, big eyes",
    "negative": "face, sad, lazy, symbols, hot, nausea, vomiting, bandage",
    "gesture": "gesture, thumb, fist, hands, palms, biceps, salute, sign, fingers",
    "heart": "heart, exclamation, red, green, yellow, blue, chocolate",
    "animal": "animal, cat, dog, mouse, frog, hamster, cow, lion",
    "food": "food, apple, orange, pear, tangerine, lemon, hot dog, sandwich",
}


@functools.lru_cache
def _emoji_docs(category):
    return [nlp(value) for value in emoji_categories[category].split(VALUES_SEPARATOR)]


def identify_emoji(emoji) -> tuple[tuple[EmojiCategory, float], tuple[EmojiCategory, float]]:
    """Return top-2 matching emoji categories for the given emoji."""
    # removing colons and replacing underscores
    emo = clean_emoji(emoji, replace_underscores=True)
    emo_doc = nlp(emo)

    result: dict[EmojiCategory, float] = {
        category: max(emo_doc.similarity(doc) for doc in _emoji_docs(category)) for category in emoji_categories
    }

    values = list(result.items())
    values.sort(key=op.itemgetter(1), reverse=True)

    first, second, *_ = values
    return first, second


shapes = {
    "Card": "notch-rect, card, notched-rectangle",
    "Collate": "hourglass, collate, hourglass",
    "Com Link": "bolt, com-link, lightning-bolt",
    "Comment": "brace, brace-l, comment",
    "Comment Right": "brace-r",
    "Comment Both": "braces",
    "Data I/O Lean Right": "lean-r, lean-right, in-out",
    "Data I/O Lean Left": "lean-l, lean-left, out-in",
    "Database": "cyl, cylinder, database, db",
    "Decision": "diam, diamond, decision, question",
    "Delay": "delay, half-rounded-rectangle",
    "DAS (Horizontal Cylinder)": "h-cyl, das, horizontal-cylinder",
    "Disk Storage": "lin-cyl, disk, lined-cylinder",
    "Display": "curv-trap, curved-trapezoid, display",
    "Divided Process": "div-rect, div-proc, divided-process, divided-rectangle",
    "Document": "doc, document",
    "Event (Rounded Rectangle)": "rounded, event",
    "Extract": "tri, extract, triangle",
    "Fork/Join": "fork, join",
    "Internal Storage": "win-pane, internal-storage, window-pane",
    "Junction": "f-circ, filled-circle, junction",
    "Lined Document": "lin-doc, lined-document",
    "Lined/Shaded Process": "lin-rect, lined-rectangle, lined-proc, lin-proc, shaded-process",
    "Loop Limit (Notched Pentagon)": "notch-pent, loop-limit, notched-pentagon",
    "Manual File": "flip-tri, flipped-triangle, manual-file",
    "Manual Input": "sl-rect, manual-input, sloped-rectangle",
    "Manual Operation": "trap-t, inv-trapezoid, manual, trapezoid-top",
    "Multi-Document": "docs, documents, st-doc, stacked-document",
    "Multi-Process": "st-rect, processes, procs, stacked-rectangle",
    "Odd": "odd",
    "Paper Tape": "flag, paper-tape",
    "Prepare (Hexagon)": "hex, hexagon, prepare",
    "Priority Action": "trap-b, priority, trapezoid-bottom",
    "Process": "rect, proc, process, rectangle",
    "Start (Circle)": "circle, circ",
    "Start Small": "sm-circ, small-circle, start",
    "Stop (Double Circle)": "dbl-circ, double-circle",
    "Stop (Framed Circle)": "fr-circ, framed-circle, stop",
    "Stored Data": "bow-rect, bow-tie-rectangle, stored-data",
    "Subprocess": "fr-rect, framed-rectangle, subproc, subprocess, subroutine",
    "Summary": "cross-circ, crossed-circle, summary",
    "Tagged Document": "tag-doc, tagged-document",
    "Tagged Process": "tag-rect, tag-proc, tagged-process, tagged-rectangle",
    "Terminal (Stadium)": "stadium, terminal, pill",
    "Text Block": "text",
}


def get_shape(category: str) -> str:
    return shapes[category].split(VALUES_SEPARATOR)[0]


@functools.lru_cache
def _shape_docs(category):
    return [nlp(value.replace("-", " ")) for value in shapes[category].split(VALUES_SEPARATOR)]


def identify_shape(text: str) -> tuple[tuple[str, float], tuple[str, float]]:
    """Return top-2 matching Mermaid shapes for user text."""
    doc = nlp(text.lower())

    result: dict[str, float] = {
        shape: max(doc.similarity(syn_doc) for syn_doc in _shape_docs(shape)) for shape in shapes
    }

    values = list(result.items())
    values.sort(key=op.itemgetter(1), reverse=True)

    first, second, *_ = values
    return first, second


def summarize_to_phrase(sentence: str) -> str:
    """
    Cuts a long sentence into a small phrase using its grammer.
    """
    doc = nlp(sentence)

    root = [token for token in doc if token.head == token][0]  # root verb or main word

    # If root is a verb → verb + object
    if root.pos_ == "VERB":
        dobj = next((child for child in root.children if child.dep_ in ("dobj", "attr", "oprd")), None)
        if dobj:
            return f"{root.lemma_} {dobj.lemma_}"
        return root.lemma_

    # If root is a noun/adjective → pick compound/descriptor
    if root.pos_ in ("NOUN", "ADJ"):
        compound = next((child for child in root.children if child.dep_ == "compound"), None)
        if compound:
            return f"{compound.text} {root.text}"
        return root.text

    # fallback: top 2 content words
    content = [t.text for t in doc if t.pos_ in ("NOUN", "VERB", "ADJ")]
    return " ".join(content[:2])


if __name__ == "__main__":
    # test summarizing function
    while True:
        text = input()
        summary = summarize_to_phrase(text)
        print(summary)
