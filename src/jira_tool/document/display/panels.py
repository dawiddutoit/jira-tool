"""Rich Panel builders for displaying Jira issues."""

from typing import Any, Self

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from jira_tool.document.adf import extract_text_from_adf
from jira_tool.document.display.formatters import (
    format_date,
    format_date_relative,
    get_priority,
    get_user_display,
)

console = Console()


class IssuePanelBuilder:
    """Builder for creating Rich Panels displaying Jira issue details."""

    def __init__(self, issue: dict[str, Any]) -> None:
        """Initialize with issue data."""
        self._issue = issue
        self._fields = issue.get("fields", {})
        self._lines: list[str] = []

    def add_key(self) -> Self:
        """Add issue key line."""
        self._lines.append(f"[bold]Issue:[/bold] {self._issue.get('key', 'N/A')}")
        return self

    def add_summary(self) -> Self:
        """Add summary line."""
        summary = self._fields.get("summary", "No summary")
        self._lines.append(f"[bold]Summary:[/bold] {summary}")
        return self

    def add_status(self) -> Self:
        """Add status line."""
        status = self._fields.get("status", {}).get("name", "Unknown")
        self._lines.append(f"[bold]Status:[/bold] {status}")
        return self

    def add_priority(self) -> Self:
        """Add priority line."""
        priority = get_priority(self._fields)
        self._lines.append(f"[bold]Priority:[/bold] {priority}")
        return self

    def add_type(self) -> Self:
        """Add issue type line."""
        issue_type = self._fields.get("issuetype", {}).get("name", "Unknown")
        self._lines.append(f"[bold]Type:[/bold] {issue_type}")
        return self

    def add_assignee(self) -> Self:
        """Add assignee line."""
        assignee = get_user_display(self._fields.get("assignee"))
        self._lines.append(f"[bold]Assignee:[/bold] {assignee}")
        return self

    def add_reporter(self) -> Self:
        """Add reporter line."""
        reporter = get_user_display(self._fields.get("reporter"))
        self._lines.append(f"[bold]Reporter:[/bold] {reporter}")
        return self

    def add_created(self) -> Self:
        """Add created date line."""
        created = format_date(self._fields.get("created"))
        self._lines.append(f"[bold]Created:[/bold] {created}")
        return self

    def add_updated(self) -> Self:
        """Add updated date line."""
        updated = format_date(self._fields.get("updated"))
        self._lines.append(f"[bold]Updated:[/bold] {updated}")
        return self

    def add_components(self) -> Self:
        """Add components line if present."""
        components = self._fields.get("components", [])
        if components:
            names = ", ".join([c["name"] for c in components])
            self._lines.append(f"[bold]Components:[/bold] {names}")
        return self

    def add_labels(self) -> Self:
        """Add labels line if present."""
        labels = self._fields.get("labels", [])
        if labels:
            self._lines.append(f"[bold]Labels:[/bold] {', '.join(labels)}")
        return self

    def add_epic_link(self) -> Self:
        """Add epic link line if present."""
        for field_key, field_value in self._fields.items():
            if (
                field_key.startswith("customfield_")
                and isinstance(field_value, str)
                and field_value.upper().startswith("EPIC-")
            ):
                self._lines.append(f"[bold]Epic:[/bold] {field_value}")
                break
        return self

    def add_parent(self) -> Self:
        """Add parent issue link if present."""
        parent = self._fields.get("parent", {})
        if parent:
            self._lines.append(f"[bold]Parent:[/bold] {parent.get('key', 'Unknown')}")
        return self

    def add_epic_name(self) -> Self:
        """Add epic name if this is an epic."""
        epic_name = self._fields.get("customfield_10011")  # Epic Name field
        if epic_name:
            self._lines.append(f"[bold]Epic Name:[/bold] {epic_name}")
        return self

    def add_all_standard(self) -> Self:
        """Add all standard issue fields."""
        return (
            self.add_key()
            .add_summary()
            .add_status()
            .add_priority()
            .add_type()
            .add_assignee()
            .add_reporter()
            .add_created()
            .add_updated()
            .add_components()
            .add_labels()
            .add_epic_link()
        )

    def build(self) -> Panel:
        """Build the Rich Panel."""
        key = self._issue.get("key", "Issue")
        return Panel("\n".join(self._lines), title=f"Jira Issue: {key}", expand=False)

    def build_lines(self) -> list[str]:
        """Return the built lines without wrapping in Panel."""
        return self._lines.copy()

    @classmethod
    def default(cls, issue: dict[str, Any]) -> Panel:
        """Build panel with all standard fields."""
        return cls(issue).add_all_standard().build()


