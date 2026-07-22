"""SQLite-backed session store (stdlib only, no extra DB server needed)."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from app.models import SessionIn, SessionOut

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trainee_id TEXT NOT NULL,
    scenario TEXT NOT NULL,
    duration_s REAL NOT NULL,
    errors INTEGER NOT NULL,
    pre_score REAL NOT NULL,
    post_score REAL NOT NULL,
    scale_name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class SessionStore:
    def __init__(self, db_path: str | Path = ":memory:"):
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(SCHEMA)
        self._conn.commit()

    def add(self, session: SessionIn) -> SessionOut:
        now = datetime.now(timezone.utc).isoformat()
        cur = self._conn.execute(
            """INSERT INTO sessions
               (trainee_id, scenario, duration_s, errors, pre_score, post_score, scale_name, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session.trainee_id,
                session.scenario,
                session.duration_s,
                session.errors,
                session.pre_score,
                session.post_score,
                session.scale_name,
                now,
            ),
        )
        self._conn.commit()
        return SessionOut(id=cur.lastrowid, created_at=now, **session.model_dump())

    def all(self, scenario: str | None = None) -> list[SessionOut]:
        if scenario:
            rows = self._conn.execute(
                "SELECT * FROM sessions WHERE scenario = ? ORDER BY id", (scenario,)
            ).fetchall()
        else:
            rows = self._conn.execute("SELECT * FROM sessions ORDER BY id").fetchall()
        return [SessionOut(**dict(r)) for r in rows]
