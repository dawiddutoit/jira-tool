# Jira Tool

A comprehensive Jira API client and CLI tool for interacting with Jira Cloud instances.
Useful to automate workflows, create rich ADF content, and analyze workflow state durations.
Use it to in your agents / prompts / instructions for AI agents, or build automation scripts.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [First Commands](#first-commands)
- [Usage](#usage)
  - [Command Line](#command-line)
  - [Python API](#python-api)
- [Documentation](#documentation)
- [Development](#development)
- [Requirements](#requirements)

## Features

**Built for AI agents and automation workflows:**

- **Agent-First Design** - Enable AI agents to retrieve tickets, parse requirements, and create implementation plans
- **Jira API Client** - Python and CLI interface to Jira Cloud REST API v3
- **Structured Data Export** - Export issues in JSON, JSONL, CSV formats optimized for agent processing
- **Document Builder** - Programmatically create ADF-formatted issues and epics with proper structure
- **Workflow Analysis** - Analyze state durations and bottlenecks for retrospectives
- **Epic & Sprint Management** - Retrieve epics with children, filter by sprint, group by assignee/status
- **JQL Support** - Advanced filtering for complex queries and batch operations
- **Claude Code Integration** - Works with prompts in `.github/` for ticket retrieval, parsing, and planning workflows

## Quick Start

### Installation

**Option 1: System-wide installation (recommended)**

Install globally so `jira-tool` is available anywhere:

```bash
# Clone the repository
git clone <repository-url>
cd jira-tool

# Build and install
./scripts/build_and_install.sh

# Verify installation
jira-tool --help
```

**Option 2: Development installation**

For development or testing:

```bash
# Install with uv (recommended)
uv sync

# Run commands
uv run jira-tool --help
```

See [scripts/README.md](scripts/README.md) for more installation options.

### Configuration

Set up your Jira credentials:

```bash
# Required environment variables
export JIRA_BASE_URL="https://your-company.atlassian.net"
export JIRA_USERNAME="your-email@example.com"
export JIRA_API_TOKEN="your-api-token"
```

**Get API token:** https://id.atlassian.com/manage-profile/security/api-tokens

See **[Setup Guide](docs/guides/jira_setup.md)** for detailed instructions including `.env` file setup, token generation, troubleshooting, and security best practices.

### First Commands

```bash
# Get issue details
jira-tool get PROJ-123

# Search for issues
jira-tool search "project = PROJ AND status = Open"

# Create a task
jira-tool create --summary "Fix login bug" --type Task

# Export to CSV
jira-tool export --project PROJ --format csv -o tickets.csv

# View your active work
jira-tool export --assignee "me" --status "In Progress"
```

## Usage

### Command Line

The CLI provides 10+ commands for issue operations (get, create, update, comment, transitions), search with JQL, epic management, data export in multiple formats (table, JSON, CSV, JSONL), and workflow state analysis. Designed for both interactive use and automation/agent workflows.

**Quick examples:**
```bash
jira-tool get PROJ-123                          # Get issue details
jira-tool search "status = 'In Progress'"       # Search with JQL
jira-tool export --assignee "me" --format csv   # Export your tickets
jira-tool analyze state-durations issues.json   # Workflow analysis
```

**See:** [CLI Reference](docs/reference/cli_reference.md) for all commands and [Usage Guide](docs/guides/usage_guide.md) for workflows and examples.

### Python API

The Python API provides `JiraClient` for all Jira operations, document builders (`IssueBuilder`, `EpicBuilder`, `JiraDocumentBuilder`) for creating ADF-formatted content, and `StateDurationAnalyzer` for workflow analysis. Use it to build automation scripts, integrate with other tools, or create custom workflows for AI agents.

**Quick example:**
```python
from jira_tool import JiraClient, IssueBuilder

# Get issues and create structured content
client = JiraClient()
issue = client.get_issue("PROJ-123")

builder = IssueBuilder(title="New feature", story_points=8)
builder.add_description("Feature description")
builder.add_acceptance_criteria(["Criteria 1", "Criteria 2"])

client.create_issue({
    "project": {"key": "PROJ"},
    "summary": "New feature",
    "issuetype": {"name": "Task"},
    "description": builder.build()
})
```

**See:** [Python API Guide](docs/guides/python_api_guide.md) for complete API documentation with examples.

## Documentation

### Guides

- **[Setup Guide](docs/guides/jira_setup.md)** - Configure Jira credentials with environment variables or `.env` files, generate API tokens, troubleshoot connection issues, and follow security best practices.

- **[Usage Guide](docs/guides/usage_guide.md)** - Common workflows including daily standup prep, sprint planning, bug triage, epic management, data export strategies, workflow analysis, and automation tips.

- **[Python API Guide](docs/guides/python_api_guide.md)** - Complete API reference for `JiraClient`, document builders, state analysis, error handling, and real-world examples for automation.

- **[Formatting Guide](docs/guides/jira_formatting_guide.md)** - Create rich Atlassian Document Format (ADF) content with headings, lists, code blocks, panels, and formatting.

### Reference

- **[CLI Reference](docs/reference/cli_reference.md)** - Complete command documentation with all options, arguments, JQL patterns, output formats, and common use cases.

- **[ADF Reference](docs/reference/adf_reference_guide.md)** - Atlassian Document Format structure, node types, and formatting reference.

### Examples

- **[examples/create_issue_with_proper_formatting.py](examples/create_issue_with_proper_formatting.py)** - Demonstrates `IssueBuilder` and `EpicBuilder` with comprehensive examples.

## Development

### Setup Development Environment

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=jira_tool

# Format code
uv run black src/ tests/

# Lint code
uv run ruff src/ tests/

# Type check
uv run mypy src/
```

### Project Structure

```
jira-tool/
├── src/jira_tool/           # Main package
│   ├── client.py            # JiraClient API
│   ├── formatter.py         # Document builders
│   ├── cli.py               # CLI commands
│   └── analysis/            # State analysis
├── docs/                    # Documentation
│   ├── guides/              # User guides
│   └── reference/           # API reference
├── examples/                # Example scripts
├── tests/                   # Test suite
└── scripts/                 # Build and install scripts
```

### Running Tests

```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/test_client.py

# Specific test function
uv run pytest tests/test_client.py::test_get_issue

# With coverage report
uv run pytest --cov=jira_tool --cov-report=html
```

### Code Quality

The project enforces:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking (strict mode)
- **Pytest** for testing (>80% coverage)

Always run linting and tests before committing:

```bash
# Format, lint, and test
uv run black src/ tests/
uv run ruff src/ tests/
uv run pytest
```

## Requirements

- **Python 3.11+**
- **Jira Cloud** (REST API v3)
- **Valid Jira API token**

## License

This project is distributed as-is without a specific license.

## Support

For issues and questions:
- Check the [documentation](docs/)
- Review the [examples](examples/)
- Create an issue in the repository

---

**Quick Links:**
- [Getting Started](docs/guides/jira_setup.md)
- [Command Reference](docs/reference/cli_reference.md)
- [Python API](docs/guides/python_api_guide.md)
- [Examples](examples/)
