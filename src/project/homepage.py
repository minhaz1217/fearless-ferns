from __future__ import annotations

from nicegui import ui


def index():
    with ui.element().classes('size-full flex place-content-center'):
        with ui.card().classes('container flex items-center'):
            ui.label("Try our crazy chart editor").classes('text-h4 font-bold font-serif')
            with ui.link(target='/editor'):
                ui.button("Try it now!").props("rounded").classes('px-8 py-2')