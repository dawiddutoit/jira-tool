# Jira Tool Usage Guide

Practical examples and common use cases for the `jira-tool` CLI.

## Table of Contents

- [Running Commands](#running-commands)
- [Common Workflows](#common-workflows)
- [Advanced Filtering](#advanced-filtering)
- [Working with Epics](#working-with-epics)
- [Data Export & Analysis](#data-export--analysis)
- [Workflow State Analysis](#workflow-state-analysis)
- [Team Collaboration](#team-collaboration)
- [Tips & Best Practices](#tips--best-practices)

## Running Commands

This guide uses `jira-tool [command]` in examples for brevity. Choose the method that matches your setup:

**System-Wide Installation:**
```bash
jira-tool get PROJ-123
```
Use this if you ran `./scripts/build_and_install.sh` and set environment variables in your shell profile.

**Development Mode:**
```bash
uv run jira-tool get PROJ-123
```
Use this if you're working from the project directory with a `.env` file.

**Examples in this guide work with both methods** - just prefix with `uv run` if using development mode.

## Common Workflows

### Daily Standup Prep

Get your active work and recently updated issues:

```bash
# Your issues in progress
jira-tool export --assignee "me" --status "In Progress"

# Issues you updated recently
jira-tool search "assignee = currentUser() AND updated >= -1d"

# Summary of all your active work
jira-tool export --assignee "me" --jql "status NOT IN (Done, Closed)"
```

### Sprint Planning

Review and organize sprint work:

```bash
# Backlog items for planning
jira-tool export --status "To Do" --priority High --format table

# Current sprint issues
jira-tool search "sprint in openSprints()" --format json -o sprint.json

# Completed work this sprint
jira-tool export --status Done --created "-14d" --format csv -o completed.csv

# Unassigned tasks
jira-tool search "project = PROJ AND assignee is EMPTY AND type = Task"
```

### Bug Triage

Manage and prioritize bugs:

```bash
# All open bugs
jira-tool export --type Bug --jql "resolution = Unresolved"

# High priority bugs
jira-tool export --type Bug --priority High --format csv -o critical_bugs.csv

# Recent bugs (last 7 days)
jira-tool export --type Bug --created "-7d" --format table

# Bugs by assignee
jira-tool export --type Bug --group-by assignee --stats
```

### Release Management

Track release progress:

```bash
# All issues in epic
jira-tool epic-details PROJ-100 --show-children --format json -o release.json

# Issues by status
jira-tool export --epic PROJ-100 --group-by status --stats

# Remaining work
jira-tool search "Epic Link = PROJ-100 AND status NOT IN (Done, Closed)"

# Export for release notes
jira-tool export --epic PROJ-100 --status Done --format csv -o release_notes.csv
```

### Quick Updates

Common update operations:

```bash
# Move to in progress and assign to yourself
jira-tool update PROJ-123 --status "In Progress" --assignee "me@example.com"

# Mark as high priority
jira-tool update PROJ-123 --priority High

# Add labels for tracking
jira-tool update PROJ-123 --labels "urgent,security,backend"

# Add comment with update
jira-tool comment PROJ-123 -m "Working on this now, ETA tomorrow"
```

## Advanced Filtering

### Date-Based Filtering

```bash
# Issues created today
jira-tool export --created "today"

# Issues created this week
jira-tool search "created >= startOfWeek()"

# Issues created in last 7 days
jira-tool export --created "-7d"

# Issues created in January 2024
jira-tool search "created >= 2024-01-01 AND created <= 2024-01-31"

# Recently updated (last hour)
jira-tool search "updated >= -1h"

# Stale issues (not updated in 30 days)
jira-tool search "updated <= -30d AND status NOT IN (Done, Closed)"
```

### Complex JQL Queries

```bash
# Multiple conditions with AND
jira-tool search "project = PROJ AND status = 'In Progress' AND assignee = currentUser()"

# Multiple conditions with OR
jira-tool search "priority = High OR priority = Highest"

# Combining AND/OR with parentheses
jira-tool search "project = PROJ AND (status = 'In Progress' OR status = Review) AND priority = High"

# NOT operator
jira-tool search "project = PROJ AND status NOT IN (Done, Closed, Cancelled)"

# IN operator for multiple values
jira-tool search "priority IN (High, Highest) AND type IN (Bug, 'Production Issue')"

# Text search
jira-tool search "project = PROJ AND summary ~ 'authentication'"
jira-tool search "description ~ 'database migration'"

# Custom field filtering
jira-tool search "project = PROJ AND 'Story Points' >= 5"

# Empty/null checks
jira-tool search "assignee is EMPTY AND priority = High"
jira-tool search "'Due Date' is not EMPTY"
```

### Component & Label Filtering

```bash
# Issues in specific component
jira-tool export --component "Backend Services"

# Multiple components (use JQL)
jira-tool search "component IN ('Backend Services', 'Frontend')"

# Issues with specific label
jira-tool search "labels = urgent"

# Issues with any of multiple labels
jira-tool search "labels IN (urgent, security, performance)"

# Issues without labels
jira-tool search "labels is EMPTY"
```

## Working with Epics

### Epic Discovery

```bash
# List all epics in project
jira-tool epics --project PROJ

# Export epic list as JSON
jira-tool epics --project PROJ --format json -o epics.json

# Find epics by name
jira-tool search "project = PROJ AND type = Epic AND summary ~ 'API'"
```

### Epic Analysis

```bash
# Get epic with all children
jira-tool epic-details PROJ-100 --show-children

# Export epic structure as JSON
jira-tool epic-details PROJ-100 --show-children --format json -o epic_structure.json

# Get issues in epic by status
jira-tool search "'Epic Link' = PROJ-100" --format table

# Count issues in epic
jira-tool search "'Epic Link' = PROJ-100" --jql "Epic Link = PROJ-100" --stats
```

### Epic Progress Tracking

```bash
# Epic completion status
jira-tool export --jql "'Epic Link' = PROJ-100" --group-by status --stats

# Remaining work in epic
jira-tool search "'Epic Link' = PROJ-100 AND status NOT IN (Done, Closed)"

# Completed items
jira-tool search "'Epic Link' = PROJ-100 AND status = Done" --format csv -o completed.csv

# Issues by assignee
jira-tool export --jql "'Epic Link' = PROJ-100" --group-by assignee --stats
```

## Data Export & Analysis

### Export Strategies

**Small Dataset (< 50 issues):**
```bash
# Use table for quick viewing
jira-tool export --project PROJ --format table

# Or JSON for further processing
jira-tool export --project PROJ --format json -o issues.json
```

**Medium Dataset (50-500 issues):**
```bash
# JSON for readability
jira-tool export --project PROJ --all --format json -o all_issues.json

# CSV for spreadsheet analysis
jira-tool export --project PROJ --all --format csv -o all_issues.csv
```

**Large Dataset (500+ issues):**
```bash
# JSONL for efficiency (recommended)
jira-tool export --project PROJ --all --format jsonl -o all_issues.jsonl

# Process line by line
cat all_issues.jsonl | jq -r '.key'
```

### Filtered Exports

```bash
# Active work across team
jira-tool export --status "In Progress" --all --format csv -o active_work.csv

# High priority backlog
jira-tool export --status "To Do" --priority High --format json -o backlog.json

# All bugs for analysis
jira-tool export --type Bug --all --format jsonl -o all_bugs.jsonl

# Issues by component
jira-tool export --component "Backend Services" --format csv -o backend.csv
```

### Grouping & Statistics

```bash
# Issues by assignee
jira-tool export --group-by assignee --stats

# Issues by status
jira-tool export --group-by status --stats

# Issues by priority
jira-tool export --group-by priority --stats

# Export grouped data as CSV
jira-tool export --group-by assignee --format csv -o by_assignee.csv
```

## Workflow State Analysis

### Analyzing State Durations

Understand how long issues spend in each workflow state:

**Step 1: Export with changelog**
```bash
# Export issues with full history
jira-tool export --project PROJ --expand changelog --format json -o issues_with_history.json

# Or for specific issues
jira-tool search "project = PROJ AND created >= -30d" --expand changelog --format json -o recent_issues.json
```

**Step 2: Analyze durations**
```bash
# Generate duration analysis
jira-tool analyze state-durations issues_with_history.json -o state_durations.csv
```

**Step 3: Review results**
```bash
# View in spreadsheet application
open state_durations.csv

# Or use command line tools
cat state_durations.csv | column -t -s,
```

### Interpreting Results

The analysis produces a CSV with:
- **issue_key** - The issue identifier
- **state** - Workflow state name
- **duration_calendar_days** - Total days (including weekends)
- **duration_business_hours** - Hours during business time (9 AM - 5 PM, weekdays)

**Example uses:**
- Identify bottlenecks (states with longest durations)
- Calculate cycle time (sum of all state durations)
- Compare business hours vs calendar days
- Track workflow efficiency over time

### Common Analysis Patterns

```bash
# Analyze recent sprint
jira-tool search "sprint = 'Sprint 10'" --expand changelog --format json -o sprint10.json
jira-tool analyze state-durations sprint10.json -o sprint10_durations.csv

# Analyze specific epic
jira-tool search "'Epic Link' = PROJ-100" --expand changelog --format json -o epic100.json
jira-tool analyze state-durations epic100.json -o epic100_durations.csv

# Analyze bugs for triage performance
jira-tool export --type Bug --created "-30d" --expand changelog --format json -o bugs.json
jira-tool analyze state-durations bugs.json -o bug_durations.csv
```

## Team Collaboration

### Reviewing Team Work

```bash
# Team capacity view
jira-tool export --jql "assignee is not EMPTY AND status NOT IN (Done, Closed)" --group-by assignee

# Unassigned issues
jira-tool search "project = PROJ AND assignee is EMPTY" --format table

# Overdue items (with due date)
jira-tool search "due < now() AND status NOT IN (Done, Closed)"

# Blocked items
jira-tool search "status = Blocked" --format csv -o blocked_items.csv
```

### Code Review Workflow

```bash
# Issues in review
jira-tool export --status Review --format table

# Your items needing review
jira-tool export --assignee "me" --status Review

# Add review comment
jira-tool comment PROJ-123 -m "LGTM, approved for merge"

# Move to done after merge
jira-tool update PROJ-123 --status Done
```

### Handoffs & Reassignment

```bash
# Check before handoff
jira-tool get PROJ-123

# Add handoff comment
jira-tool comment PROJ-123 -m "Handing off to @john - context: implemented auth, tests passing"

# Reassign
jira-tool update PROJ-123 --assignee "john@example.com"
```

## Tips & Best Practices

### Performance Optimization

**Use JSONL for large exports:**
```bash
# More efficient for 100+ issues
jira-tool export --project PROJ --all --format jsonl -o large_export.jsonl
```

**Limit results when exploring:**
```bash
# Use --max-results for quick checks
jira-tool search "project = PROJ" --max-results 10
```

**Use specific fields to reduce payload:**
```bash
# Only get what you need
jira-tool search "project = PROJ" --fields key,summary,status
```

### Automation & Scripting

**Batch processing:**
```bash
# Export, process, update
jira-tool export --status "To Do" --format json -o todo.json

# Parse and update each
cat todo.json | jq -r '.issues[].key' | while read key; do
  jira-tool update "$key" --priority High
done
```

**Daily reports:**
```bash
#!/bin/bash
# daily_report.sh
DATE=$(date +%Y-%m-%d)
jira-tool export --assignee "me" --format csv -o "report_${DATE}.csv"
echo "Report saved to report_${DATE}.csv"
```

**Integration with other tools:**
```bash
# Export to JSON for processing
jira-tool export --project PROJ --format json -o issues.json

# Process with jq
cat issues.json | jq '.issues[] | select(.fields.priority.name == "High")'

# Convert to another format
cat issues.json | jq -r '.issues[] | [.key, .fields.summary] | @csv'
```

### Error Handling

**Check for errors:**
```bash
# Save output and check exit code
jira-tool get PROJ-123 > output.txt
if [ $? -eq 0 ]; then
  echo "Success"
else
  echo "Failed" >&2
fi
```

**Validate before batch operations:**
```bash
# Check if issue exists first
jira-tool get PROJ-123 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  jira-tool update PROJ-123 --status Done
fi
```

### Working with Different Environments

**Multiple Jira instances:**
```bash
# Use different env files
export $(grep -v '^#' .env.production | xargs)
jira-tool export --project PROJ --format csv -o prod_issues.csv

export $(grep -v '^#' .env.staging | xargs)
jira-tool export --project PROJ --format csv -o staging_issues.csv
```

**Project-specific defaults:**
```bash
# Set in .env file
JIRA_DEFAULT_PROJECT=MYTEAM
JIRA_DEFAULT_COMPONENT="Backend Services"

# Then use without specifying
jira-tool export --format table
```

### Output Formatting Tips

**Pretty print JSON:**
```bash
# Already pretty by default
jira-tool get PROJ-123 --format json

# Or pipe through jq for custom formatting
jira-tool search "project = PROJ" --format json | jq '.issues[] | {key, summary: .fields.summary}'
```

**CSV for Excel:**
```bash
# Export as CSV
jira-tool export --project PROJ --format csv -o issues.csv

# Open in Excel (macOS)
open -a "Microsoft Excel" issues.csv

# Or import into Google Sheets
```

**Table output for terminal:**
```bash
# Default table format is terminal-friendly
jira-tool export --status "In Progress"

# Combine with less for pagination
jira-tool export --all | less
```

### Keyboard Shortcuts & Aliases

Add to your `.zshrc` or `.bashrc`:

```bash
# Quick aliases
alias jt="jira-tool"
alias jtg="jira-tool get"
alias jts="jira-tool search"
alias jtm="jira-tool export --assignee me"
alias jte="jira-tool export"

# Functions for common tasks
jt-mine() {
  jira-tool export --assignee "me" --status "In Progress"
}

jt-review() {
  jira-tool export --status Review
}

jt-bugs() {
  jira-tool export --type Bug --priority High
}
```

Then use:
```bash
jt-mine       # Your active work
jt-review     # Items in review
jt-bugs       # High priority bugs
```

### Data Backup

**Regular backups:**
```bash
#!/bin/bash
# backup_jira.sh
DATE=$(date +%Y%m%d)
PROJECT="PROJ"

# Full backup with history
jira-tool export --project "$PROJECT" --all --expand changelog \
  --format jsonl -o "backup_${PROJECT}_${DATE}.jsonl"

echo "Backup complete: backup_${PROJECT}_${DATE}.jsonl"
```

**Incremental backups:**
```bash
# Daily - get only updated issues
jira-tool search "project = PROJ AND updated >= -1d" \
  --expand changelog --format jsonl -o "incremental_$(date +%Y%m%d).jsonl"
```

## Related Documentation

- [CLI Reference](../reference/cli_reference.md) - Complete command reference
- [Python API Guide](python_api_guide.md) - Using the Python API
- [Setup Guide](jira_setup.md) - Initial configuration
- [ADF Reference](../reference/adf_reference_guide.md) - Document formatting
