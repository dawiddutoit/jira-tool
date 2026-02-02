"""ADF document builder for Jira Subtasks."""

from jira_tool.document.builders.base import DocumentBuilder
from jira_tool.document.nodes.block import (
    BulletList,
    CodeBlock,
    Heading,
    OrderedList,
    Panel,
    Paragraph,
)
from jira_tool.document.nodes.inline import Text
from jira_tool.document.nodes.marks import Strong


class SubtaskBuilder(DocumentBuilder):
    """Builder for creating Subtask documents with streamlined layout.

    Subtasks are small, concrete pieces of work that are part of a parent
    issue. They have a simpler, more focused structure than full issues.

    Example:
        subtask = (
            SubtaskBuilder("Validate email format", parent_key="PROJ-456")
            .add_description("Add email validation using regex")
            .add_steps(["Add validation function", "Write unit tests"])
            .add_done_criteria(["All tests pass", "Code reviewed"])
            .build()
        )
    """

    def __init__(
        self,
        title: str,
        parent_key: str | None = None,
        estimated_hours: float | None = None,
    ) -> None:
        """Initialize Subtask builder with required fields.

        Args:
            title: Subtask title (without emoji, added automatically)
            parent_key: Parent issue key (e.g., "PROJ-456")
            estimated_hours: Estimated time in hours
        """
        super().__init__()
        self.title = title
        self.parent_key = parent_key or "None"
        self.estimated_hours = estimated_hours
        self._build_header()

    def _build_header(self) -> "SubtaskBuilder":
        """Build the subtask header with parent link."""
        self._content.append(Heading(f"📌 {self.title}", level=1))

        info_parts = [
            Text("🔗 Parent: ", marks=[Strong()]),
            Text(str(self.parent_key)),
        ]

        if self.estimated_hours is not None:
            info_parts.extend([
                Text(" | "),
                Text("⏱️ Estimate: ", marks=[Strong()]),
                Text(f"{self.estimated_hours}h"),
            ])

        self._content.append(Panel(Paragraph(*info_parts), panel_type="info"))
        return self

    def add_description(self, description: str) -> "SubtaskBuilder":
        """Add a brief description."""
        self._content.append(Paragraph(description))
        return self

    def add_steps(self, steps: list[str]) -> "SubtaskBuilder":
        """Add implementation steps as an ordered list."""
        self._content.append(Heading("📝 Steps", level=2))
        self._content.append(OrderedList(*steps))
        return self

    def add_done_criteria(self, criteria: list[str]) -> "SubtaskBuilder":
        """Add definition of done criteria."""
        self._content.append(Heading("✅ Done When", level=2))
        self._content.append(Panel(BulletList(*criteria), panel_type="success"))
        return self

    def add_notes(self, notes: list[str]) -> "SubtaskBuilder":
        """Add technical notes."""
        self._content.append(Heading("📝 Notes", level=2))
        self._content.append(BulletList(*notes))
        return self

    def add_code_snippet(self, code: str, language: str = "python") -> "SubtaskBuilder":
        """Add a code snippet for reference."""
        self._content.append(CodeBlock(code, language))
        return self

    def add_blockers(self, blockers: list[str]) -> "SubtaskBuilder":
        """Add blockers or dependencies."""
        self._content.append(Heading("🚧 Blockers", level=2))
        self._content.append(Panel(BulletList(*blockers), panel_type="warning"))
        return self
