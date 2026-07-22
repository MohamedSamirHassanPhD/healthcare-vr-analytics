from app.models import SessionIn
from app.store import SessionStore


def test_add_and_list():
    store = SessionStore(":memory:")
    store.add(SessionIn(trainee_id="t1", scenario="s1", duration_s=100, errors=1, pre_score=7, post_score=3))
    store.add(SessionIn(trainee_id="t2", scenario="s1", duration_s=120, errors=0, pre_score=6, post_score=2))
    store.add(SessionIn(trainee_id="t3", scenario="s2", duration_s=90, errors=2, pre_score=8, post_score=5))

    assert len(store.all()) == 3
    assert len(store.all(scenario="s1")) == 2
