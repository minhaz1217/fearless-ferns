from __future__ import annotations

import uuid

import _examples
import editor
import homepage
from nicegui import ui

# See https://nicegui.io/documentation/colors#custom_colors
ui.colors(
    primary="#5898d4",  # not applied
)


@ui.page("/")
@ui.page("/{_:path}")
def index() -> None:
    header_links = {
        "Home": "/",
        "Editor": "/editor",
    }
    ui.context.client.content.classes("p-0")

    with ui.header().props("elevated").classes("flex py-0 items-center justify-between"):
        with ui.row().classes("items-center gap-2"):
            ui.image("https://icon-library.com/images/python-icon-png/python-icon-png-2.jpg").classes("size-16")
            ui.label("Fearless Ferns").classes("text-3xl self-center font-semibold")

        with ui.row().classes("items-center gap-6"):
            for text, target in header_links.items():
                ui.link(text, target).classes(
                    "text-xl text-white font-medium no-underline duration-200 hover:text-sky-300",
                )

    # See https://nicegui.io/documentation/sub_pages
    ui.sub_pages(
        {
            "/": homepage.index,
            "/editor": editor.index,
            "/_widgets": _examples.index,
        }
    ).classes("h-[90vh] w-full")


ui.add_head_html(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    """
)

ui.add_css(
    """
    body {
        font-family: 'Roboto', sans-serif;
    }
    """
)

ui.run(
    # [Errno 13] error while attempting to bind on address ('0.0.0.0', 8080): [winerror 10013] an attempt was made to access a socket in a way forbidden by its access permissions
    port=8081,  # default is 8080
    # NOTE: On Windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
    # reload=platform.system() != "Windows",
    # required to enable `ui.storage.user`
    storage_secret=str(uuid.uuid4()),
)
