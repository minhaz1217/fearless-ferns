from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def cleanup(text: str) -> str:
    """Clean given text, escapes html characters, and replaces html entities like `&gt;`."""
    return text  # no implementation for now


def element(tagname: str) -> Callable[[str], str]:
    """Wrap stuff in html tag.

    USAGE: element("h1")("Hello world!")
    """
    return lambda text: f"<{tagname}>{cleanup(text)}</{tagname}>"


h1 = element("h1")


def helloworld() -> str:
    """Test method."""
    return h1("Hello World!")


if __name__ == "__main__":
    print(helloworld())
