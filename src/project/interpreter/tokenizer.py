from __future__ import annotations

import re
from typing import Generator

from .models import Token


def group(pat: str, *, name="", capture=False) -> str:
    if name:
        return f"(?P<{name}>{pat})"
    elif capture:
        return f"({pat})"
    else:
        return f"(?:{pat})"


def optional(pat: str) -> str:
    return group(pat) + "?"


def many(pat: str) -> str:
    return group(pat) + "*"


def construct_pattern(patterns: dict[str, str]) -> re.Pattern:
    pattern = group("|".join(group(val, name=key) for key, val in patterns.items()))
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


pattern = construct_pattern(patterns)


def tokenize(content: str) -> Generator[Token, None, None]:
    for match in pattern.finditer(content):
        key, value = match.lastgroup, match.group()
        yield Token(value, str(key))
