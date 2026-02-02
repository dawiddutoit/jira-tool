---
applyTo: "**"
---

# Jira Workflow Prompts: Usage Guide

This document provides clear guidance on when and how to use the three Jira workflow prompts to avoid overlap and ensure efficient development workflows.

## Prompt Overview

### 🗂️ **jira-ticket-retriever.prompt.md**
**Purpose:** Fetch and archive Jira tickets for reference and documentation  
**Output:** Raw ticket data in organized artifact directories  
**Directory:** `/.github/artifacts/YYYY-MM-DD/JIRA-{TICKET_ID}-{title}/ticket.md`

### 📋 **jira-task-parser.prompt.md**  
**Purpose:** Transform Jira tickets into structured, actionable implementation plans  
**Output:** Implementation plans with phases, tasks, and requirements  
**Directory:** 
- **Standalone plans:** `/plan/{purpose}-{component}-{ticket-id}.md`
- **Artifact-based plans:** `/.github/artifacts/YYYY-MM-DD/JIRA-{TICKET_ID}-{title}/implementation-plan.md`

### ⚙️ **task-implementer.prompt.md**
**Purpose:** Execute implementation plans systematically with full traceability  
**Output:** Working code, tests, and updated plan files with completion status  
**Directory:** Updates plans in `/plan/` or `/.github/artifacts/` and creates/modifies source code

## When to Use Which Prompt

### Use **jira-ticket-retriever** when you need to:
- ✅ **Archive tickets for future reference**
  - "Store PROJ-302 in our artifact library"
  - "Keep a record of these requirements for compliance"
  - "Archive completed tickets for post-mortem analysis"

- ✅ **Document historical decisions**
  - "Save this ticket before the requirements change"
  - "Create documentation trail for audit purposes" 
  - "Preserve original ticket content for reference"

- ✅ **Gather related tickets for analysis**
  - "Retrieve all tickets from this epic for review"
  - "Collect tickets PROJ-302, PROJ-303, PROJ-304 for analysis"
  - "Archive tickets before sprint planning"

- ✅ **Export and analyze ticket data**
  - "Export all In Progress tickets to CSV for sprint review"
  - "Get all high priority bugs from last week"
  - "Analyze workflow performance with state durations"
  - "Export epic with all child issues"
  - "Generate reports grouped by assignee or status"

- ✅ **Ask questions about tickets (quick lookup)**
  - "What's PROJ-302 about?"
  - "Show me details of PROJ-302"
  - "What's the status of PROJ-302?"
  - Note: Uses `get` command for fast inquiry without creating artifacts

**Command Selection:**
- **For archival/work**: Uses `export --jql "key = PROJ-302"` (structured data for processing)
- **For quick questions**: Uses `get PROJ-302` (fast display without artifacts)

### Use **jira-task-parser** when you need to:
- ✅ **Create standalone implementation roadmaps**
  - "Break down PROJ-302 into development tasks" → Creates `/plan/feature-messaging-PROJ-302.md`
  - "Create an implementation plan for this feature" → Creates standalone plan file
  - "Plan the technical approach for this ticket" → Creates independent planning document

- ✅ **Create artifact-based implementation plans**
  - "Create implementation plan for /path/to/artifacts/JIRA-PROJ-302/ticket.md" → Creates plan in same artifact directory
  - "Plan implementation for existing ticket artifact" → Creates `implementation-plan.md` alongside `ticket.md`
  - "Add planning to archived ticket" → Keeps related materials together

- ✅ **Estimate effort and identify dependencies**
  - "What's involved in implementing this ticket?"
  - "Create phases for this complex feature"
  - "Identify risks and dependencies for this work"

- ✅ **Structure complex work**
  - "Plan the implementation phases for this epic"
  - "Break this large ticket into manageable tasks"
  - "Create development milestones for this feature"

### Use **task-implementer** when you need to:
- ✅ **Execute structured implementation plans (standalone)**
  - "Implement the plan for feature-messaging-PROJ-302" → Uses `/plan/feature-messaging-PROJ-302.md`
  - "Continue working on the current implementation plan" → Resumes plan in `/plan/` directory
  - "Execute Phase 2 of the authentication feature" → Works with standalone plan files

- ✅ **Execute structured implementation plans (artifact-based)**
  - "Implement plan from /.github/artifacts/2025-11-06/JIRA-PROJ-302/implementation-plan.md"
  - "Continue artifact-based implementation" → Works with plans in artifact directories
  - "Execute implementation plan for archived ticket" → Uses artifact-based planning

- ✅ **Maintain strict traceability**
  - "Track progress against the implementation plan"
  - "Ensure all plan requirements are implemented"
  - "Document implementation progress systematically"

