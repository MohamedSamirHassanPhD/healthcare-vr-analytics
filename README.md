# Healthcare VR Training Analytics

A small full-stack service for analyzing outcomes from repeated VR/immersive
clinical-training sessions: pre/post score change, effect size, and
learning-curve (error-rate trend) across trainees and scenarios.

The three seeded demo scenarios mirror the author's published VR/AI-immersive
healthcare-education research:

- **VR pain/anxiety during IUD insertion**
- **AI-based holographic learning for Leopold's maneuvers** (nursing competence)
- **VR-assisted pushing training, second stage of labour**

All session data in this repo is synthetic (`app/sample_data.py`) — a
reproducible, seeded generator standing in for de-identified trial data, so
there's no patient-data handling question, while the analytics themselves
(paired effect size, learning curves) are the real methodology used to
evaluate that kind of intervention.

## Analytics

- `mean_change` — average pre → post shift on the study's scale (e.g. VAS 0–10)
- `effect_size_cohens_d` — paired Cohen's d on the pre/post difference
- `error_trend_per_session` — linear-fit slope of error count vs. session
  order; negative = trainees improving with repetition
- `duration_p50_s` / `duration_p90_s` — session-time percentiles

## Run it

```bash
pip install -r requirements-dev.txt
uvicorn app.api:app --reload
```

Open `http://localhost:8000/` for the dashboard, or query the API directly:

```bash
curl localhost:8000/analytics/iud_insertion_vr
```

## Test

```bash
pytest -q
```

## Stack

Python · FastAPI · SQLite · NumPy · Chart.js · pytest

---
Part of a portfolio of applied AI/immersive-health-tech projects by
[Mohamed Samir Hassan](https://github.com/MohamedSamirHassanPhD), AI Solutions
Architect & PhD Researcher (AI Immersive Solutions).
