# Advanced Builder Patterns for Jira Documents

## Table of Contents
1. [Complex Nested Structures](#complex-nested-structures)
2. [Builder Best Practices](#builder-best-practices)
3. [Reusing and Extending Builders](#reusing-and-extending-builders)
4. [Specialized Patterns](#specialized-patterns)

## Complex Nested Structures

ADF supports hierarchical nesting for sophisticated layouts. Use multi-level headings, panels within sections, and combined formatting.

### Complex Example: Multi-Level Epic with Risk Assessment

```python
doc = JiraDocumentBuilder()

# Header
doc.add_heading("🚀 Payment System Redesign", 1)
doc.add_paragraph(
    doc.bold("Priority: "), doc.add_text("P0"),
    doc.add_text(" | "),
    doc.bold("Timeline: "), doc.add_text("Q2 2024")
)

# Problem section
doc.add_heading("Problem", 2)
doc.add_panel("warning", {
    "type": "paragraph",
    "content": [doc.add_text("Current system handles only credit cards; enterprise needs ACH/wire")]
})

# Solution approach
doc.add_heading("Solution Approach", 2)
doc.add_bullet_list([
    "Abstract payment gateway interface",
    "Implement ACH driver with bank reconciliation",
    "Add webhook for transaction status"
])

# Technical requirements
doc.add_heading("Technical Requirements", 2)
doc.add_ordered_list([
    "Design payment abstraction",
    "Implement ACH provider integration",
    "Add transaction state machine",
    "Create reconciliation batch process"
])

# Code example
doc.add_heading("Reference Implementation", 2)
doc.add_code_block("""
class PaymentGateway:
    def process(self, amount, method):
        driver = self._get_driver(method)
        return driver.charge(amount)

    def _get_driver(self, method):
        if method == 'ach':
            return ACHDriver()
        elif method == 'credit':
            return CreditCardDriver()
""", language="python")

# Risk assessment
doc.add_heading("Risk Assessment", 2)
doc.add_heading("Financial Risk", 3)
doc.add_panel("error", {
    "type": "paragraph",
    "content": [doc.add_text("ACH payments are slow and reversible; implement hold period")]
})
doc.add_heading("Integration Risk", 3)
doc.add_panel("warning", {
    "type": "paragraph",
    "content": [doc.add_text("Requires new bank partnership; 2-week setup time")]
})

# Acceptance criteria
doc.add_heading("Acceptance Criteria", 2)
doc.add_ordered_list([
    "ACH charges succeed with test account",
    "Reconciliation matches bank records",
    "All error cases handled",
    "Documentation complete",
    "Load test passes (100+ TPS)"
])

# Dependencies
doc.add_heading("Dependencies", 2)
doc.add_bullet_list([
    "Bank partnership agreement",
    "Infrastructure team support",
    "Security review approval"
])

adf = doc.build()
```

## Builder Best Practices

### Best Practice 1: Return self for Chaining
```python
class CustomBuilder:
    def add_something(self) -> "CustomBuilder":
        # ... implementation
        return self  # Allow chaining

# Usage
builder.add_a().add_b().add_c().add_d()
```

### Best Practice 2: Lazy Content
```python
# ❌ Don't require all content upfront
def __init__(self, title, items, criteria):
    pass

# ✅ Build step-by-step
def __init__(self, title):
    self.title = title

def add_items(self, items):
    # ...
    return self

def add_criteria(self, criteria):
    # ...
    return self
```

### Best Practice 3: Validate Before Building
```python
def build(self) -> dict:
    """Build and validate before returning."""
    if not self.title:
        raise ValueError("Title is required")
    if not self.builder.content:
        raise ValueError("Content is empty")

    return self.builder.build()
```

### Best Practice 4: Document Structure
```python
class DocumentTemplate:
    """
    Template for standard epic documentation.

    Structure:
    - Header (title, priority, timeline)
    - Problem statement (warning panel)
    - Solution approach (bullet list)
    - Technical requirements (ordered list)
    - Code examples (code blocks)
    - Risk assessment (info/warning panels)
    - Acceptance criteria (ordered list)
    - Dependencies (bullet list)
    """

    def __init__(self, title: str):
        pass
```

## Reusing and Extending Builders

### Pattern: Builder Inheritance
```python
class BaseIssueBuilder(JiraDocumentBuilder):
    """Base for all issue templates."""

    def add_standard_header(self, title: str, issue_type: str):
        self.add_heading(title, 1)
        self.add_paragraph(
            self.bold(f"Type: "),
            self.add_text(issue_type)
        )
        return self

class BugBuilder(BaseIssueBuilder):
    """Specialized builder for bug reports."""

    def add_reproduction_steps(self, steps: list[str]):
        self.add_heading("Steps to Reproduce", 2)
        self.add_ordered_list(steps)
        return self

    def add_expected_vs_actual(self, expected: str, actual: str):
        self.add_heading("Expected vs Actual", 2)
        self.add_paragraph(
            self.bold("Expected: "),
            self.add_text(expected)
        )
        self.add_paragraph(
            self.bold("Actual: "),
            self.add_text(actual)
        )
        return self

# Usage
bug = BugBuilder()
bug.add_standard_header("Login fails on Safari", "Bug")
bug.add_reproduction_steps([
    "Open Safari 17",
    "Visit login.example.com",
    "Click 'Sign In with Google'",
    "Approve permissions"
])
bug.add_expected_vs_actual(
    "Redirect to dashboard",
    "Blank page with JS console error"
)

adf = bug.build()
```

## Specialized Patterns

### Pattern 1: Titled Panels (common pattern)
```python
def add_titled_panel(builder, title, panel_type, content):
    """Add a heading followed by a panel."""
    builder.add_heading(title, 2)
    builder.add_panel(panel_type, {
        "type": "paragraph",
        "content": [builder.add_text(content)]
    })

# Usage
doc = JiraDocumentBuilder()
add_titled_panel(doc, "⚠️ Risks", "warning", "Performance impact on v1 API")
add_titled_panel(doc, "✅ Benefits", "success", "Eliminates 50% of CPU usage")
```

### Pattern 2: Key-Value Pairs (common in specifications)
```python
def add_kv_section(builder, title, pairs):
    """Add a section with key-value pairs."""
    builder.add_heading(title, 2)
    items = []
    for key, value in pairs.items():
        items.append(f"{key}: {value}")
    builder.add_bullet_list(items)

# Usage
doc = JiraDocumentBuilder()
add_kv_section(doc, "Specifications", {
    "Language": "Python 3.10+",
    "Framework": "FastAPI",
    "Database": "PostgreSQL 13"
})
```

### Pattern 3: Feature Lists (for requirements)
```python
def add_feature_list(builder, title, features):
    """Add a section with feature checklist."""
    builder.add_heading(title, 2)
    items = [f"☐ {f}" for f in features]
    builder.add_bullet_list(items)

# Usage
doc = JiraDocumentBuilder()
add_feature_list(doc, "Must-Have Features", [
    "User authentication",
    "Database persistence",
    "API rate limiting"
])
```