class IssueHeaderBuilder:
    """Builder for creating Rich Table header for single issue display."""

    def __init__(self, issue: dict[str, Any]) -> None:
        """Initialize with issue data."""
        self._issue = issue
        self._fields = issue.get("fields", {})
        self._table = Table(show_header=False, box=None, padding=(0, 1))
        self._table.add_column(style="bold cyan")
        self._table.add_column()

    def add_key(self) -> Self:
        """Add issue key row."""
        self._table.add_row("Key:", self._issue.get("key", "N/A"))
        return self

    def add_type(self) -> Self:
        """Add issue type row."""
        self._table.add_row(
            "Type:", self._fields.get("issuetype", {}).get("name", "Unknown")
        )
        return self

    def add_status(self) -> Self:
        """Add status row."""
        self._table.add_row(
            "Status:", self._fields.get("status", {}).get("name", "Unknown")
        )
        return self

    def add_priority(self) -> Self:
        """Add priority row."""
        self._table.add_row(
            "Priority:", self._fields.get("priority", {}).get("name", "None")
        )
        return self

    def add_reporter(self) -> Self:
        """Add reporter row if present."""
        reporter = self._fields.get("reporter", {})
        if reporter:
            self._table.add_row("Reporter:", reporter.get("displayName", "Unknown"))
        return self

    def add_assignee(self) -> Self:
        """Add assignee row."""
        assignee = self._fields.get("assignee", {})
        if assignee:
            self._table.add_row("Assignee:", assignee.get("displayName", "Unassigned"))
        else:
            self._table.add_row("Assignee:", "Unassigned")
        return self

    def add_created(self) -> Self:
        """Add created date row if present."""
        created = self._fields.get("created")
        if created:
            self._table.add_row("Created:", format_date_relative(created))
        return self

    def add_updated(self) -> Self:
        """Add updated date row if present."""
        updated = self._fields.get("updated")
        if updated:
            self._table.add_row("Updated:", format_date_relative(updated))
        return self

    def add_all_standard(self) -> Self:
        """Add all standard header fields."""
        return (
            self.add_key()
            .add_type()
            .add_status()
            .add_priority()
            .add_reporter()
            .add_assignee()
            .add_created()
            .add_updated()
        )

    def build(self) -> Table:
        """Build the Rich Table."""
        return self._table

    def build_panel(self) -> Panel:
        """Build table wrapped in Panel with summary as title."""
        summary = self._fields.get("summary", "No Summary")
        return Panel(self._table, title=f"[bold]{summary}[/bold]")

    @classmethod
    def default(cls, issue: dict[str, Any]) -> Panel:
        """Build header panel with all standard fields."""
        return cls(issue).add_all_standard().build_panel()


def format_issue(issue: dict[str, Any]) -> None:
    """Format and display a single Jira issue with rich formatting."""
    if not issue or "fields" not in issue:
        console.print("[red]Invalid issue data received[/red]")
        return

    fields = issue.get("fields", {})

    # Display header panel
    console.print(IssueHeaderBuilder.default(issue))

    # Display description if available
    description = fields.get("description")
    if description:
        console.print("\n[bold]Description:[/bold]")
        if isinstance(description, dict) and description.get("type") == "doc":
            formatted_text = extract_text_from_adf(description)
            console.print(formatted_text if formatted_text else "(No description content)")
        elif isinstance(description, str):
            console.print(description)

    # Display labels
    labels = fields.get("labels", [])
    if labels:
        console.print(f"\n[bold]Labels:[/bold] {', '.join(labels)}")

    # Display epic details if it's an epic
    epic_name = fields.get("customfield_10011")  # Epic Name field
    if epic_name:
        console.print(f"\n[bold]Epic Name:[/bold] {epic_name}")

    # Display parent/epic link
    parent = fields.get("parent", {})
    if parent:
        console.print(f"\n[bold]Parent:[/bold] {parent.get('key', 'Unknown')}")

    epic_link = fields.get("customfield_10014")  # Epic Link field
    if epic_link:
        console.print(f"\n[bold]Epic Link:[/bold] {epic_link}")
