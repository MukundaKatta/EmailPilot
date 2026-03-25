"""Core EmailPilot class — the main interface for drafting emails."""

from __future__ import annotations

from typing import Any

from emailpilot.config import EmailPilotConfig, ALLOWED_TONES
from emailpilot.utils import (
    capitalize_sentences,
    extract_keywords,
    format_paragraphs,
    get_tone_words,
    render_template,
    TONE_INDICATORS,
)


# ---------------------------------------------------------------------------
# Built-in templates
# ---------------------------------------------------------------------------

BUILTIN_TEMPLATES: dict[str, str] = {
    "follow-up": (
        "Dear {recipient_name},\n\n"
        "I hope this message finds you well. I am following up on {follow_up_topic}.\n\n"
        "I wanted to check in and see if there have been any updates or if there is "
        "anything further you need from my side.\n\n"
        "Please let me know at your earliest convenience.\n\n"
        "{closing},\n{sender_name}"
    ),
    "introduction": (
        "Dear {recipient_name},\n\n"
        "My name is {sender_name}, and I am reaching out to introduce myself. "
        "{introduction_context}\n\n"
        "I would love the opportunity to connect and discuss how we might collaborate.\n\n"
        "Looking forward to hearing from you.\n\n"
        "Best regards,\n{sender_name}"
    ),
    "thank-you": (
        "Dear {recipient_name},\n\n"
        "I wanted to take a moment to sincerely thank you for {thank_you_reason}. "
        "Your support and contribution have been truly valuable.\n\n"
        "I appreciate your time and effort, and I look forward to continuing our work together.\n\n"
        "With gratitude,\n{sender_name}"
    ),
    "meeting-request": (
        "Dear {recipient_name},\n\n"
        "I would like to request a meeting to discuss {meeting_topic}. "
        "Would {proposed_time} work for you?\n\n"
        "The meeting would take place at {meeting_location}. "
        "Please let me know if this time is convenient or if you would prefer an alternative.\n\n"
        "Thank you for your time.\n\n"
        "Best regards,\n{sender_name}"
    ),
    "apology": (
        "Dear {recipient_name},\n\n"
        "I sincerely apologize for {apology_reason}. I understand this may have caused "
        "inconvenience, and I take full responsibility.\n\n"
        "To address this, I plan to {corrective_action}. I am committed to ensuring "
        "this does not happen again.\n\n"
        "Thank you for your understanding.\n\n"
        "Sincerely,\n{sender_name}"
    ),
    "status-update": (
        "Dear {recipient_name},\n\n"
        "I wanted to provide a status update on {project_name}.\n\n"
        "Current progress: {current_status}\n\n"
        "Next steps: {next_steps}\n\n"
        "Expected completion: {timeline}\n\n"
        "Please feel free to reach out if you have any questions.\n\n"
        "Best regards,\n{sender_name}"
    ),
}


# ---------------------------------------------------------------------------
# EmailPilot class
# ---------------------------------------------------------------------------


class EmailPilot:
    """Email drafting assistant that generates professional email drafts.

    Supports tone adjustment, template management, and formatting.
    """

    def __init__(self, config: EmailPilotConfig | None = None) -> None:
        self.config = config or EmailPilotConfig()
        self._templates: dict[str, str] = dict(BUILTIN_TEMPLATES)
        self._current_tone: str = self.config.default_tone

    # -- Public API ---------------------------------------------------------

    def draft(
        self,
        intent: str,
        tone: str | None = None,
        context: dict[str, str] | None = None,
    ) -> str:
        """Generate a professional email draft from a brief intent description.

        Args:
            intent: Short description of what the email should convey.
            tone: One of 'formal', 'casual', 'friendly', 'urgent'.
                  Falls back to the current default tone.
            context: Optional dict with keys like 'recipient', 'sender', etc.
        """
        tone = tone or self._current_tone
        self._validate_tone(tone)
        ctx = context or {}

        tone_words = get_tone_words(tone)
        greeting = tone_words["greetings"][0]
        transition = tone_words["transitions"][0]
        closing = tone_words["closings"][0]

        recipient = ctx.get("recipient", "")
        sender = ctx.get("sender", self.config.sender_name or "")

        # Build greeting line
        if recipient:
            greeting_line = f"{greeting} {recipient},"
        else:
            greeting_line = f"{greeting},"

        # Build body
        body = f"{transition} {intent}."
        body = capitalize_sentences(body)

        # Build closing block
        closing_block = f"{closing},\n{sender}" if sender else f"{closing},"

        parts = [greeting_line, "", body, "", closing_block]
        raw = "\n".join(parts)
        return format_paragraphs(raw)

    def set_tone(self, tone: str) -> None:
        """Set the default tone for future drafts.

        Args:
            tone: One of 'formal', 'casual', 'friendly', 'urgent'.
        """
        self._validate_tone(tone)
        self._current_tone = tone

    def add_template(self, name: str, template: str) -> None:
        """Register a custom email template.

        Args:
            name: Template identifier (e.g. 'invoice-reminder').
            template: Template string with {variable} placeholders.
        """
        if not name or not name.strip():
            raise ValueError("Template name must not be empty")
        self._templates[name.strip()] = template

    def use_template(self, name: str, variables: dict[str, Any]) -> str:
        """Render a named template with the provided variables.

        Args:
            name: Template identifier.
            variables: Dict mapping placeholder names to values.

        Returns:
            The rendered email string.

        Raises:
            KeyError: If the template name is not found.
        """
        if name not in self._templates:
            available = ", ".join(sorted(self._templates.keys()))
            raise KeyError(f"Template '{name}' not found. Available: {available}")
        rendered = render_template(self._templates[name], variables)
        return format_paragraphs(rendered)

    def format_email(self, draft: str) -> str:
        """Clean up and format a raw email draft.

        Normalizes whitespace, capitalizes sentences, and trims blank lines.
        """
        formatted = capitalize_sentences(draft)
        return format_paragraphs(formatted)

    def suggest_subject(self, content: str) -> str:
        """Generate a subject line from email body content.

        Args:
            content: The email body text.

        Returns:
            A short suggested subject line.
        """
        keywords = extract_keywords(content, max_keywords=6)
        if not keywords:
            return "Follow-up"
        subject = " ".join(w.capitalize() for w in keywords[:5])
        return f"Re: {subject}"

    def check_tone(self, text: str) -> dict[str, Any]:
        """Analyze the tone of existing text.

        Returns a dict with the detected tone and confidence scores.
        """
        text_lower = text.lower()
        scores: dict[str, int] = {}
        for tone, indicators in TONE_INDICATORS.items():
            score = sum(1 for word in indicators if word in text_lower)
            scores[tone] = score

        total = sum(scores.values()) or 1
        confidence: dict[str, float] = {t: round(s / total, 2) for t, s in scores.items()}

        detected = max(scores, key=lambda t: scores[t])
        if scores[detected] == 0:
            detected = "neutral"

        return {
            "detected_tone": detected,
            "confidence": confidence,
            "scores": scores,
        }

    def get_templates(self) -> list[str]:
        """Return a sorted list of all available template names."""
        return sorted(self._templates.keys())

    # -- Private helpers ----------------------------------------------------

    @staticmethod
    def _validate_tone(tone: str) -> None:
        if tone not in ALLOWED_TONES:
            raise ValueError(f"Invalid tone '{tone}'. Must be one of {ALLOWED_TONES}")
