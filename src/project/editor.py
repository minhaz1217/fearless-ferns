from __future__ import annotations

import operator as op

from html2text import html2text
from nicegui import app, ui
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement


class CustomEditor(ui.editor, component="components/editor.vue"):
    """Custom editor."""

    def apply_styles(self):
        return self.classes("size-full flex flex-nowrap flex-col items-stretch").props('content-class="grow"')


async def index() -> None:
    """Index method."""
    await ui.context.client.connected(timeout=10.0)
    app.storage.tab.setdefault("editor.value", app.storage.user.get("editor.value", ""))

    with ui.splitter().classes("size-full") as splitter:
        with splitter.before:
            with ui.column().classes("items-center size-full"):
                editor = (
                    CustomEditor()
                    .apply_styles()
                    .bind_value(app.storage.tab, "editor.value")
                    .on(
                        "save",
                        lambda e: op.setitem(app.storage.user, "editor.value", e.args)
                        or ui.notify("Content is saved", type="positive"),
                    )
                )
        with splitter.after:
            with ui.column().classes("items-center size-full gap-8"):
                ui.label(editor.value).bind_text_from(editor, "value")
                transformed = ui.label(editor.value).bind_text_from(
                    editor,
                    "value",
                    backward=html2text,
                )
                ui.mermaid(editor.value).bind_content_from(transformed, "text")
