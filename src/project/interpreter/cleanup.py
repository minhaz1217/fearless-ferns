from __future__ import annotations

from emoji import demojize
from html2text import html2text


def cleanup(content: str) -> str:
    """
    Converts emoji-containing html into markdown.
    """
    return html2text(demojize(content))
