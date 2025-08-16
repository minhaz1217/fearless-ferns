from nicegui import html, ui


def text_elements():
    ui.label("This is a label")

    ui.link("This is a link", "https://github.com/minhaz1217/fearless-ferns")

    ui.chat_message("this is a chat message")

    with ui.list().props("sparator dense") as ul:
        ui.item("item 1")
        ui.separator()
        ui.item("close")

    with ui.element("div").classes("p-2 bg-blue-100"):
        ui.label("inside a colored div")

    ui.markdown("This is **Markdown**.")

    ui.restructured_text("This is **reStructuredText**.")

    ui.mermaid("""
    graph LR;
        A --> B;
        A --> C;
    """)

    ui.html("This is <strong>HTML</strong>.")

    with html.section().style("font-size: 120%"):
        html.strong("This is bold.").classes("cursor-pointer").on("click", lambda: ui.notify("Bold!"))
        html.hr()
        html.em("This is italic.").tooltip("Nice!")
        with ui.row():
            html.img().props("src=https://placehold.co/60")
            html.img(src="https://placehold.co/60")


def controls():
    ui.button("Click me!", on_click=lambda: ui.notify("You clicked me!"))

    with ui.button_group().props("rounded"):
        ui.button("One")
        ui.button("Two")
        ui.button("Three")
    with ui.button_group().props("push glossy"):
        ui.button("One", color="red").props("push")
        ui.button("Two", color="orange").props("push text-color=black")
        ui.button("Three", color="yellow").props("push text-color=black")
    with ui.button_group().props("outline"):
        ui.button("One").props("outline")
        ui.button("Two").props("outline")
        ui.button("Three").props("outline")

    with ui.dropdown_button("Open me!", auto_close=True):
        ui.item("Item 1", on_click=lambda: ui.notify("You clicked item 1"))
        ui.item("Item 2", on_click=lambda: ui.notify("You clicked item 2"))

    with ui.fab("navigation", label="Transport"):
        ui.fab_action("train", on_click=lambda: ui.notify("Train"))
        ui.fab_action("sailing", on_click=lambda: ui.notify("Boat"))
        ui.fab_action("rocket", on_click=lambda: ui.notify("Rocket"))

    with ui.button("Click me!", on_click=lambda: badge.set_text(str(int(badge.text) + 1))):
        badge = ui.badge("0", color="red").props("floating")

    with ui.row().classes("gap-1"):
        ui.chip("Click me", icon="ads_click", on_click=lambda: ui.notify("Clicked"))
        ui.chip("Selectable", selectable=True, icon="bookmark", color="orange")
        ui.chip("Removable", removable=True, icon="label", color="indigo-3")
        ui.chip("Styled", icon="star", color="green").props("outline square")
        ui.chip("Disabled", icon="block", color="red").set_enabled(False)

    toggle1 = ui.toggle([1, 2, 3], value=1)
    toggle2 = ui.toggle({1: "A", 2: "B", 3: "C"}).bind_value(toggle1, "value")

    radio1 = ui.radio([1, 2, 3], value=1).props("inline")
    radio2 = ui.radio({1: "A", 2: "B", 3: "C"}).props("inline").bind_value(radio1, "value")

    select1 = ui.select([1, 2, 3], value=1)
    select2 = ui.select({1: "One", 2: "Two", 3: "Three"}).bind_value(select1, "value")

    ui.input_chips("My favorite chips", value=["Pringles", "Doritos", "Lay's"])

    checkbox = ui.checkbox("check me")
    ui.label("Check!").bind_visibility_from(checkbox, "value")

    switch = ui.switch("switch me")
    ui.label("Switch!").bind_visibility_from(switch, "value")

    slider = ui.slider(min=0, max=100, value=50)
    ui.label().bind_text_from(slider, "value")

    min_max_range = ui.range(min=0, max=100, value={"min": 20, "max": 80})
    ui.label().bind_text_from(min_max_range, "value", backward=lambda v: f"min: {v['min']}, max: {v['max']}")

    ui.rating(value=4)

    ui.joystick(
        color="blue",
        size=50,
        on_move=lambda e: coordinates.set_text(f"{e.x:.3f}, {e.y:.3f}"),
        on_end=lambda _: coordinates.set_text("0, 0"),
    ).classes("bg-slate-300")
    coordinates = ui.label("0, 0")

    ui.input(
        label="Text",
        placeholder="start typing",
        on_change=lambda e: result.set_text("you typed: " + e.value),
        validation={"Input too long": lambda value: len(value) < 20},
    )
    result = ui.label()

    ui.textarea(label="Text", placeholder="start typing", on_change=lambda e: result.set_text("you typed: " + e.value))
    result = ui.label()

    editor = ui.codemirror('print("Edit me!")', language="Python").classes("h-32")
    ui.select(editor.supported_languages, label="Language", clearable=True).classes("w-32").bind_value(
        editor,
        "language",
    )
    ui.select(editor.supported_themes, label="Theme").classes("w-32").bind_value(editor, "theme")

    ui.number(
        label="Number",
        value=3.1415927,
        format="%.2f",
        on_change=lambda e: result.set_text(f"you entered: {e.value}"),
    )
    result = ui.label()

    knob = ui.knob(0.3, show_value=True)

    with ui.knob(color="orange", track_color="grey-2").bind_value(knob, "value"):
        ui.icon("volume_up")

    label = ui.label("Change my color!")
    ui.color_input(label="Color", value="#000000", on_change=lambda e: label.style(f"color:{e.value}"))

    with ui.button(icon="colorize") as button:
        ui.color_picker(on_pick=lambda e: button.classes(f"!bg-[{e.color}]"))

    ui.date(value="2023-01-01", on_change=lambda e: result.set_text(e.value))
    result = ui.label()

    ui.time(value="12:00", on_change=lambda e: result.set_text(e.value))
    result = ui.label()

    ui.upload(on_upload=lambda e: ui.notify(f"Uploaded {e.name}")).classes("max-w-full")


def audiovisual():
    ui.image("https://picsum.photos/id/377/640/360")
    html.img(src="https://picsum.photos/id/377/640/360")


def index():
    with ui.row():
        with ui.column():
            text_elements()
        with ui.column():
            controls()
        with ui.column():
            audiovisual()
        with ui.column():
            ui.button("Copy to clipboard").on(
                "click",
                js_handler="""() => navigator.clipboard.writeText("Hello, NiceGUI!")""",
            )


if __name__ == "__main__":
    ui.run(
        # [Errno 13] error while attempting to bind on address ('0.0.0.0', 8080): [winerror 10013] an attempt was made to access a socket in a way forbidden by its access permissions
        port=8081,  # default to 8080
        # NOTE: On Windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
        # reload=platform.system() != "Windows",
    )
