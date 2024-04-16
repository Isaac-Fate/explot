from typing import Optional
from enum import StrEnum
from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from .curve import plot_curve


DEFAULT_ARROW_DISTANCE = 0.5
DEFAULT_ARROW_LENGTH = 0.5


class DirectedLineSegmentArrowPosition(StrEnum):

    LEFT = "left"
    RIGHT = "right"


def plot_directed_line_segment(
    z0: complex,
    z1: complex,
    *,
    arrow_distance: Optional[float] = None,
    arrow_length: Optional[float] = None,
    arrow_position: Optional[DirectedLineSegmentArrowPosition] = None,
    ax: Optional[Axes] = None,
    **kwargs,
) -> None:

    # Get the current axes instance is it is not provided
    if ax is None:
        ax = plt.gca()

    # Draw the line segment
    artists = plot_curve(
        lambda t: (1 - t) * z0 + t * z1,
        0,
        1,
        ax=ax,
        **kwargs,
    )

    # Get the line
    line = artists[0]

    # Do nothing if no arrow position is provided
    if arrow_position is None:
        return

    # Set default values if not provided

    if arrow_distance is None:
        arrow_distance = DEFAULT_ARROW_DISTANCE

    if arrow_length is None:
        arrow_length = DEFAULT_ARROW_LENGTH

    # Middle point of the line
    z_mid = (z0 + z1) / 2

    # Directional vector
    z_directional = z1 - z0
    z_directional /= abs(z_directional)

    # Normal vector
    z_normal = (z1 - z0) * 1j
    z_normal /= abs(z_normal)

    match arrow_position:

        case DirectedLineSegmentArrowPosition.LEFT:
            arrow_mid = z_mid + z_normal * arrow_distance

        case DirectedLineSegmentArrowPosition.RIGHT:
            arrow_mid = z_mid - z_normal * arrow_distance

    arrow_start = arrow_mid - z_directional * arrow_length / 2
    arrow_end = arrow_mid + z_directional * arrow_length / 2

    # Draw the arrow annotation
    ax.annotate(
        "",
        xy=(arrow_end.real, arrow_end.imag),
        xytext=(arrow_start.real, arrow_start.imag),
        arrowprops=dict(
            arrowstyle="->",
            # The color of the arrow is the same as the line
            color=line.get_color(),
        ),
    )
