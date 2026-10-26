"""Robust boundary-value points for an inclusive integer range."""


def boundary_values(minimum: int, maximum: int) -> list[int]:
    """Return the six robust BVA points around an inclusive valid range.

    The range must contain at least three valid integers so that the values
    immediately inside each boundary are distinct.
    """
    if not isinstance(minimum, int) or isinstance(minimum, bool):
        raise TypeError("minimum must be an integer")
    if not isinstance(maximum, int) or isinstance(maximum, bool):
        raise TypeError("maximum must be an integer")
    if maximum - minimum < 2:
        raise ValueError("range must contain at least three integers")

    return [
        minimum - 1,
        minimum,
        minimum + 1,
        maximum - 1,
        maximum,
        maximum + 1,
    ]
