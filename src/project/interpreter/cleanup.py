from __future__ import annotations

from emoji import demojize
from html2text import html2text


def cleanup(content: str) -> str:
    """Converts emoji-containing html into markdown.
    """
    return html2text(demojize(content))


def clean_emoji(emo: str, *, replace_underscores=False) -> str:
    result = emo.replace(" ", "").replace(":", "")

    if replace_underscores:
        result = result.replace("_", " ")

    return result
