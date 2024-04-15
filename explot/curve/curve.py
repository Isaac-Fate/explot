from typing import Optional, Callable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from ..types import RealVector, ComplexVector
from .curve_arrow import CurveArrow


ARROW_HEAD_LENGTH_TO_HEAD_WIDTH_RATIO = 1 / 0.618


def plot_curve(
    curve: Callable[[float | RealVector], complex | ComplexVector],
    a: float,
    b: float,
    *,
    num_samples: int = 100,
    arrow_points: Optional[list[float]] = None,
    add_middle_arrow_point: bool = False,
    dt: float = np.finfo(np.float64).eps,
    ax: Optional[Axes] = None,
    **kwargs,
) -> None:

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
            return

        # Calculate the middle arrow point
        middle_arrow_point = t_vector.mean()

        # Add the middle arrow point
        arrow_points = [middle_arrow_point]

    # Range of the arrow point t
    t_min = min(t_vector)
    t_max = max(t_vector)

    for t in arrow_points:
        # Ensure that t must be in the range [t_min, t_max]
        assert (
            t_min <= t <= t_max
        ), f"Arrow point {t} is not in the range [{t_min}, {t_max}]"

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

    return arrow


def add_arrow_to_line(
    line: Line2D,
    x,
    y,
    dx,
    dy,
    ax: Optional[Axes] = None,
):

    # Get the current axes instance is it is not provided
    if ax is None:
        ax = plt.gca()

    # Color of the line
    color = line.get_color()

    total_delta_x = ax.get_xlim()[1] - ax.get_xlim()[0]
    total_delta_y = ax.get_ylim()[1] - ax.get_ylim()[0]
    arrow_size = np.sqrt(total_delta_x**2 + total_delta_y**2) * 0.015

    # Calculate the arrow head width
    # arrow_head_with = line_width * ARROW_HEAD_WIDTH_TO_LINE_WIDTH_RATIO
    arrow_head_width = arrow_size

    # Calculate the arrow head length
    arrow_head_length = ARROW_HEAD_LENGTH_TO_HEAD_WIDTH_RATIO * arrow_head_width

    # Create the arrow
    arrow = CurveArrow(
        x,
        y,
        dx,
        dy,
        head_width=arrow_head_width,
        head_length=arrow_head_length,
        # The color of the arrow is the same as the line
        color=color,
        # The zorder of the arrow is the same as the line
        zorder=line.get_zorder(),
    )

    # Add the arrow to the axes
    ax.add_patch(arrow)

    # Update arrows since the x and y limits of the axes may have changed
    update_curve_arrows(ax=ax)

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
    arrow_size = np.sqrt(total_delta_x**2 + total_delta_y**2) * 0.015

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