- ✅ **Follow disciplined development process**
  - "Implement with comprehensive testing at each step"
  - "Ensure code quality and project conventions"
  - "Validate implementation against acceptance criteria"

## Complete Workflow Examples

### Workflow 1: New Feature Development
```
1. jira-ticket-retriever: "Retrieve PROJ-302" 
   → Creates: /.github/artifacts/2025-11-06/JIRA-PROJ-302-implement-validation/ticket.md

2. jira-task-parser: "Create implementation plan for PROJ-302"
   → Creates: /plan/feature-messaging-PROJ-302.md

3. task-implementer: "Implement plan feature-messaging-PROJ-302.md"
   → Creates: Source code, tests, updates plan with completion status
```

### Workflow 2: Artifact-Based Planning and Implementation
```
1. jira-ticket-retriever: "Retrieve PROJ-302"
   → Creates: /.github/artifacts/2025-11-06/JIRA-PROJ-302-implement-validation/ticket.md

2. jira-task-parser: "Create implementation plan for /.github/artifacts/2025-11-06/JIRA-PROJ-302-implement-validation/ticket.md"
   → Creates: /.github/artifacts/2025-11-06/JIRA-PROJ-302-implement-validation/implementation-plan.md

3. task-implementer: "Implement plan from /.github/artifacts/2025-11-06/JIRA-PROJ-302-implement-validation/implementation-plan.md"
   → Creates: Source code, tests, updates artifact-based plan
```

### Workflow 3: Epic Analysis and Implementation
```
1. jira-ticket-retriever: "Retrieve epic PROJ-227 and all children"
   → Creates: Multiple artifact files for analysis

2. jira-task-parser: "Create implementation plans for PROJ-302, PROJ-303"
   → Creates: Multiple plan files for coordinated implementation

3. task-implementer: "Implement plan feature-messaging-PROJ-302.md"
   → Executes first feature systematically

4. task-implementer: "Implement plan feature-auth-PROJ-303.md" 
   → Executes second feature with dependency awareness
```

### Workflow 4: Documentation and Reference
```
1. jira-ticket-retriever: "Archive all completed tickets from last sprint"
   → Creates: Historical record for retrospectives

2. Later reference: Check /.github/artifacts/ directory for past decisions
   → Use archived tickets to understand historical context
```

### Workflow 5: Bug Fix Process
```
1. jira-ticket-retriever: "Retrieve bug ticket PROJ-305"
   → Creates: Bug details and reproduction steps

2. jira-task-parser: "Create fix plan for bug PROJ-305"
   → Creates: Structured approach to fix with testing strategy

3. task-implementer: "Implement plan bug-auth-PROJ-305.md"
   → Executes fix with comprehensive validation
```

### Workflow 6: Sprint Analysis and Reporting
```
1. jira-ticket-retriever: "Export all completed tickets from current sprint"
   → Executes: uv run jira-tool export --status Done --format csv -o sprint_completed.csv
   → Creates: CSV report with all completed work

2. jira-ticket-retriever: "Analyze workflow performance for completed tickets"
   → Executes: uv run jira-tool export --status Done --expand changelog --format json -o completed.json
   → Executes: uv run jira-tool analyze state-durations completed.json -o durations.csv
   → Creates: Performance analysis showing time in each state

3. Review artifacts for retrospective insights
```

### Workflow 7: Epic Management
```
1. jira-ticket-retriever: "List all epics in PROJ project"
   → Executes: uv run jira-tool epics --project PROJ
   → Displays: All epics with summary information

2. jira-ticket-retriever: "Get full details for epic PROJ-227 with all children"
   → Executes: uv run jira-tool epic-details PROJ-227 --show-children
   → Creates: /.github/artifacts/YYYY-MM-DD/JIRA-PROJ-227-{title}/ticket.md
   → Includes: Epic details and all child issue references

3. jira-task-parser: "Create implementation plan for epic PROJ-227"
   → Uses artifact data to create coordinated implementation plan
```

### Workflow 8: Advanced Filtering and Grouping
```
1. jira-ticket-retriever: "Show my high priority tasks in progress"
   → Executes: uv run jira-tool export --assignee "me" --status "In Progress" --priority High --format table
   → Displays: Filtered list in console

2. jira-ticket-retriever: "Group all tickets by assignee with statistics"
   → Executes: uv run jira-tool export --group-by assignee --stats --format csv -o by_assignee.csv
   → Creates: Report showing ticket distribution and statistics

3. jira-ticket-retriever: "Export all tickets created this week"
   → Executes: uv run jira-tool export --created "-7d" --format json -o recent_tickets.json
   → Creates: JSON file with recent tickets for further processing
```

