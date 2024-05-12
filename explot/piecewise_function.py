from typing import Optional, Callable
import portion
import numpy as np
from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from .types import RealVector


def plot_piecewise_function(
    *,
    x: RealVector,
    intervals: list[portion.Interval],
    functions: list[Callable[[float | RealVector], float | RealVector]],
    ax: Optional[Axes] = None,
    color: Optional[str] = None,
    line_width: Optional[float] = None,
    jump_line: bool = True,
    jump_line_style: str = "--",
    jump_line_width: Optional[float] = None,
    jump_line_color: Optional[str] = None,
    jump_point: bool = True,
    jump_point_size: float = 20,
    jump_point_color: Optional[str] = None,
    label: Optional[str] = None,
):

    # Get the current axes instance is it is not provided
    if ax is None:
        ax = plt.gca()

    # The function value at the right endpoint of the last interval
    prev_right_endpoint_function_value = None

    for i, (interval, function) in enumerate(zip(intervals, functions)):

        # Get flags associated with the left endpoint
        match interval.left:

            case portion.OPEN:
                left_endpoint_flags = x > interval.lower

            case portion.CLOSED:
                left_endpoint_flags = x >= interval.lower

        # Get flags associated with the right endpoint
        match interval.right:

            case portion.OPEN:
                right_endpoint_flags = x < interval.upper

            case portion.CLOSED:
                right_endpoint_flags = x <= interval.upper

        # Get the flags associated with the interval
        interval_flags = np.logical_and(left_endpoint_flags, right_endpoint_flags)

        # Get the points in the interval
        points = x[interval_flags]

        # Calculate function values
        values = function(points)

        # Plot the function
        lines = ax.plot(
            points,
            values,
            color=color,
            linewidth=line_width,
            # Only show the label for the first line
            label=label if i == 0 else None,
        )
        line = lines[0]

        # If color is not provided, use the color of the first line
        if color is None and i == 0:
            color = line.get_color()

        # If color of the jump line or jump point is not provided, use the color of the first line
        if i == 0:
            jump_line_color = color if jump_line_color is None else jump_line_color
            jump_point_color = color if jump_point_color is None else jump_point_color

        # Plot jump line and jump points
        if jump_line and prev_right_endpoint_function_value is not None:

            # Get the left endpoint
            left_endpoint = interval.lower

            # Get the left endpoint function value
            left_endpoint_function_value = values[0]

            # Plot the jump line
            ax.plot(
                [left_endpoint, left_endpoint],
                [prev_right_endpoint_function_value, left_endpoint_function_value],
                linestyle=jump_line_style,
                linewidth=jump_line_width,
                color=jump_line_color,
            )

            # Plot the jump points
            if jump_point:

                match interval.left:

                    case portion.OPEN:

                        # Left endpoint is included at the previous right endpoint
                        ax.scatter(
                            left_endpoint,
                            prev_right_endpoint_function_value,
                            marker="o",
                            sizes=[jump_point_size],
                            facecolor=jump_point_color,
                            edgecolor=jump_point_color,
                            zorder=line.zorder,
                        )

                        # Left endpoint is excluded at this line
                        ax.scatter(
                            left_endpoint,
                            left_endpoint_function_value,
                            marker="o",
                            sizes=[jump_point_size],
                            facecolor="none",
                            edgecolor=jump_point_color,
                            zorder=line.zorder,
                        )

                    case portion.CLOSED:

                        # Left endpoint is excluded at the previous right endpoint
                        ax.scatter(
                            left_endpoint,
                            prev_right_endpoint_function_value,
                            marker="o",
                            sizes=[jump_point_size],
                            facecolor="none",
                            edgecolor=jump_point_color,
                            zorder=line.zorder,
                        )

                        # Left endpoint is included at this line
                        ax.scatter(
                            left_endpoint,
                            left_endpoint_function_value,
                            marker="o",
                            sizes=[jump_point_size],
                            facecolor=jump_point_color,
                            edgecolor=jump_point_color,
                            zorder=line.zorder,
                        )

        # Keep track of the right endpoint function value for plotting the jump line
        prev_right_endpoint_function_value = values[-1]
