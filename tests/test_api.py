from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_analytics_endpoint_has_seeded_data():
    resp = client.get("/analytics/iud_insertion_vr")
    assert resp.status_code == 200
    body = resp.json()
    assert body["n_sessions"] > 0


def test_analytics_unknown_scenario_404():
    resp = client.get("/analytics/does_not_exist")
    assert resp.status_code == 404


def test_create_session():
    resp = client.post(
        "/sessions",
        json={
            "trainee_id": "new-1",
            "scenario": "iud_insertion_vr",
            "duration_s": 200,
            "errors": 1,
            "pre_score": 7,
            "post_score": 3,
        },
    )
    assert resp.status_code == 200
    assert resp.json()["id"] > 0
