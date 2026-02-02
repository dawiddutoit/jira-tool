"""Tests for ADF text extraction."""


from jira_tool.document.adf import extract_text_from_adf


class TestExtractTextFromAdf:
    """Test suite for extract_text_from_adf function."""

    def test_string_passthrough(self) -> None:
        """Plain strings are returned unchanged."""
        assert extract_text_from_adf("Hello world") == "Hello world"

    def test_non_doc_dict_returns_str(self) -> None:
        """Non-doc dicts are converted to string."""
        result = extract_text_from_adf({"type": "other", "value": "test"})
        assert "other" in result

    def test_empty_doc(self) -> None:
        """Empty doc returns empty string."""
        doc = {"type": "doc", "version": 1, "content": []}
        assert extract_text_from_adf(doc) == ""

    def test_paragraph_with_text(self) -> None:
        """Paragraphs extract text content."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Hello world"}],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "Hello world" in result

    def test_heading_level_1(self) -> None:
        """Heading level 1 prefixes with single #."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [{"type": "text", "text": "Title"}],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "# Title" in result

    def test_heading_level_3(self) -> None:
        """Heading level 3 prefixes with ###."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": [{"type": "text", "text": "Subsection"}],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "### Subsection" in result

    def test_bullet_list(self) -> None:
        """Bullet lists use bullet character."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Item 1"}],
                                }
                            ],
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Item 2"}],
                                }
                            ],
                        },
                    ],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "• Item 1" in result
        assert "• Item 2" in result

    def test_ordered_list(self) -> None:
        """Ordered lists use numbered format."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "orderedList",
                    "attrs": {"order": 1},
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "First"}],
                                }
                            ],
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Second"}],
                                }
                            ],
                        },
                    ],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "1. First" in result
        assert "2. Second" in result

    def test_code_block(self) -> None:
        """Code blocks are wrapped in triple backticks."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "codeBlock",
                    "attrs": {"language": "python"},
                    "content": [{"type": "text", "text": "print('hello')"}],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "```python" in result
        assert "print('hello')" in result
        assert "```" in result

    def test_panel(self) -> None:
        """Panels show type label."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "panel",
                    "attrs": {"panelType": "warning"},
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Warning message"}],
                        }
                    ],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "[WARNING]" in result
        assert "Warning message" in result

    def test_emoji_with_text(self) -> None:
        """Emoji nodes extract text attribute."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "emoji", "attrs": {"text": "👍", "shortName": ":+1:"}}
                    ],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "👍" in result

    def test_emoji_without_text_uses_shortname(self) -> None:
        """Emoji falls back to shortName when text missing."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "emoji", "attrs": {"shortName": ":smile:"}}],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert ":smile:" in result

    def test_complex_document(self) -> None:
        """Complex document with multiple node types."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [{"type": "text", "text": "Main Title"}],
                },
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Introduction text."}],
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Point one"}],
                                }
                            ],
                        }
                    ],
                },
            ],
        }
        result = extract_text_from_adf(doc)
        assert "# Main Title" in result
        assert "Introduction text" in result
        assert "• Point one" in result


class TestExtractTextFromAdfEdgeCases:
    """Edge case tests for extract_text_from_adf."""

    def test_missing_content(self) -> None:
        """Nodes without content are handled gracefully."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph"}],
        }
        result = extract_text_from_adf(doc)
        assert result == ""

    def test_unknown_node_type_with_content(self) -> None:
        """Unknown node types with content are traversed."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "unknownNode",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Nested text"}],
                        }
                    ],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "Nested text" in result

    def test_empty_text_node(self) -> None:
        """Empty text nodes don't cause errors."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": ""}],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert result == ""

    def test_code_block_without_language(self) -> None:
        """Code blocks without language default to empty."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "codeBlock",
                    "attrs": {},
                    "content": [{"type": "text", "text": "code here"}],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "```\n" in result or "```" in result
        assert "code here" in result

    def test_panel_without_type(self) -> None:
        """Panel without type defaults to INFO."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "panel",
                    "attrs": {},
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Info message"}],
                        }
                    ],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "[INFO]" in result

    def test_ordered_list_custom_start(self) -> None:
        """Ordered lists can start from custom number."""
        doc = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "orderedList",
                    "attrs": {"order": 5},
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Fifth item"}],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        result = extract_text_from_adf(doc)
        assert "5. Fifth item" in result
