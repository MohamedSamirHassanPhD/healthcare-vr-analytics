"""Cohort analytics for VR/immersive training sessions.

Computes the same summary statistics used in the author's published VR
training-outcome studies (pre/post anxiety-pain-competence scores, learning
curves across repeated sessions) — generalized here into a reusable analytics
module rather than one-off analysis scripts.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from app.models import SessionOut


@dataclass
class CohortSummary:
    scenario: str
    n_sessions: int
    n_trainees: int
    mean_pre: float
    mean_post: float
    mean_change: float
    effect_size_cohens_d: float
    mean_errors: float
    error_trend_per_session: float
    duration_p50_s: float
    duration_p90_s: float


def summarize(sessions: list[SessionOut], scenario: str) -> CohortSummary:
    if not sessions:
        raise ValueError("no sessions to summarize")

    pre = np.array([s.pre_score for s in sessions], dtype=float)
    post = np.array([s.post_score for s in sessions], dtype=float)
    errors = np.array([s.errors for s in sessions], dtype=float)
    durations = np.array([s.duration_s for s in sessions], dtype=float)
    diff = post - pre

    # Paired Cohen's d: mean difference / std of the differences.
    diff_std = diff.std(ddof=1) if len(diff) > 1 else 0.0
    effect_size = float(diff.mean() / diff_std) if diff_std > 0 else 0.0

    # Learning-curve slope: linear fit of error count vs. session order,
    # negative slope == fewer errors as trainees repeat the scenario.
    order = np.arange(len(errors))
    trend = float(np.polyfit(order, errors, 1)[0]) if len(errors) > 1 else 0.0

    return CohortSummary(
        scenario=scenario,
        n_sessions=len(sessions),
        n_trainees=len({s.trainee_id for s in sessions}),
        mean_pre=round(float(pre.mean()), 3),
        mean_post=round(float(post.mean()), 3),
        mean_change=round(float(diff.mean()), 3),
        effect_size_cohens_d=round(effect_size, 3),
        mean_errors=round(float(errors.mean()), 3),
        error_trend_per_session=round(trend, 4),
        duration_p50_s=round(float(np.percentile(durations, 50)), 2),
        duration_p90_s=round(float(np.percentile(durations, 90)), 2),
    )
