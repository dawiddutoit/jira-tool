"""ADF document builder for Jira Epics."""

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


class EpicBuilder(DocumentBuilder):
    """Builder for creating Epic documents with standardized layout.

    Epics are large bodies of work that can be broken down into smaller
    issues (stories, tasks, bugs). This builder provides a structured
    format for Epic descriptions.

    Example:
        epic = (
            EpicBuilder("User Authentication", "P1", dependencies="Auth0 SDK")
            .add_problem_statement("Users cannot securely log in")
            .add_description("Implement OAuth2 authentication flow")
            .add_technical_details(["Integrate Auth0", "Add JWT validation"])
            .add_acceptance_criteria(["User can log in", "Session persists"])
            .build()
        )
    """

    def __init__(
        self,
        title: str,
        priority: str,
        dependencies: str | None = None,
        services: str | None = None,
    ) -> None:
        """Initialize Epic builder with required fields.

        Args:
            title: Epic title (without emoji, added automatically)
            priority: Priority level (e.g., P0, P1, P2)
            dependencies: External dependencies for this epic
            services: Affected services/systems
        """
        super().__init__()
        self.title = title
        self.priority = priority
        self.dependencies = dependencies or "None"
        self.services = services or "TBD"
        self._build_header()

    def _build_header(self) -> "EpicBuilder":
        """Build the standard epic header with priority panel."""
        self._content.append(Heading(f"🚀 {self.title}", level=1))

        priority_content = Paragraph(
            Text("⚠️ Priority: ", marks=[Strong()]),
            Text(self.priority),
            Text(" | "),
            Text("🔗 Dependencies: ", marks=[Strong()]),
            Text(self.dependencies),
            Text(" | "),
            Text("⚙️ Services: ", marks=[Strong()]),
            Text(self.services),
        )
        self._content.append(Panel(priority_content, panel_type="warning"))
        return self

    def add_problem_statement(self, problem: str) -> "EpicBuilder":
        """Add problem statement section."""
        self._content.append(Heading("⚠️ Problem Statement", level=2))
        self._content.append(Panel(Paragraph(problem), panel_type="note"))
        return self

    def add_description(self, description: str) -> "EpicBuilder":
        """Add description section."""
        self._content.append(Heading("📋 Description", level=2))
        self._content.append(Paragraph(description))
        return self

    def add_technical_details(
        self,
        requirements: list[str],
        code_example: str | None = None,
        code_language: str = "python",
    ) -> "EpicBuilder":
        """Add technical details section with requirements list."""
        self._content.append(Heading("🔧 Technical Details", level=2))

        self._content.append(
            Panel(
                Paragraph(Text("Implementation Requirements:", marks=[Strong()])),
                BulletList(*requirements),
                panel_type="info",
            )
        )

        if code_example:
            self._content.append(CodeBlock(code_example, code_language))

        return self

    def add_acceptance_criteria(self, criteria: list[str]) -> "EpicBuilder":
        """Add acceptance criteria section."""
        self._content.append(Heading("✅ Acceptance Criteria", level=2))
        self._content.append(Panel(OrderedList(*criteria), panel_type="success"))
        return self

    def add_edge_cases(self, edge_cases: list[str]) -> "EpicBuilder":
        """Add edge cases section."""
        self._content.append(Heading("⚡ Edge Cases", level=2))
        self._content.append(Panel(BulletList(*edge_cases), panel_type="note"))
        return self

    def add_testing_considerations(self, test_cases: list[str]) -> "EpicBuilder":
        """Add testing considerations section."""
        self._content.append(Heading("🧪 Testing Considerations", level=2))
        self._content.append(Panel(OrderedList(*test_cases), panel_type="info"))
        return self

    def add_out_of_scope(self, items: list[str]) -> "EpicBuilder":
        """Add out-of-scope section to clarify boundaries."""
        self._content.append(Heading("🚫 Out of Scope", level=2))
        self._content.append(Panel(BulletList(*items), panel_type="error"))
        return self

    def add_success_metrics(self, metrics: list[str]) -> "EpicBuilder":
        """Add success metrics section."""
        self._content.append(Heading("📊 Success Metrics", level=2))
        self._content.append(Panel(BulletList(*metrics), panel_type="info"))
        return self
