from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .models import Token

if TYPE_CHECKING:
    from collections.abc import Generator


def _group(pat: str, *, name: str = "", capture: bool = False) -> str:
    if name:
        return f"(?P<{name}>{pat})"
    if capture:
        return f"({pat})"
    return f"(?:{pat})"


def _optional(pat: str) -> str:
    return _group(pat) + "?"


def _many(pat: str) -> str:
    return _group(pat) + "*"


def _construct_pattern(patterns: dict[str, str]) -> re.Pattern:
    pattern = _group("|".join(_group(val, name=key) for key, val in patterns.items()))
    return re.compile(pattern)


patterns = {
    "W": r"[a-zA-Z][_a-zA-Z0-9]*[a-zA-Z0-9]|[a-zA-Z][a-zA-Z0-9]?",
    "E": ":.+?:",
    "B": r"\b\*\*|\*\*\b",
    "I": r"\b_|_\b",
    "S": r"\b\~\~|\~\~\b",
    "L": r"\[.*?\]\(.*?\)",
    "N": r"\d[\d\.]*",
    "U": r"\s*|.",
}


pattern = _construct_pattern(patterns)


def tokenize(content: str) -> Generator[Token, None, None]:
    """Generate tokens from given content.

    Args:
        content (str): user input

    Yields:
        Generator[Token, None, None]: tokens released by the tokenizer

    """
    for match in pattern.finditer(content):
        key, value = match.lastgroup, match.group()
        yield Token(value, str(key))
