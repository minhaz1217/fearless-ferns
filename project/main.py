import platform

from nicegui import ui


def on_click_generate_diagram(mermaid_text: str) -> None:
    """Generate the diagram and set it for mermaid ui.

    Args:
        mermaid_text (str): the diagram text to be rendered

    """
    mermaid_ui.set_content(mermaid_text)


text_area = ui.textarea(
    label="Enter Something",
    placeholder="Type some code",
    value="""
graph LR;
    A--> B & C & D
    B--> A & E
    C--> A & E
    D--> A & E
    E--> B & C & D
""",
)

ui.button(
    "Generate Diagram",
    on_click=lambda: on_click_generate_diagram(text_area.value),
).props(
    "no-caps",
)

mermaid_ui = ui.mermaid(content="")


# NOTE: On Windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
ui.run(reload=platform.system() != "Windows")
