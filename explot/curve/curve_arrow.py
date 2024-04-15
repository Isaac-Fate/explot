from matplotlib.patches import FancyArrow


class CurveArrow(FancyArrow):

    def __init__(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        *,
        head_width: float,
        head_length: float,
        color: str = "black",
        zorder: int = 0,
    ) -> None:

        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self._head_width = head_width
        self._head_length = head_length
        self._color = color
        self._zorder = zorder

        super().__init__(
            x,
            y,
            dx,
            dy,
            # Set `width` to 0 to remove the tail
            width=0,
            length_includes_head=True,
            head_width=head_width,
            head_length=head_length,
            shape="full",
            overhang=0.1,
            head_starts_at_zero=False,
            color=color,
            # Set `linewidth` to 0 to remove the border line
            linewidth=0,
            zorder=zorder,
        )

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def dx(self) -> float:
        return self._dx

    @property
    def dy(self) -> float:
        return self._dy

    @property
    def head_width(self) -> float:
        return self._head_width

    @property
    def head_length(self) -> float:
        return self._head_length

    @property
    def color(self) -> str:
        return self._color

    @property
    def zorder(self) -> int:
        return self._zorder