## Decision Matrix

| **Need** | **Ticket Retriever** | **Task Parser** | **Task Implementer** |
|----------|---------------------|-----------------|-------------------|
| Archive for reference | ✅ Primary | ❌ | ❌ |
| Create implementation roadmap | ❌ | ✅ Primary | ❌ |
| Execute structured work | ❌ | ❌ | ✅ Primary |
| Document requirements | ✅ Excellent | 🔶 Partial | ❌ |
| Plan technical approach | ❌ | ✅ Excellent | ❌ |
| Write working code | ❌ | ❌ | ✅ Excellent |
| Track implementation progress | ❌ | ❌ | ✅ Excellent |
| Analyze multiple tickets | ✅ Excellent | 🔶 Individually | ❌ |
| Estimate effort | ❌ | ✅ Good | ❌ |
| Ensure code quality | ❌ | 🔶 Planning only | ✅ Excellent |
| Export/reporting | ✅ Excellent | ❌ | ❌ |
| Workflow analysis | ✅ Excellent | ❌ | ❌ |
| Epic management | ✅ Excellent | 🔶 Planning only | ❌ |
| Advanced filtering | ✅ Excellent | ❌ | ❌ |

**Legend:** ✅ Primary use case | 🔶 Partial capability | ❌ Not intended for this use

## Planning Location Decision Guide

### Use **Artifact-Based Planning** (`/.github/artifacts/YYYY-MM-DD/JIRA-{ID}/implementation-plan.md`) when:
- ✅ **You already have an archived ticket** from jira-ticket-retriever
- ✅ **Planning for historical analysis** - want to keep all related materials together
- ✅ **Compliance and audit requirements** - need complete traceability in one location
- ✅ **Sprint retrospectives** - analyzing what was planned vs what was delivered
- ✅ **User asks for plan of existing artifact** - "Create plan for /path/to/artifacts/ticket.md"

### Use **Standalone Planning** (`/plan/{purpose}-{component}-{ticket-id}.md`) when:
- ✅ **Direct ticket-to-implementation flow** - don't need artifact archival
- ✅ **Active development work** - plan will be actively updated during implementation
- ✅ **Cross-ticket coordination** - plan references multiple tickets or epics
- ✅ **User asks for general plan** - "Create implementation plan for PROJ-302"
- ✅ **Working with live tickets** - still in active development

## Anti-Patterns to Avoid

### ❌ **Don't use jira-ticket-retriever for:**
- Creating implementation plans (use jira-task-parser)
- Writing code (use task-implementer) 
- Breaking down complex work (use jira-task-parser)

### ❌ **Don't use jira-task-parser for:**
- Just storing ticket information (use jira-ticket-retriever)
- Actually implementing code (use task-implementer)
- Simple tickets that don't need planning (implement directly)

### ❌ **Don't use task-implementer for:**
- Work without implementation plans (create plan first)
- Ad-hoc coding tasks (use java-engineer prompt)
- Exploratory development (use appropriate specialist prompts)

### ❌ **Don't skip steps in the workflow:**
- Don't implement without planning complex features
- Don't create plans without understanding requirements
- Don't archive tickets without checking if plans are needed

### ❌ **Don't ignore file location context:**
- If user provides artifact path, create plan in same artifact directory
- If user asks for general plan, create in standalone `/plan/` directory
- Don't mix artifact-based and standalone workflows arbitrarily

## Integration with Other Prompts

### **Specialist Prompts for Complex Work:**
When task-implementer encounters specialized needs:
- **Database changes** → Delegate to `flyway-migration.prompt.md`
- **Complex Java development** → Delegate to `java-engineer.prompt.md`  
- **TDD implementation** → Delegate to `tdd-*.prompt.md`
- **Comprehensive testing** → Delegate to `unit-testing.prompt.md`

### **Coordination Patterns:**
- task-implementer maintains overall plan execution
- Specialist prompts handle specific technical challenges
- All work remains traceable to original plan tasks
- Plan files are updated with all implementation progress

## Quick Reference Commands

### Starting a New Feature (Standalone Planning)
```bash
# 1. Archive the ticket (optional)
jira-ticket-retriever: "Retrieve PROJ-302"

# 2. Create standalone implementation approach  
jira-task-parser: "Create implementation plan for PROJ-302"

# 3. Execute the plan systematically
task-implementer: "Implement plan feature-messaging-PROJ-302.md"
```

