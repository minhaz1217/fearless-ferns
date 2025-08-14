from __future__ import annotations

import operator as op

from nicegui import ui, app
from nicegui.events import Handler, ValueChangeEventArguments
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement
from html2text import html2text


# based on `ui.editor` and these examples https://quasar.dev/vue-components/editor
class CustomEditor(ValueElement, DisableableElement, component='editor.vue', default_classes='nicegui-editor'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False

    def __init__(self,
                 *,
                 placeholder: str | None = None,
                 value: str = '',
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        super().__init__(value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props['placeholder'] = placeholder

    def _handle_value_change(self, value) -> None:
        super()._handle_value_change(value)
        if self._send_update_on_value_change:
            self.run_method('updateValue')
    
    def apply_styles(self):
        return self.classes('size-full flex flex-col items-stretch').props('content-class="grow"')


async def index():
    await ui.context.client.connected(timeout=10.0)
    app.storage.tab.setdefault('editor.value', app.storage.user.get('editor.value', ''))
    
    with ui.splitter().classes('size-full') as splitter:
        with splitter.before:
            with ui.column(align_items='center').classes('size-full'):
                editor = CustomEditor().apply_styles().bind_value(app.storage.tab, 'editor.value')\
                    .on('save', lambda e: op.setitem(app.storage.user, 'editor.value', e.args) or ui.notify("Content is saved", type='positive'))
        with splitter.after:
            with ui.column(align_items='center').classes('justify-center size-full'):
                ui.mermaid(editor.value).bind_content_from(editor, 'value', backward=html2text)