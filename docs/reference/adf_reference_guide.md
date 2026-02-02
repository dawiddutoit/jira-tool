# Atlassian Document Format (ADF) Reference Guide for Jira Epics and Issues

## Overview
This guide provides standardized ADF templates for formatting Jira epics and issues with rich content support.

## Epic Structure Template

An epic should include:
1. **Epic Title** (H2 heading)
2. **Executive Summary** (paragraph with bold labels)
3. **Problem Statement** (H3 heading + paragraph)
4. **Description** (H3 heading + paragraphs)
5. **Technical Details** (H3 heading + bullet list and code blocks)
6. **Acceptance Criteria** (H3 heading + checkbox list)
7. **Dependencies** (H3 heading + table)
8. **Timeline** (H3 heading + table)

### Example Epic ADF Structure:
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [
        { "type": "text", "text": "Epic: Authentication System Overhaul" }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Priority: ", "marks": [{ "type": "strong" }] },
        { "type": "text", "text": "P0" }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "Problem Statement" }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Description of the problem..." }
      ]
    }
  ]
}
```

## Issue/Story Structure Template

A standard issue should include:
1. **Issue Summary** (paragraph)
2. **Problem Statement** (H3 heading + paragraph)
3. **Description** (H3 heading + paragraphs)
4. **Technical Details** (H3 heading + bullet list/code blocks)
5. **Acceptance Criteria** (H3 heading + task list)
6. **Testing Considerations** (H3 heading + bullet list)

### Example Issue ADF Structure:
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Priority: ", "marks": [{ "type": "strong" }] },
        { "type": "text", "text": "P0" },
        { "type": "text", "text": " | " },
        { "type": "text", "text": "Dependencies: ", "marks": [{ "type": "strong" }] },
        { "type": "text", "text": "None" },
        { "type": "text", "text": " | " },
        { "type": "text", "text": "Services: ", "marks": [{ "type": "strong" }] },
        { "type": "text", "text": "Some Service" }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "Problem Statement" }
      ]
    }
  ]
}
```

## Common ADF Node Types

### 1. Text with Formatting
```json
{
  "type": "text",
  "text": "Bold text",
  "marks": [{ "type": "strong" }]
}
```

### 2. Code Block
```json
{
  "type": "codeBlock",
  "attrs": { "language": "kotlin" },
  "content": [
    {
      "type": "text",
      "text": "fun federationEnabled(): Mono<Unit> = Mono.just(\\n    if (federationEnabled) Unit else throw FederationServiceUnavailableException()\\n)"
    }
  ]
}
```

### 3. Bullet List
```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "First item" }
          ]
        }
      ]
    }
  ]
}
```

### 4. Task List (Checkbox)
```json
{
  "type": "taskList",
  "attrs": { "localId": "task-list-1" },
  "content": [
    {
      "type": "taskItem",
      "attrs": { "localId": "task-1", "state": "TODO" },
      "content": [
        { "type": "text", "text": "Feature flag toggles federation on/off" }
      ]
    }
  ]
}
```

### 5. Table
```json
{
  "type": "table",
  "attrs": { "isNumberColumnEnabled": false, "layout": "default" },
  "content": [
    {
      "type": "tableRow",
      "content": [
        {
          "type": "tableHeader",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Field" }
              ]
            }
          ]
        },
        {
          "type": "tableHeader",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Value" }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Best Practices

1. **Use Semantic Structure**: Use headings to organize content hierarchically
2. **Bold Key Labels**: Make important labels stand out (Priority, Dependencies, etc.)
3. **Code Formatting**: Use code blocks for technical details and inline code for variable names
4. **Lists for Multiple Items**: Use bullet lists for unordered items, numbered lists for steps
5. **Task Lists for Acceptance Criteria**: Make criteria checkable
6. **Tables for Structured Data**: Use tables for dependencies, timelines, or comparisons
7. **Consistent Formatting**: Maintain the same structure across all epics and issues

## Python Helper Functions

```python
def create_heading(text: str, level: int = 3) -> Dict[str, Any]:
    """Create a heading node."""
    return {
        "type": "heading",
        "attrs": {"level": level},
        "content": [{"type": "text", "text": text}]
    }

def create_paragraph(content: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a paragraph node."""
    return {
        "type": "paragraph",
        "content": content
    }

def create_text(text: str, marks: List[str] = None) -> Dict[str, Any]:
    """Create a text node with optional formatting."""
    node = {"type": "text", "text": text}
    if marks:
        node["marks"] = [{"type": mark} for mark in marks]
    return node

def create_code_block(code: str, language: str = "text") -> Dict[str, Any]:
    """Create a code block node."""
    return {
        "type": "codeBlock",
        "attrs": {"language": language},
        "content": [{"type": "text", "text": code}]
    }

def create_bullet_list(items: List[str]) -> Dict[str, Any]:
    """Create a bullet list node."""
    return {
        "type": "bulletList",
        "content": [
            {
                "type": "listItem",
                "content": [
                    create_paragraph([create_text(item)])
                ]
            }
            for item in items
        ]
    }

def create_task_list(tasks: List[str]) -> Dict[str, Any]:
    """Create a task list (checkbox list) node."""
    return {
        "type": "taskList",
        "attrs": {"localId": "task-list"},
        "content": [
            {
                "type": "taskItem",
                "attrs": {"localId": f"task-{i}", "state": "TODO"},
                "content": [create_text(task)]
            }
            for i, task in enumerate(tasks, 1)
        ]
    }
```