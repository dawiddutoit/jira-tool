# Jira Formatting Guide

This guide explains how to use the Jira tool client to create well-formatted issues using Atlassian Document Format (ADF).

## Quick Start

```python
from jira_tool.client import JiraClient
from jira_tool.formatter import JiraDocumentBuilder

# Create a document
doc = JiraDocumentBuilder()

# Add content
doc.add_heading("My Issue", 1)
doc.add_paragraph(doc.add_text("Description here"))
doc.add_bullet_list(["Item 1", "Item 2", "Item 3"])

# Get the ADF content
content = doc.build()

# Create or update an issue
client = JiraClient()
client.update_issue("PROJ-123", {"description": content})
```

## Common Patterns

### 1. Technical Task

```python
doc = JiraDocumentBuilder()

# Overview with emoji
doc.add_heading("📋 Overview", 2)
doc.add_panel("info", {
    "type": "paragraph",
    "content": [{"type": "text", "text": "Task description"}]
})

# Technical details
doc.add_heading("⚡ Technical Details", 2)
doc.add_bullet_list([
    "Implementation detail 1",
    "Implementation detail 2"
])

# Acceptance criteria
doc.add_heading("🎯 Acceptance Criteria", 2)
# Use success panel for criteria
```

### 2. Bug Report

```python
doc = JiraDocumentBuilder()

doc.add_heading("🐛 Bug Report", 1)

# Steps to reproduce
doc.add_heading("Steps to Reproduce", 2)
doc.add_ordered_list([
    "Step 1",
    "Step 2",
    "Step 3"
])

# Error logs
doc.add_heading("Error Logs", 2)
doc.add_code_block("error text here", "text")
```

### 3. Using Convenience Methods

The `add_titled_panel()` method combines a heading with a panel:

```python
doc.add_titled_panel(
    title="📋 Overview",
    panel_type="info",
    content="This combines a heading and panel in one call"
)
```

## Available Methods

### Basic Content
- `add_heading(text, level)` - Add headings (level 1-6)
- `add_paragraph(*nodes)` - Add paragraph with mixed content
- `add_text(text, marks)` - Create text with optional formatting
- `add_rule()` - Add horizontal rule

### Lists
- `add_bullet_list(items)` - Unordered list
- `add_ordered_list(items, start)` - Ordered list

### Special Content
- `add_panel(type, *content)` - Info/warning/error/success panels
- `add_code_block(code, language)` - Code with syntax highlighting
- `add_emoji(shortname, unicode)` - Emoji support

### Text Formatting
- `bold(text)` - Bold text
- `italic(text)` - Italic text
- `code(text)` - Inline code
- `link(text, url)` - Hyperlinks
- `strikethrough(text)` - Strikethrough

### Convenience
- `add_titled_panel(title, panel_type, content, heading_level)` - Heading + panel combo
- `build_simple(text)` - Quick single paragraph document

## Panel Types

- `info` - Blue informational panel
- `note` - Purple note panel  
- `warning` - Yellow warning panel
- `success` - Green success panel
- `error` - Red error panel

## Code Language Support

Common languages for `add_code_block()`:
- `python`
- `javascript`/`typescript`
- `java`/`kotlin`
- `bash`/`shell`
- `yaml`/`json`
- `text` (no highlighting)

## Tips

1. **Use emojis sparingly** - They help with visual scanning but can be overwhelming
2. **Structure consistently** - Use the same heading levels and panel types across similar issues
3. **Keep panels focused** - One main point per panel
4. **Test formatting** - Use preview or dry-run options before creating issues

## Examples

See `/docs/examples/jira_document_examples.py` for complete working examples of:
- Technical tasks
- Bug reports
- Feature requests
- Documentation tasks

## Creating One-off Scripts

For specific tickets that need custom formatting:

```python
#!/usr/bin/env python3
"""One-off script for PROJ-123."""

from jira_tool.client import JiraClient
from jira_tool.formatter import JiraDocumentBuilder

def create_proj_123_content():
    doc = JiraDocumentBuilder()
    
    # Build your specific content here
    doc.add_heading("Specific Task", 1)
    # ... rest of content
    
    return doc.build()

def main():
    client = JiraClient()
    content = create_proj_123_content()
    
    client.update_issue("PROJ-123", {
        "summary": "Updated Summary",
        "description": content
    })
    print("✅ Updated PROJ-123")

if __name__ == "__main__":
    main()
```

This approach keeps one-off scripts simple while leveraging the existing formatting capabilities.