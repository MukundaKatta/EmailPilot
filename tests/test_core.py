"""Tests for the EmailPilot core module."""

import pytest

from emailpilot import EmailPilot
from emailpilot.config import EmailPilotConfig


class TestEmailPilotDraft:
    """Tests for the draft() method."""

    def test_draft_formal_tone(self) -> None:
        pilot = EmailPilot()
        result = pilot.draft(
            intent="discuss the quarterly budget review",
            tone="formal",
            context={"recipient": "Alice", "sender": "Bob"},
        )
        assert "Dear Alice," in result
        assert "Bob" in result
        assert "quarterly budget review" in result

    def test_draft_casual_tone(self) -> None:
        pilot = EmailPilot()
        result = pilot.draft(
            intent="share the project update",
            tone="casual",
            context={"recipient": "Mike"},
        )
        assert "Hi Mike," in result
        assert "project update" in result

    def test_draft_uses_default_tone(self) -> None:
        config = EmailPilotConfig(default_tone="friendly")
        pilot = EmailPilot(config=config)
        result = pilot.draft(intent="say hello")
        assert "Hi there," in result

    def test_draft_invalid_tone_raises(self) -> None:
        pilot = EmailPilot()
        with pytest.raises(ValueError, match="Invalid tone"):
            pilot.draft(intent="test", tone="angry")


class TestEmailPilotTone:
    """Tests for set_tone() and check_tone()."""

    def test_set_tone(self) -> None:
        pilot = EmailPilot()
        pilot.set_tone("urgent")
        result = pilot.draft(intent="escalate the server outage")
        assert "Attention:" in result or "immediate" in result.lower() or "urgent" in result.lower()

    def test_check_tone_detects_urgent(self) -> None:
        pilot = EmailPilot()
        analysis = pilot.check_tone("We need this done IMMEDIATELY. This is URGENT and critical.")
        assert analysis["detected_tone"] == "urgent"
        assert analysis["scores"]["urgent"] > 0

    def test_check_tone_detects_friendly(self) -> None:
        pilot = EmailPilot()
        analysis = pilot.check_tone("Hope you're having a wonderful day! So excited to share this great news.")
        assert analysis["detected_tone"] == "friendly"


class TestEmailPilotTemplates:
    """Tests for template management."""

    def test_get_templates_includes_builtins(self) -> None:
        pilot = EmailPilot()
        templates = pilot.get_templates()
        assert "follow-up" in templates
        assert "introduction" in templates
        assert "thank-you" in templates
        assert "meeting-request" in templates
        assert "apology" in templates
        assert "status-update" in templates

    def test_use_template_renders_variables(self) -> None:
        pilot = EmailPilot()
        result = pilot.use_template("thank-you", {
            "recipient_name": "Dr. Smith",
            "thank_you_reason": "your mentorship this past year",
            "sender_name": "Jane",
        })
        assert "Dr. Smith" in result
        assert "your mentorship this past year" in result
        assert "Jane" in result

    def test_add_custom_template(self) -> None:
        pilot = EmailPilot()
        pilot.add_template("custom", "Hello {name}, welcome to {company}!")
        result = pilot.use_template("custom", {"name": "Alex", "company": "Acme"})
        assert "Hello Alex, welcome to Acme!" in result

    def test_use_template_missing_raises(self) -> None:
        pilot = EmailPilot()
        with pytest.raises(KeyError, match="not found"):
            pilot.use_template("nonexistent", {})


class TestEmailPilotUtils:
    """Tests for format_email and suggest_subject."""

    def test_format_email_cleans_whitespace(self) -> None:
        pilot = EmailPilot()
        raw = "\n\n  Hello there.   \n\n\n  this is a test.  \n\n"
        result = pilot.format_email(raw)
        assert "\n\n\n" not in result
        assert result.startswith("Hello")

    def test_suggest_subject(self) -> None:
        pilot = EmailPilot()
        subject = pilot.suggest_subject("Following up on the quarterly budget discussion from last week.")
        assert subject.startswith("Re:")
        assert len(subject) > 4
