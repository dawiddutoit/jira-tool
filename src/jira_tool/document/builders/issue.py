"""ADF document builder for Jira Issues (Tasks/Stories)."""

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


class IssueBuilder(DocumentBuilder):
    """Builder for creating Issue/Task documents with standardized layout.

    Issues represent concrete work items that can be completed in a sprint.
    This builder provides a structured format for Task and Story descriptions.

    Example:
        issue = (
            IssueBuilder("Add login form", "Frontend", story_points=3)
            .add_description("Create a responsive login form component")
            .add_implementation_details(["Use React Hook Form", "Add validation"])
            .add_acceptance_criteria(["Form validates email", "Shows errors"])
            .build()
        )
    """

    def __init__(
        self,
        title: str,
        component: str,
        story_points: int | None = None,
        epic_key: str | None = None,
    ) -> None:
        """Initialize Issue builder with required fields.

        Args:
            title: Issue title (without emoji, added automatically)
            component: Component this issue belongs to
            story_points: Estimated story points
            epic_key: Parent epic key (e.g., "PROJ-123")
        """
        super().__init__()
        self.title = title
        self.component = component
        self.story_points = story_points or "TBD"
        self.epic_key = epic_key or "None"
        self._build_header()

    def _build_header(self) -> "IssueBuilder":
        """Build the standard issue header with info panel."""
        self._content.append(Heading(f"📋 {self.title}", level=1))

        info_content = Paragraph(
            Text("⚙️ Component: ", marks=[Strong()]),
            Text(self.component),
            Text(" | "),
            Text("📊 Story Points: ", marks=[Strong()]),
            Text(str(self.story_points)),
            Text(" | "),
            Text("🔗 Epic: ", marks=[Strong()]),
            Text(str(self.epic_key)),
        )
        self._content.append(Panel(info_content, panel_type="info"))
        return self

    def add_description(self, description: str) -> "IssueBuilder":
        """Add description section in a note panel."""
        self._content.append(Heading("📋 Description", level=2))
        self._content.append(Panel(Paragraph(description), panel_type="note"))
        return self

    def add_implementation_details(self, details: list[str]) -> "IssueBuilder":
        """Add implementation details section in an info panel."""
        self._content.append(Heading("🔧 Implementation Details", level=2))
        self._content.append(Panel(BulletList(*details), panel_type="info"))
        return self

    def add_acceptance_criteria(self, criteria: list[str]) -> "IssueBuilder":
        """Add acceptance criteria section in a success panel."""
        self._content.append(Heading("✅ Acceptance Criteria", level=2))
        self._content.append(Panel(OrderedList(*criteria), panel_type="success"))
        return self

    def add_technical_notes(self, notes: list[str]) -> "IssueBuilder":
        """Add technical notes section."""
        self._content.append(Heading("📝 Technical Notes", level=2))
        self._content.append(Panel(BulletList(*notes), panel_type="note"))
        return self

    def add_code_example(
        self, code: str, language: str = "python", title: str | None = None
    ) -> "IssueBuilder":
        """Add a code example with optional title."""
        if title:
            self._content.append(Heading(f"💻 {title}", level=3))
        self._content.append(CodeBlock(code, language))
        return self

    def add_dependencies(self, dependencies: list[str]) -> "IssueBuilder":
        """Add dependencies section (blocked by or blocks)."""
        self._content.append(Heading("🔗 Dependencies", level=2))
        self._content.append(Panel(BulletList(*dependencies), panel_type="warning"))
        return self

    def add_testing_notes(self, notes: list[str]) -> "IssueBuilder":
        """Add testing notes section."""
        self._content.append(Heading("🧪 Testing Notes", level=2))
        self._content.append(Panel(BulletList(*notes), panel_type="info"))
        return self