### Artifact-Based Planning and Implementation
```bash
# 1. Archive the ticket first
jira-ticket-retriever: "Retrieve PROJ-302"

# 2. Create plan within artifact directory
jira-task-parser: "Create implementation plan for /.github/artifacts/2025-11-06/JIRA-PROJ-302-do-not-allow-duplicate-source-referenceids-invoi/ticket.md"

# 3. Execute the artifact-based plan
task-implementer: "Implement plan from /.github/artifacts/2025-11-06/JIRA-PROJ-302-do-not-allow-duplicate-source-referenceids-invoi/implementation-plan.md"
```

### Continuing Interrupted Work
```bash
# Resume where you left off
task-implementer: "Continue implementing the current plan"

# Or resume specific plan
task-implementer: "Resume implementing feature-messaging-PROJ-302.md"
```

### Sprint Retrospective Preparation
```bash
# Archive all completed tickets for analysis
jira-ticket-retriever: "Retrieve PROJ-302, PROJ-303, PROJ-304, PROJ-305"

# Or export completed tickets with workflow analysis
jira-ticket-retriever: "Export all Done tickets with state durations"
```

### Advanced Filtering and Reporting
```bash
# Export high priority bugs
jira-ticket-retriever: "Export all high priority bugs to CSV"

# Group tickets by assignee
jira-ticket-retriever: "Show all tickets grouped by assignee with statistics"

# Filter by date range
jira-ticket-retriever: "Get all tickets created in the last 7 days"

# Custom JQL query
jira-ticket-retriever: "Export tickets where assignee is me and status not in Done or Closed"
```

### Epic and Child Issue Management
```bash
# List all epics
jira-ticket-retriever: "List all epics in the PROJ project"

# Get epic with children
jira-ticket-retriever: "Retrieve epic PROJ-227 with all child issues"
```

### Workflow Performance Analysis
```bash
# Export with changelog and analyze
jira-ticket-retriever: "Export In Progress tickets and analyze state durations"
```

### Quick Ticket Information (No Artifacts)
```bash
# Ask questions without creating artifacts
jira-ticket-retriever: "What's PROJ-302 about?"
jira-ticket-retriever: "Show me the status of PROJ-302"
jira-ticket-retriever: "What priority is PROJ-302?"
```

## Jira Tool Output Formats

The jira-tool supports multiple output formats optimized for different use cases:

| Format | Best For | Usage |
|--------|----------|-------|
| **table** | Console viewing, human-readable | Default, excellent for terminal review |
| **json** | Readability, API integration, small-medium datasets | `--format json -o results.json` |
| **csv** | Spreadsheet import (Excel, Google Sheets) | `--format csv -o tickets.csv` |
| **jsonl** | Large datasets (100+ issues), streaming | `--format jsonl -o large.jsonl` (most efficient) |

**Format Selection Guide:**
- Use **JSONL** for large exports (100+ issues) - most memory efficient
- Use **JSON** for smaller datasets needing human readability
- Use **CSV** when opening in spreadsheet applications
- Use **Table** for immediate console viewing

## Available Jira Tool Commands

| Command | Description | Example |
|---------|-------------|---------|
| `get` | Get full details of a Jira issue | `uv run jira-tool get PROJ-123` |
| `search` | Search for issues using JQL queries | `uv run jira-tool search "status = 'In Progress'"` |
| `create` | Create a new issue with customizable fields | `uv run jira-tool create --summary "Task" --type Task` |
| `update` | Update issue fields and transition status | `uv run jira-tool update PROJ-123 --status "Done"` |
| `comment` | Add a comment to an issue | `uv run jira-tool comment PROJ-123 -m "comment"` |
| `transitions` | Show all available state transitions | `uv run jira-tool transitions PROJ-123` |
| `epics` | List all epics in a project | `uv run jira-tool epics --project PROJ` |
| `epic-details` | Get epic details with optional children | `uv run jira-tool epic-details PROJ-100 --show-children` |
| `export` | Export issues with advanced filtering | `uv run jira-tool export --format csv -o tickets.csv` |
| `analyze` | Analyze issue data (state durations, etc.) | `uv run jira-tool analyze state-durations issues.json` |

## File Organization Summary

```
/path/to/your/project/.github/
├── artifacts/                    # jira-ticket-retriever output
│   └── YYYY-MM-DD/
│       └── JIRA-{ID}-{title}/
│           ├── ticket.md         # Original ticket data
│           ├── implementation-plan.md  # Artifact-based plans (optional)
│           └── durations.csv     # State analysis results (optional)
├── plan/                         # jira-task-parser standalone output  
│   └── {purpose}-{component}-{ticket-id}.md
└── src/                          # task-implementer output
    ├── main/java/                # Implementation code
    └── test/java/                # Test code
```

This clear separation ensures each prompt has a distinct purpose while supporting a comprehensive, traceable development workflow.