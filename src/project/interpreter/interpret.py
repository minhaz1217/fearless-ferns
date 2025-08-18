from __future__ import annotations

import io

import emoji
import html2text

from project.models.Emojis import Emojis


class InterpretError(ValueError):
    """Raised when the code in the editor is malformed"""    


def interpret(content: str):
    flowchart_direction_emojis = [
        Emojis.top_to_bottom,
        Emojis.bottom_to_top,
        Emojis.left_to_right,
        Emojis.right_to_left,
    ]
    flowchart_edges = [Emojis.arrow, Emojis.thick_arrow, Emojis.dashed_arrow]

    def first_line_emoji_to_text(emote: str) -> str:
        """Convert first line's emoji to text.

        ⏩ this will convert into `flowchart LR`
        Args:
            emote (str): the emoji to convert

        Returns:
            str: returns mermaid text

        """
        match emote:
            case Emojis.top_to_bottom:
                return "flowchart TB"
            case Emojis.bottom_to_top:
                return "flowchart BT"
            case Emojis.left_to_right:
                return "flowchart LR"
            case Emojis.right_to_left:
                return "flowchart RL"
            case _:
                return "flowchart LR"

    def detect_edge_first_last_index(line: str) -> tuple[int, int]:
        """Detect first and last index of the edge emoji.

        Args:
            line (str): the line that has the edge indicator emoji

        Returns:
            tuple[int, int]: returns first_edge_index and last_edge_index

        """
        first_edge_index = -1
        last_edge_index = -1
        for index, char in enumerate(line):
            if flowchart_edges.__contains__(char):
                if first_edge_index == -1:
                    first_edge_index = index
                else:
                    last_edge_index = index
        return (first_edge_index, last_edge_index)

    def make_node(node: str) -> str:
        """Make a unique node if isn't already present.

        Args:
            node (str): the node text

        Returns:
            str: returns mermaid syntax for a node with emoji.

        """
        if emoji.is_emoji(node):
            # just a single emoji
            key = ""
            key = all_emoji.get(node) if node in all_emoji else emoji.demojize(node).strip(":")
            return f"{key}[{node}]"
        return ""

    def make_edge(edge_descriptor: str) -> str:
        """Make an edge for mermaid syntax.

        Args:
            edge_descriptor (str): The edge connector, can be single emoji or 2 emojis with text in between

        Returns:
            str: returns mermaid syntax for edge

        """
        output = ""
        if emoji.is_emoji(edge_descriptor):
            # single edge
            match edge_descriptor:
                case Emojis.arrow:
                    output = " --> "
                case Emojis.thick_arrow:
                    output = " ==> "
                case Emojis.dashed_arrow:
                    output = " -.-> "
        else:
            # labeled edge
            first_index, last_index = detect_edge_first_last_index(edge_descriptor)
            first_emoji = edge_descriptor[first_index : first_index + 1]
            last_emoji = edge_descriptor[last_index : last_index + 1]
            if emoji.is_emoji(first_emoji) and first_emoji == last_emoji:
                label = edge_descriptor[first_index + 1 : last_index].strip()
                match first_emoji:
                    case Emojis.arrow:
                        output = f" -- {label} --> "
                    case Emojis.thick_arrow:
                        output = f" == {label} ==> "
                    case Emojis.dashed_arrow:
                        output = f" -. {label} .-> "
        return output

    flow_chart = []
    lines = html2text.html2text(content).splitlines()
    error_message = ""
    all_emoji: dict[str, str] = dict()

    if len(lines) > 0:
        first_line = lines[0].strip()
        if not flowchart_direction_emojis.__contains__(first_line):
            error_message = (
                "First line should contain one of the following emojis to indicate the direction "
                + str.join(", ", flowchart_direction_emojis)
            )
            raise InterpretError(error_message)

        direction_string = first_line_emoji_to_text(first_line)
        if direction_string != "":
            flow_chart.append(direction_string)
        else:
            error_message = "Please follow the instruction for the first line"
            raise InterpretError(error_message)

        for line in lines[1:]:
            if not line:
                continue
            if not set(flowchart_edges) & set(line):
                error_message = (
                    "Every line except the first line should contain at least one connecting arrow "
                    + str.join(", ", flowchart_edges)
                )

            (first_edge_index, last_edge_index) = detect_edge_first_last_index(line)

            if last_edge_index == -1:
                # only one arrow
                left_half = line[:first_edge_index].strip()
                right_half = line[first_edge_index + 1 :].strip()
                flow_chart.append(
                    make_node(left_half)
                    + make_edge(line[first_edge_index : first_edge_index + 1].strip())
                    + make_node(right_half),
                )
            else:
                # arrow with label in middle
                left_half = line[:first_edge_index].strip()
                right_half = line[last_edge_index + 1 :].strip()
                flow_chart.append(
                    make_node(left_half)
                    + make_edge(line[first_edge_index : last_edge_index + 1].strip())
                    + make_node(right_half),
                )
    f = io.StringIO()
    if len(flow_chart) > 0:
        f.write(str.join("\n", flow_chart))

    f.seek(0)
    return f.read()


# basic
# ⏩
# 😀➡😃


# basic multi edge
# ⏬
# 😀➡😆
# 😀▶😭
# 😀〰😡

# basic with edge label

# basic multi edge
# ⏫
# 😀➡happy➡😆
# 😀▶sad▶😭
# 😀〰angry〰😡
