"""Data model for a single VR/immersive-training session record."""
from __future__ import annotations

from pydantic import BaseModel, Field


class SessionIn(BaseModel):
    trainee_id: str
    scenario: str = Field(
        description="e.g. 'iud_insertion_vr', 'leopold_maneuver_holographic', 'labour_pushing_vr'"
    )
    duration_s: float
    errors: int = 0
    pre_score: float = Field(description="baseline anxiety/pain/competence score before session")
    post_score: float = Field(description="same scale, measured after the session")
    scale_name: str = Field(default="VAS_0_10", description="scoring scale used")


class SessionOut(SessionIn):
    id: int
    created_at: str
