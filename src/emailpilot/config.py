"""Configuration for EmailPilot using Pydantic."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator


ToneType = Literal["formal", "casual", "friendly", "urgent"]

ALLOWED_TONES: list[str] = ["formal", "casual", "friendly", "urgent"]


class EmailPilotConfig(BaseModel):
    """Configuration model for EmailPilot."""

    default_tone: ToneType = "formal"
    sender_name: str = ""
    signature: str = "Best regards"
    debug: bool = False

    @field_validator("default_tone")
    @classmethod
    def validate_tone(cls, v: str) -> str:
        if v not in ALLOWED_TONES:
            raise ValueError(f"Tone must be one of {ALLOWED_TONES}, got '{v}'")
        return v

    model_config = {
        "env_prefix": "EMAILPILOT_",
    }
