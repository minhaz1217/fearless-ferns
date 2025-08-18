from __future__ import annotations

from functools import partial
import random
from typing import Callable

from nicegui import ui
from nicegui.events import ClickEventArguments
import emoji


# Changed lists to string because they become ugly when formatted
emojies = {
    "😀": "😀 😃 😄 😁 😆 😅 😂 🤣 😊 😇 🙂 🙃 😉 😌 😍 🥰 😘 😗 😙 😚 😋 😜 🤪 😝 🤑 🤗 🤭 🤫 🤔 😐 😑 😶",
    "😢": "😏 😒 🙄 😬 😮‍💨 😔 😪 😴 😷 🤒 🤕 🤢 🤮 🥵 🥶 😵 🤯 😳 🥺 😢 😭 😤 😠 😡 🤬",
    "👍": "👍 👎 👊 ✊ 🤛 🤜 👏 🙌 👐 🤲 🤝 🙏 ✍️ 💪 🖖 🤘 👌 ✌️ 🤞 🫶",
    "❤️": "❤️ 🧡 💛 💚 💙 💜 🖤 🤍 🤎 💔 ❣️ 💕 💞 💓 💗 💖 💘 💝",
    "🐶": "🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵",
    "🍕": "🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🫐 🍒 🥝 🍅 🥥 🥑 🍍 🍔 🍟 🍕 🌭 🥪 🌮 🌯 🥗",
}

EMOJI_DEFAULT = "😀"


def emoji_keyboard(
    *,
    on_click: Callable[[str]] | None = None,
    visible=True,
):
    with ui.row(wrap=False) as container:
        with ui.tabs().props("vertical").classes("h-full") as tabs:
            inner_tabs = {emo: ui.tab(emo) for emo in emojies}

        value = random.choice(list(inner_tabs))
        with ui.tab_panels(tabs, value=value).props("vertical").classes("h-full grow"):
            for key, tab in inner_tabs.items():
                with ui.tab_panel(tab), ui.row().mark("emoji-content"):
                    for emo in emojies[key].split():
                        handler = partial(on_click, emo) if on_click is not None else None
                        with ui.button(emo, on_click=handler).props("outline rounded color=black"):
                            ui.tooltip(emoji.demojize(emo))

    container.set_visibility(visible)
    return container.mark("emoji-keyboard")
