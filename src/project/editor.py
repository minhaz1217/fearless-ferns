from __future__ import annotations

from nicegui import ui, app, ElementFilter
from nicegui.events import Handler, ValueChangeEventArguments
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement
from html2text import html2text

from emoji_keyboard import emoji_keyboard


# based on `ui.editor` and these examples https://quasar.dev/vue-components/editor
class CustomEditor(ui.editor, component="components/extended_editor.vue"):
    def apply_styles(self):
        return self.classes("size-full flex flex-nowrap flex-col items-stretch").props('content-class="grow"')


async def index():
    await ui.context.client.connected(timeout=10.0)
    app.storage.tab.setdefault("editor.value", app.storage.user.get("editor.value", ""))

    def insert_emoji(emoji, event):
        editor.run_method("insertTextAtCursor", emoji)

    def on_save(e):
        app.storage.user["editor.value"] = e.args
        ui.notify("Content is saved", type="positive")

    with ui.splitter().classes("size-full") as splitter:
        with splitter.before:
            with ui.column(align_items="center").classes("size-full relative"):
                editor = (
                    CustomEditor()
                    .apply_styles()
                    .bind_value(app.storage.tab, "editor.value")
                    .on("save", on_save)
                    .on("toggle:keyboard", lambda e: keyboard.set_visibility(e.args))
                )
                keyboard = emoji_keyboard(on_click=insert_emoji).classes(
                    "h-2/5 absolute bottom-0 inset-x-0 border bg-white"
                )

                (
                    ElementFilter(marker="emoji-content")
                    .within(marker="emoji-keyboard")
                    .classes("overflow-y-scroll justify-start")
                    # These two lines hide the vertical scroll bar and prevent overscrolling
                    .style("scrollbar-width: none;")
                    .classes("[&::-webkit-scrollbar]:hidden overscroll-contain")
                )
        with splitter.after:
            with ui.column(align_items="center").classes("justify-center size-full"):
                ui.mermaid(editor.value).bind_content_from(editor, "value", backward=html2text)
