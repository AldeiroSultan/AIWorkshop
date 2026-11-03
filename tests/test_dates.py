from datetime import date, timedelta

from app.dates import days_left


def test_deadline_far_in_the_future_has_days_left():
    deadline = date.today() + timedelta(days=100)
    assert days_left(deadline) > 0


def test_deadline_long_ago_has_passed():
    deadline = date.today() - timedelta(days=100)
    assert days_left(deadline) < 0
