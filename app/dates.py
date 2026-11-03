from datetime import date, datetime


def days_left(deadline: date) -> int:
    """Return how many days are left until the deadline.

    Negative means the deadline has passed.
    """
    deadline_time = datetime(deadline.year, deadline.month, deadline.day)
    return (deadline_time - datetime.now()).days
