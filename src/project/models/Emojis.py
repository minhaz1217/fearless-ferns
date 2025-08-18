from enum import Enum


class Emojis(str, Enum):
    """List of all emojis that are fixed."""

    arrow = "➡"
    thick_arrow = "▶"
    dashed_arrow = "〰"
    top_to_bottom = "⏬"
    bottom_to_top = "⏫"
    left_to_right = "⏩"
    right_to_left = "⏪"
