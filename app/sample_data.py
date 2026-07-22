"""Synthetic session generator for demo/tests (no real patient data)."""
from __future__ import annotations

import numpy as np

from app.models import SessionIn
from app.store import SessionStore

SCENARIOS = ["iud_insertion_vr", "leopold_maneuver_holographic", "labour_pushing_vr"]


def seed_demo_data(store: SessionStore, n_per_scenario: int = 20, seed: int = 7) -> None:
    rng = np.random.default_rng(seed)
    for scenario in SCENARIOS:
        for i in range(n_per_scenario):
            pre = float(np.clip(rng.normal(7.0, 1.2), 0, 10))
            improvement = float(np.clip(rng.normal(3.0, 1.0), 0, 10))
            post = float(np.clip(pre - improvement, 0, 10))
            errors = max(0, int(rng.normal(5 - i * 0.15, 1.5)))
            duration = float(np.clip(rng.normal(420, 60), 120, 900))
            store.add(
                SessionIn(
                    trainee_id=f"trainee-{i % 8:02d}",
                    scenario=scenario,
                    duration_s=duration,
                    errors=errors,
                    pre_score=round(pre, 2),
                    post_score=round(post, 2),
                    scale_name="VAS_0_10",
                )
            )
