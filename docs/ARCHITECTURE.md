# EmailPilot Architecture

## Overview

EmailPilot is a Python library for generating professional email drafts from brief instructions. It is built around three core subsystems: the **Tone Engine**, the **Template Manager**, and the **Formatter**.

## Components

### EmailPilot (core.py)

The main class that orchestrates email drafting. It exposes the public API:

- `draft(intent, tone, context)` — Generate an email from a brief description
- `set_tone(tone)` — Set the default tone
- `add_template(name, template)` — Register a custom template
- `use_template(name, variables)` — Render a template with variables
- `format_email(draft)` — Clean up and format a raw draft
- `suggest_subject(content)` — Generate a subject line from email body
- `check_tone(text)` — Analyze the tone of existing text
- `get_templates()` — List all available templates

### Config (config.py)

Pydantic-based configuration with environment variable support:

- Default tone, sender name, signature
- Validation of allowed tones

### Utils (utils.py)

Utility functions for text processing:

- `format_paragraphs()` — Normalize whitespace and line breaks
- `render_template()` — Substitute variables in templates
- `get_tone_words()` — Retrieve tone-specific vocabulary
- `capitalize_sentences()` — Proper sentence capitalization
- `extract_keywords()` — Pull key terms from text for subject lines

## Data Flow

```
User Intent
    |
    v
EmailPilot.draft()
    |
    +---> Tone Engine (select greeting, closing, word choices)
    |
    +---> Template Manager (optional: use a predefined structure)
    |
    +---> Formatter (clean whitespace, capitalize, structure)
    |
    v
Formatted Email String
```

## Design Decisions

1. **Pydantic for config** — Validation, environment variable loading, and type safety
2. **No external AI dependency** — Rule-based drafting for predictable, offline use
3. **Extensible templates** — Users can register custom templates at runtime
4. **Tone word lists** — Curated vocabulary per tone ensures consistent voice
