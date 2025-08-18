from __future__ import annotations

from nicegui import ui, app, ElementFilter

from project.interpreter import interpret, InterpretError
from project.widgets.emoji_keyboard import emoji_keyboard


DEBUG = False


# based on `ui.editor` and these examples https://quasar.dev/vue-components/editor
class CustomEditor(ui.editor, component="../components/extended_editor.vue"):
    def apply_styles(self):
        return self.classes("size-full flex flex-nowrap flex-col items-stretch").props('content-class="grow"')


# Custom mermaid element that uses a newer version rather than the fixed version
# provided by nicegui
class UpdatedMermaid(ui.mermaid, component="../components/updated_mermaid.js"):
    pass


async def index():
    await ui.context.client.connected(timeout=10.0)

    def insert_emoji(emoji):
        editor.run_method("insertTextAtCursor", emoji)

    def on_save(e):
        app.storage.user["editor.value"] = e.args
        ui.notify("Content is saved", type="positive")

    def backward(value: str):
        try:
            content = interpret(value)
            return content
        except InterpretError as e:
            error_message = e.args[0]
            ui.notify(error_message, type="negative")
            return ""

    with ui.splitter().classes("size-full") as splitter:
        # LEFT: CustomEditor
        with splitter.before:
            with ui.column(align_items="center").classes("size-full relative"):
                editor = (
                    CustomEditor(placeholder="You can type emojis here...")
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
        # RIGHT: UpdatedMermaid
        with splitter.after:
            with ui.column(align_items="center").classes("justify-center size-full"):
                if DEBUG:
                    ui.label().bind_text_from(editor, "value", backward=backward)
                UpdatedMermaid(editor.value).bind_content_from(editor, "value", backward=backward)
