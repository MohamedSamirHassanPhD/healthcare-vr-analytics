from app.analytics import summarize
from app.models import SessionIn, SessionOut


def _session(i, pre, post, errors):
    return SessionOut(
        id=i,
        trainee_id=f"t{i}",
        scenario="demo",
        duration_s=300,
        errors=errors,
        pre_score=pre,
        post_score=post,
        scale_name="VAS_0_10",
        created_at="now",
    )


def test_summarize_computes_expected_direction():
    sessions = [_session(i, pre=8.0 + i * 0.1, post=4.0 - i * 0.2, errors=5 - i) for i in range(5)]
    summary = summarize(sessions, "demo")
    assert summary.mean_change < 0  # scores went down (improvement)
    assert summary.effect_size_cohens_d != 0
    assert summary.error_trend_per_session < 0  # errors decreasing = learning curve


def test_summarize_raises_on_empty():
    import pytest

    with pytest.raises(ValueError):
        summarize([], "demo")
