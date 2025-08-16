from __future__ import annotations

import operator as op

from nicegui import ui, app
from nicegui.events import Handler, ValueChangeEventArguments
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement
from html2text import html2text

from emoji_keyboard import emoji_keyboard


# based on `ui.editor` and these examples https://quasar.dev/vue-components/editor
class CustomEditor(
    ValueElement, DisableableElement, component="components/extended_editor.vue", default_classes="nicegui-editor"
):
    VALUE_PROP: str = "value"
    LOOPBACK = False

    def __init__(
        self,
        *,
        placeholder: str | None = None,
        value: str = "",
        on_change: Handler[ValueChangeEventArguments] | None = None,
    ) -> None:
        """Editor

        A WYSIWYG editor based on `Quasar's QEditor <https://quasar.dev/vue-components/editor>`_.
        The value is a string containing the formatted text as HTML code.

        :param value: initial value
        :param on_change: callback to be invoked when the value changes
        """
        super().__init__(value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props["placeholder"] = placeholder

    def _handle_value_change(self, value) -> None:
        super()._handle_value_change(value)
        if self._send_update_on_value_change:
            self.run_method("updateValue")

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
                    "h-2/5 overflow-y-scroll p-4 absolute bottom-0 inset-x-0 border justify-between bg-white"
                # This line hides the vertical scroll bar and prevents overscrolling
                ).style('scrollbar-width: none;').classes('[&::-webkit-scrollbar]:hidden overscroll-contain')
        with splitter.after:
            with ui.column(align_items="center").classes("justify-center size-full"):
                ui.mermaid(editor.value).bind_content_from(editor, "value", backward=html2text)
