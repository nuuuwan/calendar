import calendar

from utils import Log, TimeFormat, _

from cal.AbstractCalendar import AbstractCalendar
from cal.HOLIDAYS import HOLIDAYS

log = Log("YearCalendar")


class YearCalendar(AbstractCalendar):

    N_X = 4
    N_Y = 3
    BOX_WIDTH = AbstractCalendar.DISPLAY_WIDTH / N_X
    BOX_HEIGHT = AbstractCalendar.DISPLAY_HEIGHT / N_Y

    def __init__(self, year):
        self.year = year

    def __str__(self):
        return f"{self.year}"

    @property
    def time_format(self):
        return TimeFormat("%Y")

    def render_title(self):
        return _(
            "text",
            TimeFormat("%Y").stringify(self.time),
            self.point(0.5, -0.07)
            | dict(
                font_size=30,
                text_anchor="middle",
            ),
        )

    def render_box_background(
        self,
        x,
        y,
    ):
        return _(
            "rect",
            None,
            dict(
                fill="#fff",
                stroke="black",
                width=self.BOX_WIDTH,
                height=self.BOX_HEIGHT,
            )
            | self.point(x / self.N_X, y / self.N_Y),
        )

    def render_box_day(self, x, y, day):
        return _(
            "text",
            f"{day}" if day != 0 else "",
            dict(
                fill="black",
                stroke="none",
                font_size=20,
                width=self.BOX_WIDTH,
                height=self.BOX_HEIGHT,
            )
            | self.point(
                (x + 0.1) / self.N_X,
                (y + 0.2) / self.N_Y,
            ),
        )

    def render_box(self, x, y, day):
        if not day:
            return None

        return _(
            "g",
            [
                self.render_box_background(
                    x,
                    y,
                ),
                self.render_box_day(x, y, day),
            ],
        )

    def render_box_grid(self):
        box_list = []

        months = list(calendar.month_name[1:])

        for i, month in enumerate(months):
            y = i % self.N_Y
            x = i // self.N_Y
            box = self.render_box(x, y, month)
            box_list.append(box)
        return box_list

    def render_header_box_row(self):

        header_box_row = []
        for y in [-0.014, 1.03]:
            for x, qtr_name in enumerate(["Q1", "Q2", "Q3", "Q4"]):
                header_box = _(
                    "g",
                    [
                        _(
                            "text",
                            qtr_name,
                            dict(
                                fill="black",
                                stroke="none",
                                text_anchor="middle",
                                font_size=20,
                                width=self.DISPLAY_WIDTH / 7,
                                height=self.DISPLAY_HEIGHT / 6,
                            )
                            | self.point(
                                (x + 0.5) / self.N_X,
                                y,
                            ),
                        ),
                    ],
                )
                header_box_row.append(header_box)

        return header_box_row

    def render(self):
        return _(
            "svg",
            self.render_header_box_row()
            + self.render_box_grid()
            + [self.render_title()],
            dict(
                width=self.WIDTH,
                height=self.HEIGHT,
                font_family="Menlo",
            ),
        )
