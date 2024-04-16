from typing import Optional, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from ..types import RealVector, ComplexVector
from .curve_arrow import CurveArrow


ARROW_SIZE_FACTOR = 0.015
ARROW_HEAD_LENGTH_TO_HEAD_WIDTH_RATIO = 1 / 0.618


def plot_curve(
    curve: Callable[[float | RealVector], complex | ComplexVector],
    a: float,
    b: float,
    *,
    num_samples: int = 100,
    arrow_points: Optional[list[float]] = None,
    add_middle_arrow_point: bool = False,
    dt: Optional[float] = None,
    ax: Optional[Axes] = None,
    **kwargs,
) -> tuple[Line2D | CurveArrow]:

    # Get the current axes instance is it is not provided
    if ax is None:
        ax = plt.gca()

    t_vector = np.linspace(a, b, num_samples)
    z_vector = curve(t_vector)

    # Plot the curve
    lines = ax.plot(z_vector.real, z_vector.imag, **kwargs)

    # Get the one and only line
    line = lines[-1]

    if arrow_points is None:

        if not add_middle_arrow_point:
            return (line,)

        # Calculate the middle arrow point
        middle_arrow_point = t_vector.mean()

        # Add the middle arrow point
        arrow_points = [middle_arrow_point]

    # Range of the arrow point t
    t_min = min(t_vector)
    t_max = max(t_vector)

    arrows: list[CurveArrow] = []
    for t in arrow_points:
        # Ensure that t must be in the range [t_min, t_max]
        assert (
            t_min <= t < t_max
        ), f"Arrow point {t} is not in the range [{t_min}, {t_max})"

        if dt is None:
            # Find the first index of the number in vector that is greater than t
            # The value pointed by the index will be denoted as t1
            # Its preceding value in the vector will be denoted as t0
            # And dt will be set to t1 - t0
            t1_index = find_first_value_greater_than(t, t_vector)

            # Although t1_index is garanteed to be non-None since t is in the range [t_min, t_max)
            assert (
                t1_index is not None
            ), f"Cannot find a value in the vector that is  greater than {t}"

            # Index of t0
            t0_index = t1_index - 1

            # Calculate dt
            t0 = t_vector[t0_index]
            t1 = t_vector[t1_index]
            dt = t1 - t0

        # Calculate the position of the arrow
        z = curve(t)
        x = z.real
        y = z.imag

        # Calculate the dx and dy
        dz = curve(t + dt) - z
        dx = dz.real
        dy = dz.imag

        # Add the arrow to the line
        arrow = add_arrow_to_line(line, x, y, dx, dy, ax=ax)
        arrows.append(arrow)

    # Return the line (curve) as well as the arrows
    return tuple((line, *arrows))


def add_arrow_to_line(
    line: Line2D,
    x,
    y,
    dx,
    dy,
    ax: Optional[Axes] = None,
) -> CurveArrow:

    # Get the current axes instance is it is not provided
    if ax is None:
        ax = plt.gca()

    # Color of the line
    color = line.get_color()

    # Create the arrow
    arrow = CurveArrow(
        x,
        y,
        dx,
        dy,
        # Set dummy values for head width and head length
        # since they will be updated later in the function `update_curve_arrows`
        head_width=0,
        head_length=0,
        # The color of the arrow is the same as the line
        color=color,
        # The zorder of the arrow is the same as the line
        zorder=line.get_zorder(),
    )

    # Add the arrow to the axes
    ax.add_patch(arrow)

    # Update arrows since the x and y limits of the axes may have changed
    update_curve_arrows(ax=ax)

    # The newly added arrow
    arrow = list(filter(lambda x: isinstance(x, CurveArrow), ax.patches))[-1]

    return arrow


def update_curve_arrows(
    *,
    ax: Optional[Axes] = None,
) -> None:

    # Get the current axes instance is it is not provided
    if ax is None:
        ax = plt.gca()

    # The total delta x and y of the axes
    total_delta_x = ax.get_xlim()[1] - ax.get_xlim()[0]
    total_delta_y = ax.get_ylim()[1] - ax.get_ylim()[0]

    # Calculate the arrow size
    arrow_size = np.sqrt(total_delta_x**2 + total_delta_y**2) * ARROW_SIZE_FACTOR

    # Calculate the arrow head width
    # arrow_head_with = line_width * ARROW_HEAD_WIDTH_TO_LINE_WIDTH_RATIO
    arrow_head_width = arrow_size

    # Calculate the arrow head length
    arrow_head_length = ARROW_HEAD_LENGTH_TO_HEAD_WIDTH_RATIO * arrow_head_width

    # Clear all curve arrows in the patches
    old_arrow: CurveArrow
    for old_arrow in list(filter(lambda x: isinstance(x, CurveArrow), ax.patches)):

        # Create a new arrow with the updated properties
        arrow = CurveArrow(
            old_arrow.x,
            old_arrow.y,
            old_arrow.dx,
            old_arrow.dy,
            head_width=arrow_head_width,
            head_length=arrow_head_length,
            color=old_arrow.color,
            zorder=old_arrow.zorder,
        )

        # Remove the old arrow
        old_arrow.remove()

        # Add the new arrow to the axes
        ax.add_patch(arrow)


def find_first_value_greater_than(
    value: float,
    sorted_array: RealVector,
) -> Optional[int]:

    start = 0
    end = len(sorted_array) - 1

    # Handle corner cases

    if sorted_array[start] > value:
        return start

    if sorted_array[end] <= value:
        return None

    # Note that, now start < end

    # Get the middle index
    mid = (start + end) // 2

    # The loop preserves the invariant that
    # sorted_array[start] <= value < sorted_array[end]
    while mid > start:

        # Update the start or end index
        if sorted_array[mid] > value:
            end = mid
        else:
            start = mid

        # Update the middle index
        mid = (start + end) // 2

    # Here, end is start + 1 since the middle index remains unchanged
    return end
