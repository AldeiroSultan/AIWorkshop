from datetime import date


def days_left(deadline: date) -> int:
    """Return how many days are left until the deadline.

    Negative means the deadline has passed.
    """
    return (deadline - date.today()).days
