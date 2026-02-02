"""Extract plain text from Atlassian Document Format (ADF) content."""

from typing import Any


def extract_text_from_adf(content: str | dict[str, Any]) -> str:
    """Extract plain text from ADF content.

    Args:
        content: ADF document dict or plain string

    Returns:
        Plain text representation of the content
    """
    if isinstance(content, str):
        return content

    if not isinstance(content, dict) or content.get("type") != "doc":
        return str(content)

    text_parts: list[str] = []

    for node in content.get("content", []):
        _extract_node(node, text_parts, indent=0)

    return "".join(text_parts).strip()


def _extract_node(node: dict[str, Any], text_parts: list[str], indent: int = 0) -> None:
    """Recursively extract text from an ADF node."""
    node_type = node.get("type", "")

    handler = _NODE_HANDLERS.get(node_type)
    if handler:
        handler(node, text_parts, indent)
    elif "content" in node:
        _handle_generic_content(node, text_parts, indent)


def _handle_text(
    node: dict[str, Any], text_parts: list[str], indent: int  # noqa: ARG001
) -> None:
    """Handle text node."""
    text_parts.append(node.get("text", ""))


def _handle_paragraph(node: dict[str, Any], text_parts: list[str], indent: int) -> None:
    """Handle paragraph node."""
    if text_parts and text_parts[-1] != "\n":
        text_parts.append("\n")
    for child in node.get("content", []):
        _extract_node(child, text_parts, indent)
    text_parts.append("\n")


def _handle_heading(node: dict[str, Any], text_parts: list[str], indent: int) -> None:
    """Handle heading node."""
    level = node.get("attrs", {}).get("level", 1)
    if text_parts and text_parts[-1] != "\n":
        text_parts.append("\n")
    text_parts.append("#" * level + " ")
    for child in node.get("content", []):
        _extract_node(child, text_parts, indent)
    text_parts.append("\n")


def _handle_bullet_list(
    node: dict[str, Any], text_parts: list[str], indent: int
) -> None:
    """Handle bullet list node."""
    for item in node.get("content", []):
        _handle_list_item(item, text_parts, indent, bullet="•")


def _handle_ordered_list(
    node: dict[str, Any], text_parts: list[str], indent: int
) -> None:
    """Handle ordered list node."""
    start = node.get("attrs", {}).get("order", 1)
    for i, item in enumerate(node.get("content", []), start):
        _handle_list_item(item, text_parts, indent, bullet=f"{i}.")


def _handle_list_item(
    item: dict[str, Any], text_parts: list[str], indent: int, bullet: str
) -> None:
    """Handle a single list item."""
    item_text: list[str] = []
    for child in item.get("content", []):
        for subchild in child.get("content", []):
            if subchild.get("type") == "text":
                item_text.append(subchild.get("text", ""))
    text_parts.append("  " * indent + f"{bullet} " + "".join(item_text))


def _handle_code_block(
    node: dict[str, Any], text_parts: list[str], indent: int
) -> None:
    """Handle code block node."""
    lang = node.get("attrs", {}).get("language", "")
    text_parts.append(f"\n```{lang}\n")
    for child in node.get("content", []):
        _extract_node(child, text_parts, indent)
    text_parts.append("\n```\n")


def _handle_panel(node: dict[str, Any], text_parts: list[str], indent: int) -> None:
    """Handle panel node."""
    panel_type = node.get("attrs", {}).get("panelType", "info").upper()
    text_parts.append(f"\n[{panel_type}]\n")
    for child in node.get("content", []):
        _extract_node(child, text_parts, indent)
    text_parts.append("\n")


def _handle_emoji(
    node: dict[str, Any], text_parts: list[str], indent: int  # noqa: ARG001
) -> None:
    """Handle emoji node."""
    attrs = node.get("attrs", {})
    text_parts.append(attrs.get("text", attrs.get("shortName", "")))


def _handle_generic_content(
    node: dict[str, Any], text_parts: list[str], indent: int
) -> None:
    """Handle nodes with generic content."""
    for child in node["content"]:
        _extract_node(child, text_parts, indent)


# Node type to handler mapping
_NODE_HANDLERS: dict[str, Any] = {
    "text": _handle_text,
    "paragraph": _handle_paragraph,
    "heading": _handle_heading,
    "bulletList": _handle_bullet_list,
    "orderedList": _handle_ordered_list,
    "codeBlock": _handle_code_block,
    "panel": _handle_panel,
    "emoji": _handle_emoji,
}
