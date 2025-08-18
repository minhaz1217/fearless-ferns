from __future__ import annotations


def cleanup(text):
    """A function that cleans given text, escapes html characters, and replaces html entities like `&gt;`."""
    return text  # no implementation for now


def element(tagname):
    """A simple helper function for wrapping stuff in html tag.

    USAGE: element("h1")("Hello world!")
    """
    return lambda text: f"<{tagname}>{cleanup(text)}</{tagname}>"


h1 = element("h1")


def helloworld():
    return h1("Hello World!")


if __name__ == "__main__":
    print(helloworld())
