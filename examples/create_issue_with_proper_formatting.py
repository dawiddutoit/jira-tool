#!/usr/bin/env python3
"""
Example: Create a properly formatted Jira issue using IssueBuilder.

This demonstrates how to use the IssueBuilder to create comprehensive,
well-structured issues with proper sections for descriptions, acceptance
criteria, implementation details, and testing.
"""

import os
from dotenv import load_dotenv

from jira_tool import JiraClient, IssueBuilder

# Load environment
load_dotenv()


def create_proper_issue_example():
    """Create a properly formatted issue with all sections."""
    # Initialize client
    client = JiraClient()

    # Build the issue description using IssueBuilder
    # This creates a richly formatted description with sections for:
    # - Title with emoji
    # - Component, Story Points, Epic info
    # - Clear description
    # - Implementation details
    # - Acceptance criteria
    issue_builder = IssueBuilder(
        title="Implement user authentication",
        component="Backend Services",
        story_points=8,
        epic_key="PROJ-100",
    )

    # Add clear, structured description
    issue_builder.add_description(
        "Implement OAuth2-based authentication system to secure API endpoints "
        "and allow users to authenticate using their corporate credentials."
    )

    # Add implementation details - what needs to be done
    issue_builder.add_implementation_details(
        [
            "Set up OAuth2 provider configuration",
            "Create authentication middleware for API routes",
            "Implement token refresh mechanism with expiration",
            "Add user session management and logout functionality",
            "Create authentication error handling and response codes",
            "Add rate limiting for authentication attempts",
        ]
    )

    # Add acceptance criteria - how to know when it's done
    issue_builder.add_acceptance_criteria(
        [
            "Users can authenticate using corporate OAuth2 credentials",
            "Access tokens are generated and returned on successful login",
            "Refresh tokens allow extending sessions without re-authentication",
            "Expired tokens return 401 Unauthorized responses",
            "Rate limiting prevents brute force attacks (max 5 attempts/minute)",
            "All endpoints return consistent authentication error messages",
            "Session data is stored securely with encryption",
        ]
    )

    # Build the final ADF (Atlassian Document Format) content
    adf_content = issue_builder.build()

    # Create the issue in Jira
    print("Creating issue: 'Implement user authentication'...")
    issue_data = {
        "project": {"key": "PROJ"},
        "summary": "Implement user authentication",
        "issuetype": {"name": "Task"},
        "description": adf_content,
        "priority": {"name": "High"},
        "labels": ["backend", "security", "authentication"],
    }

    result = client.create_issue(issue_data)
    print(f"✓ Issue created successfully: {result['key']}")
    print(f"\nView the issue:")
    print(f"  uv run jira-tool get {result['key']}")
    return result["key"]


def create_epic_example():
    """Create a properly formatted epic with all sections."""
    from jira_tool import EpicBuilder

    # Initialize client
    client = JiraClient()

    # Build the epic using EpicBuilder
    epic_builder = EpicBuilder(
        title="Redesign User Dashboard",
        priority="P1",
        dependencies="Design system completion (PROJ-50)",
        services="Frontend, Backend API, Analytics",
    )

    # Add problem statement - why are we doing this?
    epic_builder.add_problem_statement(
        "Current dashboard is slow to load and doesn't provide users with "
        "actionable insights. We need a complete redesign to improve performance "
        "and user engagement."
    )

    # Add detailed description
    epic_builder.add_description(
        "Complete redesign of the user dashboard with modern UX patterns, "
        "improved performance through component optimization and caching, "
        "and new features for data visualization and insights."
    )

    # Add technical requirements
    epic_builder.add_technical_details(
        requirements=[
            "Implement React 18+ with Suspense for data loading",
            "Add Redux Toolkit for state management",
            "Integrate Recharts for interactive visualizations",
            "Implement server-side pagination for large datasets",
            "Add service worker for offline support",
            "Use CSS-in-JS for component styling",
        ],
        code_example=(
            "// Example: Dashboard component with Suspense\n"
            "import { Suspense } from 'react';\n"
            "import DashboardContent from './DashboardContent';\n\n"
            "export default function Dashboard() {\n"
            "  return (\n"
            "    <Suspense fallback={<LoadingSpinner />}>\n"
            "      <DashboardContent />\n"
            "    </Suspense>\n"
            "  );\n"
            "}"
        ),
        code_language="javascript",
    )

    # Add acceptance criteria - definition of done
    epic_builder.add_acceptance_criteria(
        [
            "Dashboard loads in under 2 seconds on 4G networks",
            "All components are responsive on mobile (320px+)",
            "Users can customize widget arrangement",
            "Real-time data updates using WebSockets",
            "100% lighthouse performance score ≥ 90",
            "Full accessibility compliance (WCAG 2.1 AA)",
        ]
    )

    # Add edge cases
    epic_builder.add_edge_cases(
        [
            "Handle missing or incomplete data gracefully",
            "Support users with limited bandwidth",
            "Manage rapid widget updates without UI flicker",
            "Handle session expiry during dashboard use",
        ]
    )

    # Add testing considerations
    epic_builder.add_testing_considerations(
        [
            "Unit tests for all dashboard components (>80% coverage)",
            "Integration tests for data fetching and state management",
            "E2E tests for common user workflows",
            "Performance testing under various network conditions",
            "Accessibility testing with screen readers",
            "Load testing with 1000+ concurrent users",
        ]
    )

    # Build the final ADF content
    adf_content = epic_builder.build()

    # Create the epic in Jira
    print("Creating epic: 'Redesign User Dashboard'...")
    epic_data = {
        "project": {"key": "PROJ"},
        "summary": "Redesign User Dashboard",
        "issuetype": {"name": "Epic"},
        "description": adf_content,
        "priority": {"name": "Highest"},
        "labels": ["frontend", "ux", "performance"],
    }

    result = client.create_issue(epic_data)
    print(f"✓ Epic created successfully: {result['key']}")
    print(f"\nView the epic:")
    print(f"  uv run jira-tool get {result['key']}")
    return result["key"]


if __name__ == "__main__":
    print("=" * 70)
    print("JIRA ISSUE CREATION EXAMPLES")
    print("=" * 70)
    print()

    print("Example 1: Create a Task with Proper Formatting")
    print("-" * 70)
    task_key = create_proper_issue_example()
    print()

    print("Example 2: Create an Epic with Complete Structure")
    print("-" * 70)
    epic_key = create_epic_example()
    print()

    print("=" * 70)
    print("Summary:")
    print(f"  Task created: {task_key}")
    print(f"  Epic created: {epic_key}")
    print()
    print("These issues demonstrate the use of IssueBuilder and EpicBuilder")
    print("for creating comprehensive, properly formatted Jira tickets.")
    print("=" * 70)
