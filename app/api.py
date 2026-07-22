"""FastAPI service for VR training-session analytics."""
from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.analytics import summarize
from app.models import SessionIn, SessionOut
from app.sample_data import seed_demo_data
from app.store import SessionStore

app = FastAPI(
    title="Healthcare VR Training Analytics",
    description=(
        "Tracks pre/post outcome scores, error rates, and learning curves "
        "across repeated VR/immersive clinical-training sessions."
    ),
    version="1.0.0",
)

store = SessionStore(":memory:")
seed_demo_data(store)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/sessions", response_model=SessionOut)
def create_session(session: SessionIn) -> SessionOut:
    return store.add(session)


@app.get("/sessions", response_model=list[SessionOut])
def list_sessions(scenario: str | None = None) -> list[SessionOut]:
    return store.all(scenario=scenario)


@app.get("/analytics/{scenario}")
def analytics(scenario: str) -> dict:
    sessions = store.all(scenario=scenario)
    if not sessions:
        raise HTTPException(status_code=404, detail=f"no sessions for scenario '{scenario}'")
    return asdict(summarize(sessions, scenario))
