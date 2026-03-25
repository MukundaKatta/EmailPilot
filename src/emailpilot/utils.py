"""Utility functions for text formatting, tone word lists, and template rendering."""

from __future__ import annotations

import re
from typing import Any


# ---------------------------------------------------------------------------
# Tone word lists
# ---------------------------------------------------------------------------

TONE_GREETINGS: dict[str, list[str]] = {
    "formal": ["Dear", "To whom it may concern,", "Respected"],
    "casual": ["Hi", "Hey", "Hello"],
    "friendly": ["Hi there", "Hello", "Hey"],
    "urgent": ["Attention:", "Dear", "Important —"],
}

TONE_CLOSINGS: dict[str, list[str]] = {
    "formal": ["Sincerely", "Best regards", "Respectfully"],
    "casual": ["Thanks", "Cheers", "Best"],
    "friendly": ["Warm regards", "Take care", "All the best"],
    "urgent": ["Regards", "Thank you for your prompt attention", "Best regards"],
}

TONE_TRANSITIONS: dict[str, list[str]] = {
    "formal": [
        "I am writing to",
        "I would like to bring to your attention",
        "Please find below",
        "I wish to inform you that",
    ],
    "casual": [
        "Just wanted to",
        "Quick note about",
        "Thought I'd reach out about",
        "Dropping a line about",
    ],
    "friendly": [
        "I hope this message finds you well! I wanted to",
        "Hope you're doing great! Just reaching out to",
        "It's great to connect! I wanted to",
    ],
    "urgent": [
        "This requires your immediate attention regarding",
        "I need to urgently discuss",
        "Time-sensitive matter:",
        "Please prioritize the following:",
    ],
}

TONE_INDICATORS: dict[str, list[str]] = {
    "formal": [
        "sincerely", "respectfully", "pursuant", "herein", "accordingly",
        "furthermore", "regarding", "kindly", "shall", "hereby",
    ],
    "casual": [
        "hey", "thanks", "cool", "sure", "awesome", "cheers",
        "gonna", "btw", "fyi", "asap",
    ],
    "friendly": [
        "wonderful", "great", "lovely", "happy", "excited",
        "thrilled", "appreciate", "hope", "enjoy", "welcome",
    ],
    "urgent": [
        "immediately", "asap", "urgent", "critical", "deadline",
        "overdue", "priority", "now", "crucial", "time-sensitive",
    ],
}


# ---------------------------------------------------------------------------
# Text formatting helpers
# ---------------------------------------------------------------------------


def format_paragraphs(text: str) -> str:
    """Normalize whitespace: collapse blank lines, strip trailing spaces."""
    lines = text.splitlines()
    cleaned: list[str] = []
    prev_blank = False
    for line in lines:
        stripped = line.rstrip()
        if stripped == "":
            if not prev_blank:
                cleaned.append("")
            prev_blank = True
        else:
            cleaned.append(stripped)
            prev_blank = False
    # Strip leading / trailing blank lines
    while cleaned and cleaned[0] == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()
    return "\n".join(cleaned)


def capitalize_sentences(text: str) -> str:
    """Capitalize the first letter of each sentence."""
    def _cap(match: re.Match[str]) -> str:
        return match.group(0).upper()

    result = re.sub(r"(?<=[.!?]\s)([a-z])", _cap, text)
    # Capitalize very first character
    if result and result[0].islower():
        result = result[0].upper() + result[1:]
    return result


def render_template(template: str, variables: dict[str, Any]) -> str:
    """Render a template string by substituting {variable} placeholders."""
    result = template
    for key, value in variables.items():
        result = result.replace("{" + key + "}", str(value))
    return result.strip()


def extract_keywords(text: str, max_keywords: int = 5) -> list[str]:
    """Extract significant words from text for subject line generation."""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "it", "that", "this", "was", "are",
        "be", "has", "had", "have", "will", "would", "could", "should", "may",
        "can", "do", "did", "not", "so", "if", "my", "your", "our", "we", "i",
        "me", "you", "he", "she", "they", "them", "his", "her", "its", "us",
        "am", "been", "being", "as", "just", "about", "also", "very", "there",
    }
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    keywords = [w for w in words if w not in stop_words]
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return unique[:max_keywords]


def get_tone_words(tone: str) -> dict[str, list[str]]:
    """Return greeting, closing, and transition word lists for a given tone."""
    return {
        "greetings": TONE_GREETINGS.get(tone, TONE_GREETINGS["formal"]),
        "closings": TONE_CLOSINGS.get(tone, TONE_CLOSINGS["formal"]),
        "transitions": TONE_TRANSITIONS.get(tone, TONE_TRANSITIONS["formal"]),
    }
