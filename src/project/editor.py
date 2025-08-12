from __future__ import annotations

from nicegui import ui, app
from html2text import html2text


async def index():
    await ui.context.client.connected()
    app.storage.tab.setdefault('editor.value', '')
    
    with ui.splitter().classes('size-full') as splitter:
        with splitter.before:
            editor = ui.editor().classes('size-full').bind_value(app.storage.tab, 'editor.value')
        with splitter.after:
            with ui.column():
                ui.label(editor.value).bind_text_from(editor, 'value')
                transformed = ui.label(editor.value).bind_text_from(editor, 'value', backward=html2text)
                ui.mermaid(editor.value).bind_content_from(transformed, 'text')