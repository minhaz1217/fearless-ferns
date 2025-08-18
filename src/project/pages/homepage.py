from __future__ import annotations

from nicegui import ui


def _index() -> None:
    """Disabled homepage."""
    with ui.element().classes("size-full flex place-content-center"), ui.card().classes("container flex items-center"):
        ui.label("Try our crazy chart editor").classes("text-h4 font-bold font-serif")
        with ui.link(target="/editor"):
            ui.button("Try it now!").props("rounded").classes("px-8 py-2")


def index() -> None:
    """Active code for homepage. Redirect user to editor page."""
    ui.navigate.to("/editor")
