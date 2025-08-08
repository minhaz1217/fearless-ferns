from __future__ import annotations

import html
import pyhtml


def cleanup(text):
    """
    A function that cleans given text and escapes html characters
    """
    return html.escape(text)


def element(tagname):
    """
    A simple helper function for wrapping stuff in html tag

    USAGE: element("h1")("Hello world!")
    """
    return lambda text: "<{0}>{1}</{0}>".format(tagname, cleanup(text))


h1 = element("h1")


def helloworld():
    return h1("Hello World!")


if __name__ == "__main__":
    print(helloworld())
