"""Test fixtures for Jira integration tests."""

# Sample Jira issue response
SAMPLE_ISSUE = {
    "key": "PROJ-123",
    "id": "10001",
    "fields": {
        "summary": "Sample Jira Issue",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This is a sample issue description."}
                    ],
                }
            ],
        },
        "status": {"name": "To Do", "id": "1"},
        "priority": {"name": "Medium", "id": "3"},
        "issuetype": {"name": "Task", "id": "10001"},
        "assignee": {
            "accountId": "user123",
            "displayName": "John Doe",
            "emailAddress": "john.doe@example.com",
        },
        "reporter": {
            "accountId": "user456",
            "displayName": "Jane Smith",
            "emailAddress": "jane.smith@example.com",
        },
        "created": "2023-01-01T00:00:00.000+0000",
        "updated": "2023-01-02T00:00:00.000+0000",
        "components": [{"name": "Authentication", "id": "10001"}],
        "labels": ["urgent", "bug-fix"],
        "project": {"key": "PROJ", "name": "Sample Project"},
    },
}

# Sample issue without optional fields
MINIMAL_ISSUE = {
    "key": "PROJ-124",
    "id": "10002",
    "fields": {
        "summary": "Minimal Issue",
        "status": {"name": "In Progress", "id": "2"},
        "issuetype": {"name": "Story", "id": "10002"},
        "created": "2023-01-01T00:00:00.000+0000",
        "updated": "2023-01-01T00:00:00.000+0000",
        "project": {"key": "PROJ", "name": "Sample Project"},
    },
}

# Sample epic issue
EPIC_ISSUE = {
    "key": "PROJ-470",
    "id": "10003",
    "fields": {
        "summary": "Platform Enhancement Implementation",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Implement platform enhancement for improved user experience.",
                        }
                    ],
                }
            ],
        },
        "status": {"name": "In Progress", "id": "2"},
        "priority": {"name": "High", "id": "2"},
        "issuetype": {"name": "Epic", "id": "10000"},
        "assignee": {
            "accountId": "user789",
            "displayName": "Epic Owner",
            "emailAddress": "epic.owner@example.com",
        },
        "created": "2023-01-01T00:00:00.000+0000",
        "updated": "2023-01-15T00:00:00.000+0000",
        "project": {"key": "PROJ", "name": "Sample Project"},
    },
}

# Sample search results
SEARCH_RESULTS = {"issues": [SAMPLE_ISSUE, MINIMAL_ISSUE], "total": 2, "maxResults": 50}

# Sample epic search results
EPIC_SEARCH_RESULTS = {"issues": [EPIC_ISSUE], "total": 1, "maxResults": 50}

# Sample transitions
ISSUE_TRANSITIONS = {
    "transitions": [
        {"id": "11", "name": "To Do", "to": {"name": "To Do", "id": "1"}},
        {"id": "21", "name": "In Progress", "to": {"name": "In Progress", "id": "2"}},
        {"id": "31", "name": "Done", "to": {"name": "Done", "id": "3"}},
    ]
}

# Sample comment response
COMMENT_RESPONSE = {
    "id": "10001",
    "created": "2023-01-01T12:00:00.000+0000",
    "updated": "2023-01-01T12:00:00.000+0000",
    "author": {"accountId": "user123", "displayName": "John Doe"},
    "body": {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "This is a test comment."}],
            }
        ],
    },
}

# Sample create issue response
CREATE_ISSUE_RESPONSE = {
    "key": "PROJ-125",
    "id": "10004",
    "self": "https://example.atlassian.net/rest/api/3/issue/10004",
}

# Sample field metadata
FIELD_METADATA = [
    {"id": "summary", "name": "Summary", "custom": False, "schema": {"type": "string"}},
    {
        "id": "customfield_11923",
        "name": "Epic Link",
        "custom": True,
        "schema": {
            "type": "string",
            "custom": "com.pyxis.greenhopper.jira:gh-epic-link",
        },
    },
    {
        "id": "customfield_10014",
        "name": "Epic Link",
        "custom": True,
        "schema": {
            "type": "string",
            "custom": "com.pyxis.greenhopper.jira:gh-epic-link",
        },
    },
]

# Sample create metadata for project
CREATE_METADATA = {
    "projects": [
        {
            "key": "PROJ",
            "name": "Sample Project",
            "issuetypes": [
                {
                    "id": "10001",
                    "name": "Task",
                    "fields": {
                        "summary": {
                            "name": "Summary",
                            "required": True,
                            "schema": {"type": "string"},
                        },
                        "description": {
                            "name": "Description",
                            "required": False,
                            "schema": {"type": "string"},
                        },
                        "priority": {
                            "name": "Priority",
                            "required": False,
                            "schema": {"type": "priority"},
                        },
                    },
                },
                {
                    "id": "10002",
                    "name": "Story",
                    "fields": {
                        "summary": {
                            "name": "Summary",
                            "required": True,
                            "schema": {"type": "string"},
                        },
                        "customfield_11923": {
                            "name": "Epic Link",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "custom": "com.pyxis.greenhopper.jira:gh-epic-link",
                            },
                        },
                    },
                },
            ],
        }
    ]
}

# Error responses
ERROR_UNAUTHORIZED = {
    "errorMessages": ["The request was rejected because no credentials were provided."],
    "errors": {},
}

ERROR_NOT_FOUND = {
    "errorMessages": ["Issue does not exist or you do not have permission to see it."],
    "errors": {},
}

ERROR_BAD_REQUEST = {
    "errorMessages": [],
    "errors": {
        "summary": "Summary is required.",
        "issuetype": "Issue type is required.",
    },
}

# Sample JQL queries for testing
SAMPLE_JQL_QUERIES = [
    "project = PROJ AND status = 'In Progress'",
    "assignee = currentUser() AND resolution = Unresolved",
    "project = PROJ AND issuetype = Epic",
    "labels = urgent AND priority = High",
]
