from __future__ import annotations

from functools import partial

from typing import Callable

from nicegui import ui
from nicegui.events import ClickEventArguments, Handler
import emoji


def enumerate_emojies():
    # return first 100 values
    return zip(range(100), emoji.EMOJI_DATA)


def emoji_keyboard(
    *,
    on_click: Callable[[str, ClickEventArguments]] | None = None,
    visible=False,
):
    with ui.row() as container:
        for i, emo in enumerate_emojies():
            handler = partial(on_click, emo) if on_click is not None else lambda: None
            ui.button(emo, on_click=handler).props("outline rounded color=black")

    container.set_visibility(visible)
    return container
