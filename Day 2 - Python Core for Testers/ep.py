"""Equivalence partitioning for a sample age-based ticket rule."""


def partition(age: int) -> str:
    """Classify age into a ticket-pricing equivalence class.

    Assumed rule for this exercise: ages 0-12 are children, 13-17 teenagers,
    18-64 adults, 65-120 seniors, and values outside that range are invalid.
    """
    if not isinstance(age, int) or isinstance(age, bool):
        return "invalid"
    if age < 0 or age > 120:
        return "invalid"
    if age <= 12:
        return "child"
    if age <= 17:
        return "teenager"
    if age <= 64:
        return "adult"
    return "senior"
