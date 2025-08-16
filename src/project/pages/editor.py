from __future__ import annotations

from html2text import html2text
from nicegui import ui, app, ElementFilter
from nicegui.events import Handler, ValueChangeEventArguments
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement
from nicegui.events import Handler, ValueChangeEventArguments

from project.widgets.emoji_keyboard import emoji_keyboard


# based on `ui.editor` and these examples https://quasar.dev/vue-components/editor
class CustomEditor(ui.editor, component="../components/extended_editor.vue"):
    def apply_styles(self):
        return self.classes("size-full flex flex-nowrap flex-col items-stretch").props('content-class="grow"')


# ===============================
# Emoji to shape mapping
# ===============================
EMOJI_TO_SHAPE = {
    "🟢": lambda nid, label: f"{nid}(({label}))",  # Oval
    "🔴": lambda nid, label: f"{nid}(({label}))",  # Oval
    "⌨️": lambda nid, label: f"{nid}[/ {label} /]",  # Parallelogram
    "🛠": lambda nid, label: f"{nid}[{label}]",  # Rectangle
    "🔍": lambda nid, label: f"{nid}{{{label}}}",  # Diamond
    "✅": "YES",  # edge label
    "❌": "NO",  # edge label
}

EMOJI_TOOLTIPS = {
    "🟢": "Start • Oval",
    "🔴": "End • Oval",
    "⌨️": "Input • Parallelogram",
    "🛠": "Process • Rectangle",
    "🔍": "Decision • Diamond",
    "✅": "Yes branch",
    "❌": "No branch",
}


# ===============================
# State
# ===============================
emoji_chain: list[dict] = []  # Each item: {"emoji": str, "label": str, "size": int}

# ===============================
# Functions
# ===============================


def prompt_for_label_and_size(emoji: str):
    """Ask the user for label text and size before adding a shape."""
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Configure {emoji} Shape").classes("text-lg font-bold mb-2")

        label_input = ui.input(label="Text inside shape", value="")
        size_input = ui.number(label="Size (%)", value=100, min=50, max=200)

        with ui.row():
            ui.button(
                "OK",
                on_click=lambda: (add_emoji(emoji, label_input.value or emoji, size_input.value), dialog.close()),
            )
            ui.button("Cancel", on_click=dialog.close)

    dialog.open()


def add_emoji(emoji: str, label: str, size: int):
    emoji_chain.append({"emoji": emoji, "label": label, "size": size})
    update_diagram()


def clear_chain():
    emoji_chain.clear()
    update_diagram()


def update_diagram():
    mermaid_code = parse_emoji_chain(emoji_chain)
    diagram.content = mermaid_code  # send raw Mermaid code


def parse_emoji_chain(chain: list[dict]) -> str:
    mermaid_lines = ["flowchart LR"]  # Left-to-Right flow
    node_count = 0
    prev_node = None
    last_decision_node = None  # store last diamond node
    edge_label = None

    for item in chain:
        emoji = item["emoji"]

        # ✅ / ❌ mean: set edge label, next shape is branch target
        if emoji in ("✅", "❌"):
            edge_label = EMOJI_TO_SHAPE[emoji]
            continue

        if emoji not in EMOJI_TO_SHAPE:
            continue

        label = item["label"]
        size = item["size"]
        node_id = f"N{node_count}"
        node_def = EMOJI_TO_SHAPE[emoji](node_id, label)

        mermaid_lines.append(node_def)
        mermaid_lines.append(f"style {node_id} font-size:{size}%;")

        if edge_label:
            # Branch from the decision node if we have one
            source_node = last_decision_node if last_decision_node else prev_node
            mermaid_lines.append(f"{source_node} -->|{edge_label}| {node_id}")
            edge_label = None
        elif prev_node is not None:
            mermaid_lines.append(f"{prev_node} --> {node_id}")

        # Track decision nodes for branching
        if emoji == "🔍":
            last_decision_node = node_id
            prev_node = node_id
        else:
            prev_node = node_id

        node_count += 1

    return "\n".join(mermaid_lines)


# ===============================
# UI
# ===============================
async def index():
    # ui.label("Emoji Flowchart Editor").classes("text-h4 font-bold mb-4")
    await ui.context.client.connected(timeout=10.0)
    
    def insert_emoji(emoji, event):
        editor.run_method("insertTextAtCursor", emoji)

    def on_save(e):
        app.storage.user["editor.value"] = e.args
        ui.notify("Content is saved", type="positive")
    
    with ui.splitter().classes("size-full") as splitter:
        # LEFT: CustomEditor
        with splitter.before:
            with ui.column(align_items="center").classes("size-full relative"):
                editor = (
                    CustomEditor(placeholder="Type emojis here...")
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
        with splitter.after:
            with ui.column(align_items="center").classes("justify-center size-full"):
                global diagram
                diagram = ui.mermaid(editor.value).bind_content_from(editor, "value", backward=html2text)
            
            
            # editor = CustomEditor(placeholder="Type emojis here...").apply_styles()

    # with splitter.after:
    #     with ui.row():
    #         for emoji, tooltip in EMOJI_TOOLTIPS.items():
    #             if emoji in ("✅", "❌"):
    #                 with ui.button(emoji, on_click=lambda e=emoji: add_emoji(e, e, 100)).props("color=blue"):
    #                     ui.tooltip(tooltip)
    #             else:
    #                 with ui.button(emoji, on_click=lambda e=emoji: prompt_for_label_and_size(e)).props("color=blue"):
    #                     ui.tooltip(tooltip)

    #     ui.button("CLEAR", on_click=clear_chain).classes("mt-2").props("color=blue")

    #     global diagram
    #     diagram = ui.mermaid("")
    #     update_diagram()
