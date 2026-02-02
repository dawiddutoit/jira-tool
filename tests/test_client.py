"""Tests for Jira client."""

from unittest.mock import MagicMock, patch

import pytest

from jira_tool.client import JiraClient
from tests.conftest import TEST_JIRA_API_TOKEN, TEST_JIRA_BASE_URL, TEST_JIRA_USERNAME


@pytest.fixture
def jira_client():
    """Create a Jira client with mocked credentials."""
    with patch.dict(
        "os.environ",
        {
            "JIRA_BASE_URL": TEST_JIRA_BASE_URL,
            "JIRA_USERNAME": TEST_JIRA_USERNAME,
            "JIRA_API_TOKEN": TEST_JIRA_API_TOKEN,
        },
    ):
        return JiraClient()


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = MagicMock()
    response.json.return_value = {
        "issues": [{"key": "TEST-1", "fields": {"summary": "Test Issue"}}],
        "isLast": True,
    }
    response.raise_for_status = MagicMock()
    return response


class TestSearchIssues:
    """Tests for search_issues method."""

    def test_search_issues_without_expand(self, jira_client, mock_response):
        """Test search_issues without expand parameter."""
        with patch.object(
            jira_client, "_request", return_value=mock_response
        ) as mock_request:
            issues, is_last = jira_client.search_issues("project = TEST")

            # Verify the request was made with correct parameters
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0] == (
                "GET",
                f"{TEST_JIRA_BASE_URL}/rest/api/3/search/jql",
            )

            # Check params don't include expand
            params = call_args[1]["params"]
            assert "jql" in params
            assert params["jql"] == "project = TEST"
            assert "expand" not in params

            # Verify result
            assert issues == [{"key": "TEST-1", "fields": {"summary": "Test Issue"}}]
            assert is_last is True

    def test_search_issues_with_expand_single(self, jira_client, mock_response):
        """Test search_issues with single expand parameter."""
        with patch.object(
            jira_client, "_request", return_value=mock_response
        ) as mock_request:
            issues, is_last = jira_client.search_issues("project = TEST", expand=["changelog"])

            # Verify the request was made with correct parameters
            mock_request.assert_called_once()
            call_args = mock_request.call_args

            # Check params include expand
            params = call_args[1]["params"]
            assert "expand" in params
            assert params["expand"] == "changelog"

            # Verify result
            assert issues == [{"key": "TEST-1", "fields": {"summary": "Test Issue"}}]
            assert is_last is True

    def test_search_issues_with_expand_multiple(self, jira_client, mock_response):
        """Test search_issues with multiple expand parameters."""
        with patch.object(
            jira_client, "_request", return_value=mock_response
        ) as mock_request:
            issues, is_last = jira_client.search_issues(
                "project = TEST", expand=["changelog", "transitions", "renderedFields"]
            )

            # Verify the request was made with correct parameters
            mock_request.assert_called_once()
            call_args = mock_request.call_args

            # Check params include expand with comma-separated values
            params = call_args[1]["params"]
            assert "expand" in params
            assert params["expand"] == "changelog,transitions,renderedFields"

            # Verify result
            assert issues == [{"key": "TEST-1", "fields": {"summary": "Test Issue"}}]
            assert is_last is True

    def test_search_issues_with_all_parameters(self, jira_client, mock_response):
        """Test search_issues with all parameters including expand.

        Note: start_at parameter is deprecated in the new API and not sent to the server.
        The new API uses token-based pagination via nextPageToken.
        """
        with patch.object(
            jira_client, "_request", return_value=mock_response
        ) as mock_request:
            issues, is_last = jira_client.search_issues(
                "project = TEST",
                fields=["summary", "status"],
                _start_at=10,  # This parameter is accepted for backward compatibility but ignored
                max_results=25,
                expand=["changelog"],
            )

            # Verify the request was made with correct parameters
            mock_request.assert_called_once()
            call_args = mock_request.call_args

            # Check all params are present (except startAt which is deprecated)
            params = call_args[1]["params"]
            assert params["jql"] == "project = TEST"
            assert params["fields"] == "summary,status"
            # startAt is no longer sent to the API (deprecated in favor of nextPageToken)
            assert "startAt" not in params
            assert params["maxResults"] == 25
            assert params["expand"] == "changelog"

            # Verify result
            assert issues == [{"key": "TEST-1", "fields": {"summary": "Test Issue"}}]
            assert is_last is True

    def test_search_issues_backwards_compatibility(self, jira_client, mock_response):
        """Test that existing code without expand parameter still works."""
        with patch.object(
            jira_client, "_request", return_value=mock_response
        ) as mock_request:
            # Call with original signature (no expand)
            issues, is_last = jira_client.search_issues(
                jql="project = TEST", fields=["summary"], _start_at=0, max_results=50
            )

            # Verify the request was made correctly
            mock_request.assert_called_once()
            call_args = mock_request.call_args

            # Check params don't include expand
            params = call_args[1]["params"]
            assert "expand" not in params

            # Verify result
            assert issues == [{"key": "TEST-1", "fields": {"summary": "Test Issue"}}]
            assert is_last is True


class TestGetEpics:
    """Tests for get_epics method that uses search_issues internally."""

    def test_get_epics_uses_search_issues(self, jira_client):
        """Test that get_epics correctly calls search_issues without breaking."""
        with patch.object(
            jira_client, "search_issues", return_value=([{"key": "EPIC-1"}], True)
        ) as mock_search:
            result = jira_client.get_epics("PROJ", max_results=25)

            # Verify search_issues was called with correct parameters
            mock_search.assert_called_once_with(
                "project = PROJ AND issuetype = Epic ORDER BY created DESC",
                max_results=25,
            )

            # Verify result
            assert result == [{"key": "EPIC-1"}]
