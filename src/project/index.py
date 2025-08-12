from __future__ import annotations

import platform

from nicegui import ui

import _examples, home, editor


# See https://nicegui.io/documentation/colors#custom_colors
ui.colors(
    primary='#5898d4',  # not applied
)


@ui.page('/')
@ui.page('/{_:path}')
def index():
    header_links = {
        "homepage": '/',
        "editor": '/editor',
    }
    ui.context.client.content.classes('p-0')
    
    with ui.header().props('elevated').classes('py-0 items-center'):
        ui.image("https://icon-library.com/images/python-icon-png/python-icon-png-2.jpg").classes('size-16')
        ui.label("Fearless Ferns").classes('font-serif text-h3 self-center')
        ui.space()
        for text, target in header_links.items():
            ui.link(text, target).classes('text-h5 text-white font-bold no-underline hover:text-amber-600')

    # See https://nicegui.io/documentation/sub_pages
    ui.sub_pages({
        '/': home.index,
        '/editor': editor.index,
        '/_widgets': _examples.index,
    }).classes('h-[90vh] w-full')


ui.run(
    # [Errno 13] error while attempting to bind on address ('0.0.0.0', 8080): [winerror 10013] an attempt was made to access a socket in a way forbidden by its access permissions
    port=8081,  # default is 8080
    # NOTE: On Windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
    # reload=platform.system() != "Windows",
)