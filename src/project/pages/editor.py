from __future__ import annotations

from nicegui import ElementFilter, app, ui

from project.interpreter import InterpretError, interpret
from project.widgets.emoji_keyboard import emoji_keyboard

# adds a label that displays mermaid code generated from user input
DEBUG = False


# based on `ui.editor` and these examples https://quasar.dev/vue-components/editor
class CustomEditor(ui.editor, component="../components/extended_editor.vue"):
    """Modified version of nicegui WYSIWYG editor with many buttons added to the toolbar."""

    def apply_styles(self) -> CustomEditor:
        """Apply styles to give the editor the desired appearance.

        Returns itself
        """
        return self.classes("size-full flex flex-nowrap flex-col items-stretch").props(
            'content-class="grow"',
        )


# nicegui mermaid object has a fixed version that is less than 11.3
# This particular version supports syntax like A@{ shape: rect, label: 'A' }
# This class defines a custom mermaid element that shares the same behaviour as the original
# but using a custom component that loads the required version from a cdn
class UpdatedMermaid(ui.mermaid, component="../components/updated_mermaid.js"):
    """Mermaid element that uses a newer version."""


async def index() -> None:
    """Root method for this page."""
    await ui.context.client.connected(timeout=10.0)
    app.storage.tab.setdefault("editor.value", app.storage.user.get("editor.value"))

    # used by emoji keyboard
    def insert(text) -> None:
        """Use javascript to insert text at the cursor/caret of the editor."""
        editor.run_method("insertTextAtCursor", text)

    def on_save(e) -> None:
        """Save the code to the user storage overriding any previous value."""
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
                keyboard = emoji_keyboard(on_click=insert).classes(
                    "h-2/5 absolute bottom-0 inset-x-0 border bg-white",
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
                UpdatedMermaid(editor.value).bind_content_from(
                    editor,
                    "value",
                    backward=backward,
                )
