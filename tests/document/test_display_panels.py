"""Tests for display panel builders."""

from unittest.mock import patch

import pytest
from rich.panel import Panel

from jira_tool.document.display.panels import (
    IssueHeaderBuilder,
    IssuePanelBuilder,
    format_issue,
)


@pytest.fixture
def sample_issue() -> dict:
    """Sample Jira issue for testing."""
    return {
        "key": "TEST-123",
        "fields": {
            "summary": "Test issue summary",
            "status": {"name": "Open"},
            "priority": {"name": "High"},
            "issuetype": {"name": "Task"},
            "assignee": {"displayName": "John Doe"},
            "reporter": {"displayName": "Jane Smith"},
            "created": "2024-01-15T10:00:00Z",
            "updated": "2024-01-16T14:30:00Z",
            "components": [{"name": "API"}, {"name": "Backend"}],
            "labels": ["urgent", "bug"],
        },
    }


@pytest.fixture
def minimal_issue() -> dict:
    """Minimal issue with only required fields."""
    return {
        "key": "MIN-1",
        "fields": {
            "summary": "Minimal issue",
            "status": {"name": "Open"},
        },
    }


class TestIssuePanelBuilder:
    """Tests for IssuePanelBuilder class."""

    def test_add_key(self, sample_issue: dict) -> None:
        """add_key adds issue key to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_key().build_lines()
        assert any("TEST-123" in line for line in lines)

    def test_add_summary(self, sample_issue: dict) -> None:
        """add_summary adds summary to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_summary().build_lines()
        assert any("Test issue summary" in line for line in lines)

    def test_add_status(self, sample_issue: dict) -> None:
        """add_status adds status to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_status().build_lines()
        assert any("Open" in line for line in lines)

    def test_add_priority(self, sample_issue: dict) -> None:
        """add_priority adds priority to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_priority().build_lines()
        assert any("High" in line for line in lines)

    def test_add_type(self, sample_issue: dict) -> None:
        """add_type adds issue type to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_type().build_lines()
        assert any("Task" in line for line in lines)

    def test_add_assignee(self, sample_issue: dict) -> None:
        """add_assignee adds assignee to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_assignee().build_lines()
        assert any("John Doe" in line for line in lines)

    def test_add_reporter(self, sample_issue: dict) -> None:
        """add_reporter adds reporter to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_reporter().build_lines()
        assert any("Jane Smith" in line for line in lines)

    def test_add_created(self, sample_issue: dict) -> None:
        """add_created adds created date to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_created().build_lines()
        assert any("2024-01-15" in line for line in lines)

    def test_add_updated(self, sample_issue: dict) -> None:
        """add_updated adds updated date to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_updated().build_lines()
        assert any("2024-01-16" in line for line in lines)

    def test_add_components(self, sample_issue: dict) -> None:
        """add_components adds components to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_components().build_lines()
        assert any("API" in line and "Backend" in line for line in lines)

    def test_add_components_empty(self, minimal_issue: dict) -> None:
        """add_components with no components adds nothing."""
        builder = IssuePanelBuilder(minimal_issue)
        lines = builder.add_components().build_lines()
        assert len(lines) == 0

    def test_add_labels(self, sample_issue: dict) -> None:
        """add_labels adds labels to lines."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_labels().build_lines()
        assert any("urgent" in line and "bug" in line for line in lines)

    def test_add_labels_empty(self, minimal_issue: dict) -> None:
        """add_labels with no labels adds nothing."""
        builder = IssuePanelBuilder(minimal_issue)
        lines = builder.add_labels().build_lines()
        assert len(lines) == 0

    def test_add_all_standard(self, sample_issue: dict) -> None:
        """add_all_standard adds all standard fields."""
        builder = IssuePanelBuilder(sample_issue)
        lines = builder.add_all_standard().build_lines()
        # Should have key, summary, status, priority, type, assignee, reporter, dates, components, labels
        assert len(lines) >= 10

    def test_build_returns_panel(self, sample_issue: dict) -> None:
        """build returns a Rich Panel."""
        builder = IssuePanelBuilder(sample_issue)
        panel = builder.add_key().build()
        assert isinstance(panel, Panel)

    def test_default_classmethod(self, sample_issue: dict) -> None:
        """default classmethod builds complete panel."""
        panel = IssuePanelBuilder.default(sample_issue)
        assert isinstance(panel, Panel)

    def test_method_chaining(self, sample_issue: dict) -> None:
        """Methods can be chained."""
        lines = (
            IssuePanelBuilder(sample_issue)
            .add_key()
            .add_summary()
            .add_status()
            .build_lines()
        )
        assert len(lines) == 3


class TestIssueHeaderBuilder:
    """Tests for IssueHeaderBuilder class."""

    def test_build_returns_table(self, sample_issue: dict) -> None:
        """build returns a Rich Table."""
        from rich.table import Table

        builder = IssueHeaderBuilder(sample_issue)
        table = builder.add_key().build()
        assert isinstance(table, Table)

    def test_build_panel_returns_panel(self, sample_issue: dict) -> None:
        """build_panel returns a Rich Panel."""
        builder = IssueHeaderBuilder(sample_issue)
        panel = builder.add_key().build_panel()
        assert isinstance(panel, Panel)

    def test_default_classmethod(self, sample_issue: dict) -> None:
        """default classmethod builds complete panel."""
        panel = IssueHeaderBuilder.default(sample_issue)
        assert isinstance(panel, Panel)


class TestFormatIssue:
    """Tests for format_issue function."""

    @patch("jira_tool.document.display.panels.console")
    def test_invalid_issue_shows_error(self, mock_console) -> None:
        """Invalid issue data shows error message."""
        format_issue({})
        mock_console.print.assert_called()
        call_args = str(mock_console.print.call_args)
        assert "Invalid" in call_args or "red" in call_args

    @patch("jira_tool.document.display.panels.console")
    def test_valid_issue_prints_panel(self, mock_console, sample_issue: dict) -> None:
        """Valid issue prints panel to console."""
        format_issue(sample_issue)
        mock_console.print.assert_called()

    @patch("jira_tool.document.display.panels.console")
    def test_issue_with_description(self, mock_console) -> None:
        """Issue with description prints description."""
        issue = {
            "key": "TEST-1",
            "fields": {
                "summary": "Test",
                "status": {"name": "Open"},
                "description": "Plain text description",
            },
        }
        format_issue(issue)
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("Description" in c for c in calls)

    @patch("jira_tool.document.display.panels.console")
    def test_issue_with_adf_description(self, mock_console) -> None:
        """Issue with ADF description extracts text."""
        issue = {
            "key": "TEST-1",
            "fields": {
                "summary": "Test",
                "status": {"name": "Open"},
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "ADF content"}],
                        }
                    ],
                },
            },
        }
        format_issue(issue)
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("ADF content" in c for c in calls)

    @patch("jira_tool.document.display.panels.console")
    def test_issue_with_labels(self, mock_console) -> None:
        """Issue with labels prints labels."""
        issue = {
            "key": "TEST-1",
            "fields": {
                "summary": "Test",
                "status": {"name": "Open"},
                "labels": ["urgent", "important"],
            },
        }
        format_issue(issue)
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("urgent" in c for c in calls)

    @patch("jira_tool.document.display.panels.console")
    def test_issue_with_parent(self, mock_console) -> None:
        """Issue with parent prints parent key."""
        issue = {
            "key": "TEST-1",
            "fields": {
                "summary": "Test",
                "status": {"name": "Open"},
                "parent": {"key": "EPIC-100"},
            },
        }
        format_issue(issue)
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("EPIC-100" in c for c in calls)
